from openai import OpenAI
import os

def get_llm_client():
    # In a more complex scenario, you might have different LLM providers
    # or models, and this factory would handle their initialization.
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    return OpenAI(api_key=OPENAI_API_KEY)
