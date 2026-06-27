from logs.logger import logger


class HumanMemoryLayer:

    def __init__(self):

        self.people = {}

    def remember(
            self,
            person,
            category,
            information):

        if person not in self.people:

            self.people[person] = {}

        if category not in self.people[person]:

            self.people[person][category] = []

        self.people[person][category].append(
            information
        )

        logger.info(
            f"Memory stored for {person}"
        )

    def recall(
            self,
            person):

        return self.people.get(
            person,
            {}
        )

    def show_person(
            self,
            person):

        print(f"\nHuman Memory: {person}\n")

        memory = self.recall(
            person
        )

        if not memory:

            print(
                "No memories."
            )

            return

        for category, items in memory.items():

            print(
                f"{category}:"
            )

            for item in items:

                print(
                    f"  - {item}"
                )