from logs.logger import logger


class KernelRouter:

    def __init__(self):

        self.routes = {}

    def register_route(
            self,
            event_type,
            destination):

        self.routes[event_type] = destination

        logger.info(
            f"Route registered: {event_type} -> {destination}"
        )

    def resolve_route(
            self,
            event_type):

        return self.routes.get(
            event_type,
            "UNREGISTERED"
        )

    def show_routes(self):

        print("\n========== KERNEL ROUTER ==========\n")

        if not self.routes:

            print("No routes registered.")
            return

        for event, destination in self.routes.items():

            print(f"{event}")

            print(f"  Destination : {destination}")

            print()