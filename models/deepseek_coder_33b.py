# models/deepseek_coder_33b.py

from openai import OpenAI
import openai

class DeepseekCoder33BModel:
    def __init__(self, api_key, base_url="https://api.aimlapi.com"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def generate_code(self, instruction):
        try:
            response = self.client.chat.completions.create(
                model="deepseek-ai/deepseek-coder-33b-instruct",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI assistant who specializes in coding."
                    },
                    {
                        "role": "user",
                        "content": instruction
                    },
                ],
                max_tokens=2000,  # Reduced for testing
            )
            return response.choices[0].message.content.strip()
        except openai.error.OpenAIError as e:
            # Log the error message for debugging
            return f"Error generating code: {str(e)}"

    def explain_code(self, instruction):
        try:
            response = self.client.chat.completions.create(
                model="deepseek-ai/deepseek-coder-33b-instruct",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI assistant who specializes in coding."
                    },
                    {
                        "role": "user",
                        "content": instruction
                    },
                ],
                max_tokens=2000,  # Reduced for testing
            )
            return response.choices[0].message.content.strip()
        except openai.error.OpenAIError as e:
            # Log the error message for debugging
            return f"Error explaining code: {str(e)}"
