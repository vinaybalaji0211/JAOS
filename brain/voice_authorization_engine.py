

class VoiceAuthorizationEngine:

    def __init__(self):

        self.permissions = {

            "AUTHOR": [
                "ALL"
            ],

            "TRUSTED": [
                "VIEW",
                "NORMAL_COMMANDS"
            ],

            "UNKNOWN": [
                "PUBLIC"
            ],

            "BLOCKED": []
        }

    def authorize(
            self,
            role,
            permission):

        allowed = self.permissions.get(
            role,
            []
        )

        if "ALL" in allowed:
            return True

        return permission in allowed

    def show_authorization(
            self,
            role,
            permission):

        result = self.authorize(
            role,
            permission
        )

        print(
            "\nVoice Authorization Engine:\n"
        )

        print(
            f"Role: {role}"
        )

        print(
            f"Permission: {permission}"
        )

        print(
            f"Authorized: {result}"
        )