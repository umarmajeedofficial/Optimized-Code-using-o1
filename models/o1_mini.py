# models/o1_mini.py

from openai import OpenAI

class O1MiniModel:
    def __init__(self, api_key, base_url="https://api.aimlapi.com"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def generate_code(self, instruction):
        response = self.client.chat.completions.create(
            model="o1-mini",
            messages=[
                {
                    "role": "user",
                    "content": instruction
                },
            ],
            max_tokens=1000,
        )
        return response.choices[0].message.content.strip()

    def explain_code(self, instruction):
        response = self.client.chat.completions.create(
            model="o1-mini",
            messages=[
                {
                    "role": "user",
                    "content": instruction
                }
            ],
            max_tokens=1000,
        )
        return response.choices[0].message.content.strip()
