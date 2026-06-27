import json
import os
from datetime import datetime

from logs.logger import logger


class ReasoningTraceLogger:

    FILE_PATH = "data/reasoning/reasoning_traces.json"

    @staticmethod
    def record(decision, reason):

        os.makedirs(
            "data/reasoning",
            exist_ok=True
        )

        traces = ReasoningTraceLogger.get_all()

        traces.append(
            {
                "timestamp": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "decision": decision,
                "reason": reason
            }
        )

        with open(
                ReasoningTraceLogger.FILE_PATH,
                "w",
                encoding="utf-8") as file:

            json.dump(
                traces,
                file,
                indent=4
            )

        logger.info(
            f"Reasoning trace recorded: {decision}"
        )

    @staticmethod
    def get_all():

        if not os.path.exists(
                ReasoningTraceLogger.FILE_PATH):

            return []

        with open(
                ReasoningTraceLogger.FILE_PATH,
                "r",
                encoding="utf-8") as file:

            try:

                return json.load(file)

            except:

                return []

    @staticmethod
    def show():

        traces = ReasoningTraceLogger.get_all()

        print("\nReasoning Traces:")

        if not traces:

            print("No reasoning traces found.")

        else:

            for index, trace in enumerate(
                    traces,
                    start=1):

                print(
                    f"{index}. [{trace['timestamp']}]"
                )

                print(
                    f"Decision: {trace['decision']}"
                )

                print(
                    f"Reason: {trace['reason']}"
                )