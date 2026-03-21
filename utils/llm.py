from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

def get_llm(model="groq/compound-mini", temperature=0.7, max_tokens=1024):
    return ChatGroq(model=model, temperature=temperature, max_tokens=max_tokens)
    # llama-3.1-8b-instant, llama-3.3-70b-versatile, openai/gpt-oss-120b

# https://console.groq.com/docs/models
# https://console.groq.com/docs/rate-limits