# models/gpt4o_model.py

from openai import OpenAI

class GPT4oModel:
    def __init__(self, api_key, base_url="https://api.aimlapi.com"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def generate_code(self, instruction):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "As a highly skilled software engineer, please analyze the following question thoroughly and provide optimized code for the problem & Make sure to give only code"
                },
                {
                    "role": "user",
                    "content": instruction
                },
            ],
            max_tokens=5000,
        )
        return response.choices[0].message.content.strip()

    def explain_code(self, instruction):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant who knows everything."
                },
                {
                    "role": "user",
                    "content": instruction
                }
            ],
            max_tokens=5000,
        )
        return response.choices[0].message.content.strip()
