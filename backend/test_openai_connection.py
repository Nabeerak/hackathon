#!/usr/bin/env python
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

try:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    print("[OK] OpenAI client initialized")

    # Test with a simple completion
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say 'test successful'"}],
        max_tokens=10
    )
    print(f"[OK] API Response: {response.choices[0].message.content}")

except Exception as e:
    print(f"[ERROR] {type(e).__name__}: {e}")
