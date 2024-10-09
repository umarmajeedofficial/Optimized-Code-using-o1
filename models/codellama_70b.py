# models/codellama_70b.py

from openai import OpenAI
import openai

class CodeLlama70BModel:
    def __init__(self, api_key, base_url="https://api.aimlapi.com"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def generate_code(self, instruction):
        try:
            response = self.client.chat.completions.create(
                model="codellama/CodeLlama-70b-hf",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an SQL code assistant.",
                    },
                    {
                        "role": "user",
                        "content": instruction
                    },
                ],
                max_tokens=2000,  # Temporarily reduced for testing
            )
            return response.choices[0].message.content.strip()
        except openai.error.OpenAIError as e:
            # Log the error message for debugging
            return f"Error generating code: {str(e)}"

    def explain_code(self, instruction):
        try:
            response = self.client.chat.completions.create(
                model="codellama/CodeLlama-70b-hf",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an SQL code assistant.",
                    },
                    {
                        "role": "user",
                        "content": instruction
                    },
                ],
                max_tokens=2000,  # Temporarily reduced for testing
            )
            return response.choices[0].message.content.strip()
        except openai.error.OpenAIError as e:
            # Log the error message for debugging
            return f"Error explaining code: {str(e)}"
