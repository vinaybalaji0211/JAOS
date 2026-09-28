from logs.logger import logger


class PermissionSystem:

    def __init__(self):

        self.permissions = {
            "read_file": True,
            "write_file": True,
            "delete_file": False,
            "system_command": False,
            "device_control": False,
            "web_access": False
        }

    def is_allowed(self, action):

        allowed = self.permissions.get(
            action,
            False
        )

        logger.info(
            f"Permission checked: {action} = {allowed}"
        )

        return allowed

    def show_permissions(self):

        print("\nPermissions:")

        for action, allowed in self.permissions.items():

            print(f"{action}: {allowed}")