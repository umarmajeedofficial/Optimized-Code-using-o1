# models/phind_codellama_v2.py

from openai import OpenAI

class PhindCodeLlamaV2Model:
    def __init__(self, api_key, base_url="https://api.aimlapi.com"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def generate_code(self, instruction):
        response = self.client.chat.completions.create(
            model="Phind/Phind-CodeLlama-34B-Python-v1",
            messages=[
                {
                    "role": "user",
                    "content": instruction
                },
            ],
            max_tokens=10000,
        )
        return response.choices[0].message.content.strip()

    def explain_code(self, instruction):
        response = self.client.chat.completions.create(
            model="Phind/Phind-CodeLlama-34B-Python-v1",
            messages=[
                {
                    "role": "user",
                    "content": instruction
                },
            ],
            max_tokens=10000,
        )
        return response.choices[0].message.content.strip()

