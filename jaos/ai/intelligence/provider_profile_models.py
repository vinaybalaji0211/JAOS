from dataclasses import dataclass
from enum import Enum


class ProviderCostType(str, Enum):
    FREE = "free"
    PAID = "paid"
    FREE_AND_PAID = "free_and_paid"
    UNKNOWN = "unknown"


class ProviderPrivacyType(str, Enum):
    LOCAL_PRIVATE = "local_private"
    CLOUD = "cloud"
    HYBRID = "hybrid"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class ProviderProfile:
    """
    Describes what an AI provider is useful for.

    This is not a secret/config object. It stores public knowledge
    used for routing, recommendations, and future provider selection.
    """

    name: str
    display_name: str
    description: str
    cost_type: ProviderCostType
    privacy_type: ProviderPrivacyType
    strengths: tuple[str, ...]
    limitations: tuple[str, ...]
    recommended_for: tuple[str, ...]