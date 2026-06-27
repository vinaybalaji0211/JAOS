from logs.logger import logger


class APIIntelligenceManager:

    def __init__(self):

        self.apis = {}

    def register_api(
            self,
            name,
            status,
            quota,
            api_type):

        self.apis[name] = {
            "status": status,
            "quota": quota,
            "type": api_type
        }

        logger.info(
            f"API Registered: {name}"
        )

    def api_status(
            self,
            name):

        return self.apis.get(name)

    def show_apis(self):

        print("\n=== API Intelligence Manager ===\n")

        if not self.apis:

            print("No APIs registered.")
            return

        for name, api in self.apis.items():

            print(f"{name}")

            print(
                f"  Type   : {api['type']}"
            )

            print(
                f"  Status : {api['status']}"
            )

            print(
                f"  Quota  : {api['quota']}"
            )

            print()