from logs.logger import logger


class FileSystemManager:

    def __init__(self):

        self.files = {}

    def register_file(
            self,
            file_name,
            location,
            file_type):

        self.files[file_name] = {
            "location": location,
            "type": file_type
        }

        logger.info(
            f"Registered file: {file_name}"
        )

    def get_file(
            self,
            file_name):

        return self.files.get(
            file_name
        )

    def show_files(self):

        print(
            "\n=== File System Manager ===\n"
        )

        if not self.files:

            print(
                "No files registered."
            )

            return

        for name, data in self.files.items():

            print(name)

            print(
                f"  Location : {data['location']}"
            )

            print(
                f"  Type     : {data['type']}"
            )

            print()