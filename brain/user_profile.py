import json
import os

from logs.logger import logger


class UserProfile:

    FILE_PATH = "data/profile/user_profile.json"

    @staticmethod
    def save(profile):

        os.makedirs(
            "data/profile",
            exist_ok=True
        )

        with open(
                UserProfile.FILE_PATH,
                "w",
                encoding="utf-8") as file:

            json.dump(
                profile,
                file,
                indent=4
            )

        logger.info(
            "User profile saved."
        )

    @staticmethod
    def load():

        if not os.path.exists(
                UserProfile.FILE_PATH):

            return {}

        with open(
                UserProfile.FILE_PATH,
                "r",
                encoding="utf-8") as file:

            return json.load(file)

    @staticmethod
    def show():

        profile = UserProfile.load()

        print("\nUser Profile:")

        if not profile:

            print(
                "No profile available."
            )

        else:

            for key, value in profile.items():

                print(
                    f"{key}: {value}"
                )