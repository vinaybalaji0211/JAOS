class VersionManager:

    VERSION = "0.1"

    PHASE = "Phase 1"

    BUILD = "Core Foundation"

    @staticmethod
    def show_version():

        print("\nJARVIS OS Version Information\n")

        print(
            f"Version : {VersionManager.VERSION}"
        )

        print(
            f"Phase   : {VersionManager.PHASE}"
        )

        print(
            f"Build   : {VersionManager.BUILD}"
        )