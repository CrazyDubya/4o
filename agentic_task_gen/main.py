
import os
from components import TaskComponent
from task_generator import TaskGenerationSystem
from task_divider import TaskDivisionSystem
from task_integrator import TaskIntegrationSystem

# Ensure output directory exists
output_dir = "/mnt/data/agentic_task_gen/output/"
os.makedirs(output_dir, exist_ok=True)

# OpenAI API key
API_KEY = "your_openai_api_key_here"

# Initialize systems
task_gen_system = TaskGenerationSystem(API_KEY)
task_div_system = TaskDivisionSystem()
task_int_system = TaskIntegrationSystem()

# Create initial task
task = TaskComponent("Main Task", ["Generate a task list for organizing a hackathon."])

# Generate tasks
task_gen_system.generate_tasks(task)

# Divide tasks
subtasks = task_div_system.divide_task(task)

# Integrate tasks
final_result = task_int_system.integrate_tasks(subtasks)

# Create README.md
readme_content = task_int_system.create_readme(task.description, "output/\n  README.md\n  final_result.txt")
with open(os.path.join(output_dir, "README.md"), "w") as readme_file:
    readme_file.write(readme_content)

# Save final result
with open(os.path.join(output_dir, "final_result.txt"), "w") as result_file:
    result_file.write(final_result)

print("Task generation completed. Check the output directory for results.")
