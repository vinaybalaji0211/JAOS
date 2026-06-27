from logs.logger import logger


class ScreenWorkflowRecorder:

    def __init__(self):

        self.workflows = {}

    def start_recording(
            self,
            workflow_name):

        self.workflows[
            workflow_name
        ] = []

        logger.info(
            f"Recording started: "
            f"{workflow_name}"
        )

    def record_step(
            self,
            workflow_name,
            step):

        if workflow_name not in self.workflows:

            return

        self.workflows[
            workflow_name
        ].append(
            step
        )

    def show_workflow(
            self,
            workflow_name):

        print(
            f"\nWorkflow: "
            f"{workflow_name}\n"
        )

        steps = self.workflows.get(
            workflow_name,
            []
        )

        if not steps:

            print(
                "No steps recorded."
            )

            return

        for index, step in enumerate(
                steps,
                start=1):

            print(
                f"{index}. {step}"
            )