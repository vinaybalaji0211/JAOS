from logs.logger import logger


class SecurityLockdownMode:

    def __init__(self):

        self.mode = "NORMAL"

        self.plugins_enabled = True

        self.agents_enabled = True

        self.commands_enabled = True

        self.secrets_locked = False

        self.memory_locked = False

    def enter_lockdown(self):

        self.mode = "LOCKDOWN"

        self.plugins_enabled = False

        self.agents_enabled = False

        self.commands_enabled = False

        self.secrets_locked = True

        self.memory_locked = True

        logger.warning(
            "SYSTEM ENTERED LOCKDOWN MODE"
        )

    def enter_recovery(self):

        self.mode = "RECOVERY"

        logger.info(
            "Recovery mode activated."
        )

    def reset_normal(self):

        self.mode = "NORMAL"

        self.plugins_enabled = True

        self.agents_enabled = True

        self.commands_enabled = True

        self.secrets_locked = False

        self.memory_locked = False

        logger.info(
            "System restored to NORMAL mode."
        )

    def show_status(self):

        print("\nSecurity Lockdown Mode:\n")

        print(
            f"Mode: {self.mode}"
        )

        print(
            f"Plugins Enabled: {self.plugins_enabled}"
        )

        print(
            f"Agents Enabled: {self.agents_enabled}"
        )

        print(
            f"Commands Enabled: {self.commands_enabled}"
        )

        print(
            f"Secrets Locked: {self.secrets_locked}"
        )

        print(
            f"Memory Locked: {self.memory_locked}"
        )