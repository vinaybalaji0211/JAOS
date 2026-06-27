from core.session_manager import SessionManager


session = SessionManager()

session.add_event(
    "JARVIS OS started"
)

session.add_event(
    "Capability registry checked"
)

session.show_session()