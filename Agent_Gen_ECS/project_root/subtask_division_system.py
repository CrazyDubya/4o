from llm import LLM
from task_manager import TaskComponent, SubTaskComponent

class SubTaskDivisionSystem:
    def __init__(self, llm: LLM):
        self.llm = llm
    
    def divide_task(self, task: TaskComponent) -> SubTaskComponent:
        prompt = f"Divide the task: {task.description}"
        response = self.llm.generate(prompt)
        subtask_descriptions = response.split('\n')
        subtasks = [TaskComponent(description=desc) for desc in subtask_descriptions]
        return SubTaskComponent(parent_task=task, subtasks=subtasks)
