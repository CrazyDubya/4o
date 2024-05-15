from pr.llm import LLM
from pr.task_manager import TaskComponent


class TaskGenerationSystem:
    def __init__(self, llm: LLM):
        self.llm = llm

    def generate_task(self, prompt: str) -> TaskComponent:
        response = self.llm.generate(prompt)
        return TaskComponent(description=response)
