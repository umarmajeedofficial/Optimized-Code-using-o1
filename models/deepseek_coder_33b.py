# models/deepseek_coder_33b.py

import openai

class DeepseekCoder33BModel:
    def __init__(self, api_key, base_url="https://api.aimlapi.com"):
        openai.api_key = api_key
        openai.api_base = base_url

    def generate_code(self, instruction):
        try:
            response = openai.ChatCompletion.create(
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
                max_tokens=2000,  # Adjust based on provider limits
            )
            return response.choices[0].message.content.strip()
        except openai.error.OpenAIError as e:
            # Log the error message for debugging
            return f"Error generating code: {str(e)}"

    def explain_code(self, instruction):
        try:
            response = openai.ChatCompletion.create(
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
                max_tokens=2000,  # Adjust based on provider limits
            )
            return response.choices[0].message.content.strip()
        except openai.error.OpenAIError as e:
            # Log the error message for debugging
            return f"Error explaining code: {str(e)}"
