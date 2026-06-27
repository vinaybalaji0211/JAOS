from logs.logger import logger


class TaskPriorityManager:

    @staticmethod
    def calculate_priority(
            urgency,
            importance,
            safety,
            goal_relevance):

        score = (
            urgency +
            importance +
            safety +
            goal_relevance
        )

        logger.info(
            f"Task priority calculated: {score}"
        )

        return score

    @staticmethod
    def rank_tasks(tasks):

        ranked_tasks = []

        for task in tasks:

            score = TaskPriorityManager.calculate_priority(
                task["urgency"],
                task["importance"],
                task["safety"],
                task["goal_relevance"]
            )

            ranked_tasks.append(
                {
                    "task": task["task"],
                    "score": score
                }
            )

        ranked_tasks.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        logger.info(
            "Tasks ranked by priority."
        )

        return ranked_tasks

    @staticmethod
    def show_ranked_tasks(tasks):

        ranked_tasks = TaskPriorityManager.rank_tasks(
            tasks
        )

        print("\nRanked Tasks:")

        for index, task in enumerate(
                ranked_tasks,
                start=1):

            print(
                f"{index}. {task['task']} "
                f"| Priority Score: {task['score']}"
            )