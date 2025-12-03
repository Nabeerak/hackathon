import os
import google.generativeai as genai

class GeminiService:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.client = genai.GenerativeModel('gemini-2.5-flash')

    def get_chat_completion(self, messages: list[dict]) -> str:
        # Gemini's chat format expects roles like 'user' and 'model'
        # Convert OpenAI-like messages to Gemini's format
        gemini_messages = []
        for message in messages:
            if message["role"] == "system":
                # Gemini doesn't have a direct 'system' role in chat,
                # so we can prepend system instructions to the first user message
                if gemini_messages and gemini_messages[0]["role"] == "user":
                    gemini_messages[0]["parts"][0] = message["content"] + "\n" + gemini_messages[0]["parts"][0]
                else:
                    gemini_messages.insert(0, {"role": "user", "parts": [message["content"]]})
            elif message["role"] == "assistant":
                gemini_messages.append({"role": "model", "parts": [message["content"]]})
            else:
                gemini_messages.append({"role": message["role"], "parts": [message["content"]]})

        # Ensure the first message is from 'user'
        if gemini_messages and gemini_messages[0]["role"] == "model":
            # Prepend a dummy user message if the conversation starts with model
            gemini_messages.insert(0, {"role": "user", "parts": ["Hello"]})

        response = self.client.start_chat(history=gemini_messages[:-1]).send_message(gemini_messages[-1]["parts"][0])
        return response.text
