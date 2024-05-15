
class TaskDivisionSystem:
    def divide_task(self, task_component):
        subtasks = self._create_subtasks(task_component)
        return subtasks

    def _create_subtasks(self, task_component):
        subtasks = []
        for i, result in enumerate(task_component.results):
            subtask = SubTaskComponent(f"Subtask {i}: {result}", [task_component])
            subtasks.append(subtask)
        return subtasks
