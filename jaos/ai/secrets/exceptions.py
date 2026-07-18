class SecretError(Exception):
    """
    Base exception for AI secret management errors.
    """


class SecretNotFoundError(SecretError):
    """
    Raised when a requested secret cannot be found.
    """


class SecretStoreError(SecretError):
    """
    Raised when a secret store fails.
    """