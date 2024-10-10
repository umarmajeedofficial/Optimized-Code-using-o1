# models/llama.py

from together import Together

class LlamaModel:
    def __init__(self, api_key, base_url="https://api.aimlapi.com/v1"):
        self.client = Together(base_url=base_url, api_key=api_key)

    def process_question(self, user_question):
        response = self.client.chat.completions.create(
            model="meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_question,
                        }
                    ],
                }
            ],
            max_tokens=5000,
        )
        
        llama_response = response.choices[0].message.content.strip()
        processed_string = llama_response.replace('"', '').replace("'", '').replace('\n', ' ')
        return processed_string
