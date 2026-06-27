from logs.logger import logger


class CapabilityTruthEngine:

    def __init__(self):

        self.capabilities = {}

    def register_capability(
            self,
            name,
            platform,
            available,
            version,
            notes=""):

        self.capabilities[name] = {

            "platform": platform,

            "available": available,

            "version": version,

            "notes": notes

        }

        logger.info(
            f"Capability registered: {name}"
        )

    def can_execute(
            self,
            capability):

        return self.capabilities.get(capability)

    def show_capabilities(self):

        print("\n========== CAPABILITY TRUTH ENGINE ==========\n")

        if not self.capabilities:

            print("No capabilities registered.")
            return

        for name, data in self.capabilities.items():

            print(name)

            print(f"  Platform : {data['platform']}")

            print(f"  Available: {data['available']}")

            print(f"  Version  : {data['version']}")

            print(f"  Notes    : {data['notes']}")

            print()