from security.identity_manager import IdentityManager

manager = IdentityManager()

manager.register_identity(
    "Vinay"
)

manager.register_identity(
    "Admin",
    "SYSTEM"
)

manager.show_identities()