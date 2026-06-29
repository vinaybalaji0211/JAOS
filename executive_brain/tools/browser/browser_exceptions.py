"""
JAOS Browser Exceptions

Phase 4 — JAOS-M-0032

Custom exceptions for browser tools and browser providers.
"""


class BrowserError(Exception):
    """
    Base exception for browser-layer errors.
    """


class BrowserProviderError(BrowserError):
    """
    Raised when a browser provider fails.
    """


class BrowserValidationError(BrowserError):
    """
    Raised when browser request validation fails.
    """