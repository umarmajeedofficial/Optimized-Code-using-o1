# models/gemini_model.py

from openai import OpenAI

class GeminiModel:
    def __init__(self, api_key, base_url="https://api.aimlapi.com"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def generate_code(self, instruction):
        response = self.client.chat.completions.create(
            model="gemini-1.5-pro",
            messages=[
                {
                    "role": "user",
                    "content": instruction
                },
            ],
            max_tokens=1048,
        )
        return response.choices[0].message.content.strip()

    def explain_code(self, instruction):
        response = self.client.chat.completions.create(
            model="gemini-1.5-pro",
            messages=[
                {
                    "role": "user",
                    "content": instruction
                }
            ],
            max_tokens=1048,
        )
        return response.choices[0].message.content.strip()
