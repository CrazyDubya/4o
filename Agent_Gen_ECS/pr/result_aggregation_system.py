from typing import Dict

from pr.agent_management import AgentComponent


class ResultAggregationSystem:
    def aggregate_results(self, results: Dict[AgentComponent, str]) -> str:
        final_result = "\n".join(results.values())
        return final_result
