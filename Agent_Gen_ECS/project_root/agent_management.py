class AgentComponent:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id

class AgentManagement:
    def __init__(self):
        self.agents = []

    def add_agent(self, agent_id: str) -> AgentComponent:
        agent = AgentComponent(agent_id)
        self.agents.append(agent)
        return agent

    def remove_agent(self, agent_id: str):
        self.agents = [agent for agent in self.agents if agent.agent_id != agent_id]
