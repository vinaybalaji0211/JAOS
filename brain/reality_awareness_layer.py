from logs.logger import logger


class RealityAwarenessLayer:

    @staticmethod
    def assess(
            task,
            hardware_level,
            internet_available,
            capability_available):

        issues = []

        feasible = True

        if hardware_level == "LOW":

            issues.append(
                "Limited hardware resources."
            )

        if not internet_available:

            issues.append(
                "Internet unavailable."
            )

        if not capability_available:

            issues.append(
                "Required capability missing."
            )

        if issues:

            feasible = False

        logger.info(
            f"Reality assessment completed. Feasible={feasible}"
        )

        return {

            "task": task,

            "feasible": feasible,

            "issues": issues

        }

    @staticmethod
    def show_assessment(
            task,
            hardware_level,
            internet_available,
            capability_available):

        result = RealityAwarenessLayer.assess(

            task,

            hardware_level,

            internet_available,

            capability_available

        )

        print("\nReality Assessment:")

        print(
            f"Task: {result['task']}"
        )

        print(
            f"Feasible: {result['feasible']}"
        )

        if result["issues"]:

            print("\nIssues:")

            for issue in result["issues"]:

                print(
                    f"- {issue}"
                )

        else:

            print(
                "No reality issues detected."
            )