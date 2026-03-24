# from dotenv import load_dotenv
# load_dotenv()

import os
from langchain_groq import ChatGroq

# On Streamlit Cloud: secrets are set in the dashboard and exposed via st.secrets.
# Locally: set GROQ_API_KEY in .env or your shell.
try:
    import streamlit as st
    if "GROQ_API_KEY" in st.secrets:
        os.environ.setdefault("GROQ_API_KEY", st.secrets["GROQ_API_KEY"])
except Exception:
    pass  # Running outside Streamlit (e.g. book_bot.py in terminal)

def get_llm(model="llama-3.3-70b-versatile", temperature=0.7, max_tokens=512):
    return ChatGroq(model=model, temperature=temperature, max_tokens=max_tokens)

# https://console.groq.com/docs/models
# https://console.groq.com/docs/rate-limits