import os
from openai import OpenAI

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def get_embedding(self, text: str) -> list[float]:
        response = self.client.embeddings.create(
            input=text,
            model="text-embedding-ada-002"
        )
        return response.data[0].embedding

    def get_chat_completion(self, messages: list[dict], model: str = "gpt-3.5-turbo") -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content
