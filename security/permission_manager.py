from logs.logger import logger


class PermissionManager:

    def __init__(self):

        self.permissions = {}

    def grant_permission(
            self,
            username,
            permission):

        self.permissions.setdefault(username, set()).add(permission)

        logger.info(
            f"Permission granted: {username} -> {permission}"
        )

    def has_permission(
            self,
            username,
            permission):

        return permission in self.permissions.get(username, set())

    def show_permissions(self):

        print("\n=== Permission Manager ===\n")

        if not self.permissions:

            print("No permissions assigned.")
            return

        for username, perms in self.permissions.items():

            print(username)

            for permission in sorted(perms):

                print(f"  - {permission}")

            print()