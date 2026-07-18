from enum import Enum


class ToolCapability(str, Enum):
    FILESYSTEM_READ = "filesystem.read"
    FILESYSTEM_WRITE = "filesystem.write"
    FILESYSTEM_COPY = "filesystem.copy"
    FILESYSTEM_MOVE = "filesystem.move"
    FILESYSTEM_RENAME = "filesystem.rename"
    FILESYSTEM_DELETE = "filesystem.delete"
    FILESYSTEM_SEARCH = "filesystem.search"

    WINDOWS_LAUNCH = "windows.launch"
    WINDOWS_CLOSE = "windows.close"
    WINDOWS_CLIPBOARD = "windows.clipboard"
    WINDOWS_NOTIFICATIONS = "windows.notifications"
    WINDOWS_PROCESS = "windows.process"

    BROWSER_OPEN = "browser.open"
    BROWSER_SEARCH = "browser.search"
    BROWSER_TABS = "browser.tabs"
    BROWSER_DOWNLOAD = "browser.download"
    BROWSER_COOKIES = "browser.cookies"

    DEVELOPMENT_GIT = "development.git"
    DEVELOPMENT_BUILD = "development.build"
    DEVELOPMENT_RUN = "development.run"
    DEVELOPMENT_DEBUG = "development.debug"

    COMMUNICATION_EMAIL = "communication.email"
    COMMUNICATION_CALENDAR = "communication.calendar"
    COMMUNICATION_CONTACTS = "communication.contacts"