# models/mistral_model.py

from openai import OpenAI

class MistralModel:
    def __init__(self, api_key, base_url="https://api.aimlapi.com"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def generate_code(self, instruction):
        response = self.client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.3",
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
            max_tokens=2000,
        )
        return response.choices[0].message.content.strip()

    def explain_code(self, instruction):
        response = self.client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.3",
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
            max_tokens=2000,
        )
        return response.choices[0].message.content.strip()
