from logs.logger import logger


class CloudSecurityManager:

    def __init__(self):

        self.sessions = {}

    def create_session(
            self,
            user_id):

        self.sessions[
            user_id
        ] = "ACTIVE"

        logger.info(
            f"Cloud session created: "
            f"{user_id}"
        )

    def revoke_session(
            self,
            user_id):

        if user_id in self.sessions:

            self.sessions[
                user_id
            ] = "REVOKED"

            logger.warning(
                f"Session revoked: "
                f"{user_id}"
            )

    def show_sessions(self):

        print(
            "\nCloud Security Manager:\n"
        )

        if not self.sessions:

            print(
                "No cloud sessions."
            )

            return

        for user_id, status in (
                self.sessions.items()):

            print(
                f"User: {user_id}"
            )

            print(
                f"Status: {status}"
            )

            print()