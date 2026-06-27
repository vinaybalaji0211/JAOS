from logs.logger import logger


class ObjectRegistry:

    def __init__(self):

        self.objects = {}

    def register(
            self,
            object_id,
            object_type,
            properties=None):

        if properties is None:
            properties = {}

        self.objects[object_id] = {

            "type": object_type,

            "properties": properties

        }

        logger.info(
            f"Registered {object_id}"
        )

    def get(
            self,
            object_id):

        return self.objects.get(
            object_id
        )

    def show_registry(self):

        print("\nObject Registry:\n")

        if not self.objects:

            print(
                "Registry empty."
            )

            return

        for object_id, obj in self.objects.items():

            print(
                f"ID: {object_id}"
            )

            print(
                f"Type: {obj['type']}"
            )

            print(
                f"Properties: {obj['properties']}"
            )

            print()