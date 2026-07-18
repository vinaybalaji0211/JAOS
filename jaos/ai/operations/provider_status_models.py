from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderOperationalStatus:
    """
    Public operational status for an AI provider.

    This model never exposes secret values.
    """

    name: str
    configured: bool
    enabled: bool
    is_default: bool
    secret_required: bool
    secret_present: bool
    current_model: str | None = None