from logs.logger import logger


class AgentConflictResolver:

    def __init__(self):

        self.conflicts = []

    def report_conflict(
            self,
            agent_a,
            agent_b,
            issue):

        conflict = {
            "agent_a": agent_a,
            "agent_b": agent_b,
            "issue": issue,
            "status": "OPEN"
        }

        self.conflicts.append(
            conflict
        )

        logger.info(
            f"Conflict detected: "
            f"{agent_a} vs {agent_b}"
        )

    def resolve_conflict(
            self,
            issue):

        for conflict in self.conflicts:

            if conflict["issue"] == issue:

                conflict["status"] = (
                    "RESOLVED"
                )

                logger.info(
                    f"Conflict resolved: "
                    f"{issue}"
                )

    def show_conflicts(self):

        print(
            "\nAgent Conflict Resolver:\n"
        )

        if not self.conflicts:

            print(
                "No conflicts."
            )

            return

        for conflict in self.conflicts:

            print(
                f"Agent A: "
                f"{conflict['agent_a']}"
            )

            print(
                f"Agent B: "
                f"{conflict['agent_b']}"
            )

            print(
                f"Issue: "
                f"{conflict['issue']}"
            )

            print(
                f"Status: "
                f"{conflict['status']}"
            )

            print()