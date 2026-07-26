"""Context trust levels for the JAOS AI Intelligence Platform."""

from enum import Enum, unique


@unique
class ContextTrustLevel(str, Enum):
    """Classifies context by authority and trust source."""

    TRUSTED_SYSTEM = "trusted_system"
    TRUSTED_INTERNAL = "trusted_internal"
    USER_PROVIDED = "user_provided"
    RETRIEVED_MEMORY = "retrieved_memory"
    EXTERNAL_UNTRUSTED = "external_untrusted"