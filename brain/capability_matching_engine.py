from logs.logger import logger


class CapabilityMatchingEngine:

    @staticmethod
    def match(required_capabilities, available_capabilities):

        matched = []

        missing = []

        for capability in required_capabilities:

            if capability in available_capabilities:

                matched.append(capability)

            else:

                missing.append(capability)

        logger.info(
            "Capability matching completed."
        )

        return {
            "matched": matched,
            "missing": missing
        }

    @staticmethod
    def show_match(required_capabilities, available_capabilities):

        result = CapabilityMatchingEngine.match(
            required_capabilities,
            available_capabilities
        )

        print("\nCapability Matching Result:")

        print("\nMatched:")

        if not result["matched"]:

            print("No matched capabilities.")

        else:

            for item in result["matched"]:

                print(f"- {item}")

        print("\nMissing:")

        if not result["missing"]:

            print("No missing capabilities.")

        else:

            for item in result["missing"]:

                print(f"- {item}")