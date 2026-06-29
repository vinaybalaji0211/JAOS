"""
JAOS IDE Exceptions

Phase 4 — JAOS-M-0033

Custom exceptions for development environment providers.
"""


class IDEError(Exception):
    """
    Base exception for development-layer errors.
    """


class IDEProviderError(IDEError):
    """
    Raised when an IDE provider fails.
    """


class IDEValidationError(IDEError):
    """
    Raised when IDE request validation fails.
    """