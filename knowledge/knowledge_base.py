from logs.logger import logger


class KnowledgeBase:

    def __init__(self):

        self.entries = {}

    def add_entry(
            self,
            topic,
            content):

        self.entries[topic] = content

        logger.info(
            f"Knowledge entry added: {topic}"
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