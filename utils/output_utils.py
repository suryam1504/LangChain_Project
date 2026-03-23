import re
from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnableLambda


def _clean_thinking(text: str) -> str:
    """Strip <think>...</think> blocks and any leading/trailing prose."""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


def _extract_all_json_objects(text: str) -> list:
    """Extract every complete top-level {...} JSON object from text, in order."""
    results = []
    i = 0
    while i < len(text):
        start = text.find("{", i)
        if start == -1:
            break
        depth = 0
        for j, ch in enumerate(text[start:], start=start):
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
            if depth == 0:
                results.append(text[start : j + 1])
                i = j + 1
                break
        else:
            # Unclosed/truncated block — still add it so last_error gets populated
            results.append(text[start:])
            break
    return results


def make_safe_parser(pydantic_class):
    """Drop-in replacement for PydanticOutputParser at the end of a LangChain chain.

    Handles thinking-model outputs (e.g. kimi-k2, qwen3) that:
      - Prepend <think>...</think> blocks
      - Echo the format-instructions JSON schema before the actual answer
      - Wrap the answer in prose

    Strategy:
      1. Strip <think>...</think> blocks
      2. Try parsing the full cleaned text
      3. Extract ALL {...} JSON objects and try each in order until one succeeds
         (this handles the case where the schema JSON appears before the answer)
    """
    inner = PydanticOutputParser(pydantic_object=pydantic_class)

    def _parse(llm_output):
        text = llm_output.content if hasattr(llm_output, "content") else str(llm_output)
        cleaned = _clean_thinking(text)

        # Try 1: parse cleaned text as-is
        try:
            return inner.parse(cleaned)
        except Exception:
            pass

        # Try 2: try every JSON object found in the text
        last_error = None
        for candidate in _extract_all_json_objects(cleaned):
            try:
                return inner.parse(candidate)
            except Exception as e:
                last_error = e

        raise OutputParserException(
            f"make_safe_parser: no candidate parsed successfully. Last error: {last_error}\nOutput (first 300 chars): {cleaned[:300]}"
        ) from last_error

    return RunnableLambda(_parse)
