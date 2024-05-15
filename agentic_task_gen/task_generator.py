
import openai

class TaskGenerationSystem:
    def __init__(self, api_key):
        openai.api_key = api_key

    def generate_tasks(self, task_component):
        for prompt in task_component.prompts:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ]
                )
                task_component.results.append(response['choices'][0]['message']['content'])
            except Exception as e:
                print(f"Error generating task for prompt '{prompt}': {e}")
                task_component.results.append(f"Error generating task: {e}")
