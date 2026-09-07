from logs.logger import logger


class KernelPermissionGateway:

    def __init__(self):

        self.permissions = {}

    def grant_permission(
            self,
            action):

        self.permissions[action] = True

        logger.info(
            f"Permission granted: {action}"
        )

    def revoke_permission(
            self,
            action):

        self.permissions[action] = False

        logger.info(
            f"Permission revoked: {action}"
        )

    def is_allowed(
            self,
            action):

        return self.permissions.get(
            action,
            False
        )

    def show_permissions(self):

        print("\n========== PERMISSION GATEWAY ==========\n")

        if not self.permissions:

            print("No permissions registered.")
            return

        for action, allowed in self.permissions.items():

            print(f"{action}")

            print(f"  Allowed : {allowed}")

            print()