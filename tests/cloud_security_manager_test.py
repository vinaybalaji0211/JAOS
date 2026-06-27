from brain.cloud_security_manager import (
    CloudSecurityManager
)

manager = CloudSecurityManager()

manager.create_session(
    "vinay"
)

manager.create_session(
    "jarvis_admin"
)

manager.revoke_session(
    "jarvis_admin"
)

manager.show_sessions()