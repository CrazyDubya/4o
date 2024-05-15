
class TaskIntegrationSystem:
    def integrate_tasks(self, subtasks):
        final_result = ""
        for subtask in subtasks:
            final_result += subtask.task + "\n"
        return final_result

    def create_readme(self, task_description, file_tree):
        readme_content = f"# Project Overview\n\n{task_description}\n\n## File Tree\n\n{file_tree}"
        return readme_content
