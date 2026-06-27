from logs.logger import logger


class AgentCollaborationEngine:

    def __init__(self):

        self.agents = {

            "Safety Agent": {
                "status": "ACTIVE",
                "busy": False,
                "priority": 1,
                "capabilities": [
                    "safety",
                    "permissions"
                ]
            },

            "Planner Agent": {
                "status": "ACTIVE",
                "busy": False,
                "priority": 2,
                "capabilities": [
                    "planning",
                    "decomposition"
                ]
            },

            "Memory Agent": {
                "status": "ACTIVE",
                "busy": False,
                "priority": 3,
                "capabilities": [
                    "memory_search",
                    "context"
                ]
            },

            "Provider Agent": {
                "status": "ACTIVE",
                "busy": False,
                "priority": 4,
                "capabilities": [
                    "provider_selection"
                ]
            },

            "Tool Agent": {
                "status": "ACTIVE",
                "busy": False,
                "priority": 5,
                "capabilities": [
                    "tool_discovery"
                ]
            },

            "Reflection Agent": {
                "status": "ACTIVE",
                "busy": False,
                "priority": 6,
                "capabilities": [
                    "feedback",
                    "self_improvement"
                ]
            }
        }

    def show_agents(self):

        print("\nAgents:\n")

        for name, details in self.agents.items():

            print(
                f"{name} | "
                f"Priority={details['priority']} | "
                f"Status={details['status']} | "
                f"Busy={details['busy']} | "
                f"Capabilities={details['capabilities']}"
            )

    def collaborate(self, goal):

        print("\nAgent Collaboration Flow:\n")

        order = sorted(
            self.agents.items(),
            key=lambda item: item[1]["priority"]
        )

        for agent, details in order:

            print(
                f"{agent} working on goal: {goal}"
            )

        logger.info(
            "Agent collaboration completed."
        )