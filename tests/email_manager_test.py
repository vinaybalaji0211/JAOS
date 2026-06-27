from communication.email_manager import EmailManager

manager = EmailManager()

manager.register_account(
    "Gmail",
    "vinay@example.com"
)

manager.register_account(
    "Outlook",
    "work@example.com",
    "DISCONNECTED"
)

manager.show_accounts()