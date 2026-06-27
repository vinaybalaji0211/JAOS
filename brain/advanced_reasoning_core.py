from logs.logger import logger


class AdvancedReasoningCore:

    def __init__(self):

        self.reasoning_sessions = []

    def start_reasoning(
            self,
            goal,
            strategy):

        session = {
            "goal": goal,
            "strategy": strategy,
            "status": "IN_PROGRESS"
        }

        self.reasoning_sessions.append(session)

        logger.info(
            f"Reasoning started: {goal}"
        )

    def complete_reasoning(
            self,
            goal):

        for session in self.reasoning_sessions:

            if session["goal"] == goal:

                session["status"] = "COMPLETED"

                logger.info(
                    f"Reasoning completed: {goal}"
                )

    def show_sessions(self):

        print(
            "\nAdvanced Reasoning Core:\n"
        )

        if not self.reasoning_sessions:

            print("No reasoning sessions.")
            return

        for session in self.reasoning_sessions:

            print(f"Goal: {session['goal']}")
            print(f"Strategy: {session['strategy']}")
            print(f"Status: {session['status']}")
            print()