import json
import os
from datetime import datetime

from logs.logger import logger


class CrashRecoverySystem:

    FILE_PATH = "data/recovery/crash_checkpoint.json"

    @staticmethod
    def save_checkpoint(
            last_state,
            last_task,
            last_goal,
            crash_reason="None"):

        os.makedirs(
            "data/recovery",
            exist_ok=True
        )

        checkpoint = {
            "last_state": last_state,
            "last_task": last_task,
            "last_goal": last_goal,
            "crash_reason": crash_reason,
            "recovery_time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        with open(
                CrashRecoverySystem.FILE_PATH,
                "w",
                encoding="utf-8") as file:

            json.dump(
                checkpoint,
                file,
                indent=4
            )

        logger.info(
            "Crash recovery checkpoint saved."
        )

    @staticmethod
    def load_checkpoint():

        if not os.path.exists(
                CrashRecoverySystem.FILE_PATH):

            return None

        with open(
                CrashRecoverySystem.FILE_PATH,
                "r",
                encoding="utf-8") as file:

            return json.load(file)

    @staticmethod
    def show_checkpoint():

        checkpoint = CrashRecoverySystem.load_checkpoint()

        print("\nCrash Recovery Checkpoint:\n")

        if not checkpoint:

            print("No checkpoint found.")

            return

        for key, value in checkpoint.items():

            print(f"{key}: {value}")