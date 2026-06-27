from logs.logger import logger


class ResearchAgent:

    def __init__(self):

        self.name = "Research Agent"

        self.capabilities = [
            "web_research",
            "fact_checking",
            "market_research",
            "competitor_analysis",
            "news_summary",
            "research_report"
        ]

    def handle_task(
            self,
            task):

        task_lower = task.lower()

        if "fact" in task_lower or "verify" in task_lower:

            result = "Fact-checking task accepted."

        elif "market" in task_lower:

            result = "Market research task accepted."

        elif "competitor" in task_lower:

            result = "Competitor analysis task accepted."

        elif "news" in task_lower:

            result = "News summary task accepted."

        elif "report" in task_lower:

            result = "Research report task accepted."

        else:

            result = "General research task accepted."

        logger.info(
            f"{self.name} handled task."
        )

        return result

    def show_capabilities(self):

        print("\nResearch Agent:\n")

        for capability in self.capabilities:

            print(
                f"- {capability}"
            )