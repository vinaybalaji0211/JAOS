from jaos_platform.base_platform_service import BasePlatformService
from logs.logger import logger


class KnowledgeBase(BasePlatformService):
    """Runtime-managed JAOS knowledge base service."""

    SERVICE_NAME = "knowledge_base"

    def __init__(self, runtime=None):
        self.entries = {}

        super().__init__(runtime)

    def add_entry(self, topic, content):
        self.entries[topic] = content

        logger.info(f"Knowledge entry added: {topic}")

        if self.runtime is not None:
            self.runtime.events.publish(
                "knowledge_entry_added",
                {
                    "topic": topic,
                    "content": content,
                },
            )

    def show_entries(self):
        print("\n=== Knowledge Base ===\n")

        if not self.entries:
            print("No knowledge entries.")
            return

        for topic, content in self.entries.items():
            print(topic)
            print(f"  Content : {content}")
            print()