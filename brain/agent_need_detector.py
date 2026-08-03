

class AgentNeedDetector:

    def __init__(self):

        self.known_domains = {
            "code": "Coding Agent",
            "research": "Research Agent",
            "memory": "Memory Agent",
            "document": "Document Agent",
            "email": "Email Agent",
            "calendar": "Calendar Agent",
            "vision": "Vision Agent",
            "security": "Security Agent"
        }

    def analyze_request(
            self,
            request):

        request = request.lower()

        for domain, agent in (
                self.known_domains.items()):

            if domain in request:

                return {
                    "new_agent_needed": False,
                    "recommended_agent": agent
                }

        return {
            "new_agent_needed": True,
            "recommended_agent":
            f"Custom Agent for: {request}"
        }

    def show_analysis(
            self,
            request):

        result = self.analyze_request(
            request
        )

        print(
            "\nAgent Need Detector:\n"
        )

        print(
            f"Request: {request}"
        )

        print(
            f"New Agent Needed: "
            f"{result['new_agent_needed']}"
        )

        print(
            f"Recommendation: "
            f"{result['recommended_agent']}"
        )