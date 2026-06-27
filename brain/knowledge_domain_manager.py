from logs.logger import logger


class KnowledgeDomainManager:

    def __init__(self):

        self.domains = {}

    def add_domain(
            self,
            domain_name,
            description=""):

        self.domains[domain_name] = {
            "description": description,
            "topics": []
        }

        logger.info(
            f"Knowledge domain added: {domain_name}"
        )

    def add_topic(
            self,
            domain_name,
            topic):

        if domain_name not in self.domains:

            self.add_domain(
                domain_name
            )

        self.domains[
            domain_name
        ]["topics"].append(
            topic
        )

        logger.info(
            f"Topic added to {domain_name}: {topic}"
        )

    def show_domains(self):

        print("\nKnowledge Domain Manager:\n")

        if not self.domains:

            print("No knowledge domains.")

            return

        for domain, details in self.domains.items():

            print(f"Domain: {domain}")

            print(
                f"Description: "
                f"{details['description']}"
            )

            print(
                f"Topics: "
                f"{details['topics']}"
            )

            print()