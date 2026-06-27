from logs.logger import logger


class SpatialMemory:

    def __init__(self):

        self.locations = {}

    def remember_location(
            self,
            name,
            path,
            location_type="folder"):

        self.locations[name] = {
            "path": path,
            "type": location_type
        }

        logger.info(
            f"Spatial location remembered: {name}"
        )

    def get_location(
            self,
            name):

        return self.locations.get(name)

    def show_locations(self):

        print("\nSpatial Memory:\n")

        if not self.locations:

            print("No locations remembered.")

            return

        for name, details in self.locations.items():

            print(
                f"{name} | "
                f"Type: {details['type']} | "
                f"Path: {details['path']}"
            )