from security.authentication_manager import (
    AuthenticationManager
)

manager = AuthenticationManager()

manager.register_method(
    "Vinay",
    "Password"
)

manager.register_method(
    "Admin",
    "System Token"
)

manager.show_methods()