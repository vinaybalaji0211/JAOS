from pc_control.browser_controller import (
    BrowserController
)

browser = BrowserController()

browser.register_session(
    "Chrome",
    "https://github.com"
)

browser.register_session(
    "Chrome",
    "https://chat.openai.com"
)

browser.register_session(
    "Edge",
    "https://mail.google.com"
)

browser.show_sessions()