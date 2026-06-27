from logs.logger import logger


class StartupValidator:

    def __init__(self):

        self.required_services = []

        self.registered_services = {}

    def add_required_service(
            self,
            service):

        if service not in self.required_services:
            self.required_services.append(service)

    def register_service(
            self,
            service,
            enabled=True):

        self.registered_services[service] = enabled

        logger.info(
            f"Startup service registered: {service}"
        )

    def validate(self):

        print("\n========== STARTUP VALIDATOR ==========\n")

        missing = []

        disabled = []

        for service in self.required_services:

            if service not in self.registered_services:

                print(f"✗ Missing : {service}")

                missing.append(service)

                continue

            if not self.registered_services[service]:

                print(f"⚠ Disabled : {service}")

                disabled.append(service)

            else:

                print(f"✓ {service}")

        print()

        if not missing and not disabled:

            print("Startup validation PASSED.")

        else:

            print("Startup validation FAILED.")

            if missing:

                print("\nMissing Services:")

                for service in missing:

                    print(f" - {service}")

            if disabled:

                print("\nDisabled Services:")

                for service in disabled:

                    print(f" - {service}")