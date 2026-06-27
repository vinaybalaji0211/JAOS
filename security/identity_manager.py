from logs.logger import logger


class IdentityManager:

    def __init__(self):

        self.identities = {}

    def register_identity(
            self,
            username,
            identity_type="LOCAL",
            status="ACTIVE"):

        self.identities[username] = {
            "type": identity_type,
            "status": status
        }

        logger.info(
            f"Identity registered: {username}"
        )

    def show_identities(self):

        print("\n=== Identity Manager ===\n")

        if not self.identities:

            print("No identities.")
            return

        for username, data in self.identities.items():

            print(username)
            print(f"  Type   : {data['type']}")
            print(f"  Status : {data['status']}")
            print()