import os
import json
from datetime import datetime
from typing import List, Dict
from pr.task_generation_system import TaskGenerationSystem
from pr.subtask_division_system import SubTaskDivisionSystem
from pr.task_assignment_system import TaskAssignmentSystem
from pr.result_aggregation_system import ResultAggregationSystem
from pr.agent_management import AgentManagement
from pr.task_manager import TaskManager
from pr.llm import LLM

# Main Execution Flow
def main():
    llm = LLM()
    task_gen_system = TaskGenerationSystem(llm)
    subtask_div_system = SubTaskDivisionSystem(llm)
    task_assign_system = TaskAssignmentSystem()
    result_agg_system = ResultAggregationSystem()
    agent_mgmt = AgentManagement()
    task_manager = TaskManager()

    # Example Agents
    agents = [agent_mgmt.add_agent(f"agent_{i}") for i in range(3)]

    # Generate Main Task
    main_task = task_gen_system.generate_task("Create a comprehensive guide on AI-driven task management systems.")
    task_manager.add_task(main_task)

    # Divide Main Task into Sub-Tasks
    subtasks = subtask_div_system.divide_task(main_task)
    task_manager.add_subtasks(main_task, subtasks)

    # Assign Sub-Tasks to Agents
    assignments = task_assign_system.assign_tasks(subtasks, agents)

    # Simulate Agent Processing (For Demonstration)
    results = {agent: f"Result from {agent.agent_id} for {task.description}" for agent, task in assignments.items()}

    # Aggregate Results
    final_result = result_agg_system.aggregate_results(results)

    # Generate README.md
    readme_content = generate_readme()

    # Write README.md to File
    with open('readme.md', 'w') as readme_file:
        readme_file.write(readme_content)

    print("README.md generated successfully.")

def generate_readme():
    return f"""
# AI-Driven Task Management System

## Overview
This project implements an AI-driven task management system using principles from Unity's ECS (Entity Component System).

## Components
- **TaskComponent**: Stores task descriptions.
- **SubTaskComponent**: Stores sub-task lists derived from a main task.
- **AgentComponent**: Represents an agent handling tasks.

## Systems
- **TaskGenerationSystem**: Generates initial tasks from prompts.
- **SubTaskDivisionSystem**: Breaks tasks into smaller sub-tasks.
- **TaskAssignmentSystem**: Assigns sub-tasks to agents.
- **ResultAggregationSystem**: Aggregates results into a final package.
- **AgentManagement**: Manages dynamic addition and removal of agents.
- **TaskManager**: Manages tasks with different priority levels and dependencies.

## File Structure
"""

if __name__ == "__main__":
    main()

