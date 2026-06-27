from logs.logger import logger


class TaskDecomposer:

    KEYWORDS = {

        "build": [

            "Plan",

            "Design",

            "Implement",

            "Test",

            "Deploy"

        ],

        "learn": [

            "Research",

            "Study",

            "Practice",

            "Review"

        ],

        "train": [

            "Prepare data",

            "Train model",

            "Evaluate model"

        ]

    }

    @staticmethod
    def decompose(goal):

        goal_lower = goal.lower()

        tasks = []

        for keyword, subtasks in TaskDecomposer.KEYWORDS.items():

            if keyword in goal_lower:

                tasks.extend(subtasks)

        if not tasks:

            tasks.append(

                "Manual decomposition required"

            )

        logger.info(

            f"Goal decomposed into {len(tasks)} tasks"

        )

        return tasks

    @staticmethod
    def show_tasks(goal):

        tasks = TaskDecomposer.decompose(

            goal

        )

        print(

            f"\nTask Breakdown for:\n{goal}\n"

        )

        for index, task in enumerate(

                tasks,

                start=1):

            print(

                f"{index}. {task}"

            )