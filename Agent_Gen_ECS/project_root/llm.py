import openai

class LLM:
    def generate(self, prompt: str) -> str:
        openai.api_key = 'your-api-key'
        response = openai.Completion.create(engine="davinci", prompt=prompt, max_tokens=100)
        return response.choices[0].text.strip()
