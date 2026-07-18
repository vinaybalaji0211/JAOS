from dataclasses import dataclass


@dataclass(frozen=True)
class SecretReference:
    """
    Safe reference to a secret.

    This stores the secret name, never the secret value.
    """

    name: str

    def __post_init__(self) -> None:
        normalized_name = self.name.strip().upper()

        if not normalized_name:
            raise ValueError("Secret reference name cannot be empty")

        object.__setattr__(self, "name", normalized_name)


@dataclass(frozen=True)
class SecretStatus:
    """
    Public status for a secret without exposing the secret value.
    """

    name: str
    exists: bool