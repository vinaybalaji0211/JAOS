from logs.logger import logger


class AgentMemorySyncManager:

    def __init__(self):

        self.sync_log = []

    def sync_agent(
            self,
            agent_name,
            memory_item):

        record = {
            "agent": agent_name,
            "memory": memory_item,
            "status": "SYNCED"
        }

        self.sync_log.append(
            record
        )

        logger.info(
            f"Memory synced to {agent_name}"
        )

    def show_sync_log(self):

        print(
            "\nAgent Memory Sync Manager:\n"
        )

        if not self.sync_log:

            print(
                "No sync records."
            )

            return

        for record in self.sync_log:

            print(
                f"Agent: {record['agent']}"
            )

            print(
                f"Memory: {record['memory']}"
            )

            print(
                f"Status: {record['status']}"
            )

            print()