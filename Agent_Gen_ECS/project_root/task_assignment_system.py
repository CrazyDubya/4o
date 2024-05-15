from typing import List, Dict
from task_manager import TaskComponent, SubTaskComponent
from agent_management import AgentComponent

class TaskAssignmentSystem:
    def assign_tasks(self, subtask_component: SubTaskComponent, agents: List[AgentComponent]) -> Dict[AgentComponent, TaskComponent]:
        assignments = {}
        for i, subtask in enumerate(subtask_component.subtasks):
            agent = agents[i % len(agents)]
            assignments[agent] = subtask
        return assignments
