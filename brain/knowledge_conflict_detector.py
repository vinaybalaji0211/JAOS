from logs.logger import logger


class KnowledgeConflictDetector:

    @staticmethod
    def detect(conflict_pairs):

        conflicts = []

        for pair in conflict_pairs:

            source_1 = pair["source_1"]
            source_2 = pair["source_2"]

            value_1 = pair["value_1"]
            value_2 = pair["value_2"]

            if value_1 != value_2:

                conflicts.append(

                    {
                        "source_1": source_1,
                        "source_2": source_2,
                        "value_1": value_1,
                        "value_2": value_2
                    }

                )

        logger.info(
            f"Knowledge conflicts detected: {len(conflicts)}"
        )

        return conflicts

    @staticmethod
    def show_conflicts(conflict_pairs):

        conflicts = (
            KnowledgeConflictDetector.detect(
                conflict_pairs
            )
        )

        print("\nKnowledge Conflict Report:\n")

        if not conflicts:

            print(
                "No conflicts detected."
            )

            return

        for index, conflict in enumerate(
                conflicts,
                start=1):

            print(
                f"{index}. Conflict:"
            )

            print(
                f"   {conflict['source_1']} = {conflict['value_1']}"
            )

            print(
                f"   {conflict['source_2']} = {conflict['value_2']}"
            )

            print()