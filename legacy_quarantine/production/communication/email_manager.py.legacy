from logs.logger import logger


class EmailManager:

    def __init__(self):
        self.accounts = {}

    def register_account(
            self,
            provider,
            email,
            status="CONNECTED"):

        self.accounts[email] = {
            "provider": provider,
            "status": status
        }

        logger.info(
            f"Email account registered: {email}"
        )

    def show_accounts(self):

        print("\n=== Email Manager ===\n")

        if not self.accounts:
            print("No accounts registered.")
            return

        for email, data in self.accounts.items():

            print(email)
            print(f"  Provider : {data['provider']}")
            print(f"  Status   : {data['status']}")
            print()