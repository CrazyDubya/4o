
class TaskComponent:
    def __init__(self, description, prompts):
        self.description = description
        self.prompts = prompts
        self.results = []

class SubTaskComponent:
    def __init__(self, task, dependencies):
        self.task = task
        self.dependencies = dependencies
        self.results = None

class AgentComponent:
    def __init__(self, agent_id, status):
        self.agent_id = agent_id
        self.status = status
        self.results = None
