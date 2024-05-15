from openai import OpenAI
import logging

class LLM:
    def __init__(self):
        self.client = OpenAI(api_key='API')

    def generate(self, prompt: str) -> str:

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        result = response.choices[0]['message']['content'].strip()

        return result