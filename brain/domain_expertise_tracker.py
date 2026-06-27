from logs.logger import logger


class DomainExpertiseTracker:

    def __init__(self):

        self.domains = {}

    def update_expertise(
            self,
            domain,
            score):

        self.domains[domain] = score

        logger.info(
            f"Expertise updated: "
            f"{domain}"
        )

    def get_expertise(
            self,
            domain):

        return self.domains.get(
            domain,
            0
        )

    def show_expertise(self):

        print(
            "\nDomain Expertise Tracker:\n"
        )

        if not self.domains:

            print(
                "No expertise recorded."
            )

            return

        for domain, score in (
                self.domains.items()):

            print(
                f"{domain}: {score}%"
            )