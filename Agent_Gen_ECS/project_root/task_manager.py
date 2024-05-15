from typing import List, Dict

class TaskComponent:
    def __init__(self, description: str):
        self.description = description

class SubTaskComponent:
    def __init__(self, parent_task: TaskComponent, subtasks: List[TaskComponent]):
        self.parent_task = parent_task
        self.subtasks = subtasks

class TaskManager:
    def __init__(self):
        self.tasks = {}
        self.subtasks = {}

    def add_task(self, task: TaskComponent):
        self.tasks[task.description] = task

    def add_subtasks(self, task: TaskComponent, subtask_component: SubTaskComponent):
        self.subtasks[task.description] = subtask_component.subtasks
