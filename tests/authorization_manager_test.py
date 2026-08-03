from security.authorization_manager import AuthorizationManager

manager = AuthorizationManager()

manager.register_role(
    "Vinay",
    "USER"
)

manager.register_role(
    "Admin",
    "SYSTEM"
)

manager.show_roles()

print()

print(
    "Vinay USER:",
    manager.is_authorized(
        "Vinay",
        "USER"
    )
)

print(
    "Vinay ADMIN:",
    manager.is_authorized(
        "Vinay",
        "ADMIN"
    )
)