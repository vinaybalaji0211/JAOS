from jaos.ai.identity.capability_registry import CapabilityRegistry
from jaos.ai.identity.identity_models import JAOSIdentity
from jaos.ai.identity.limitation_registry import LimitationRegistry


class IdentityManager:
    """
    Builds the canonical runtime identity for JAOS.
    """

    def __init__(
        self,
        capability_registry: CapabilityRegistry | None = None,
        limitation_registry: LimitationRegistry | None = None,
    ) -> None:
        self.capability_registry = capability_registry or CapabilityRegistry()
        self.limitation_registry = limitation_registry or LimitationRegistry()

    def get_identity(self) -> JAOSIdentity:
        return JAOSIdentity(
            name="JAOS",
            version="v0.7.0-alpha",
            codename="Jarvis Artificial Operating System",
            description=(
                "JAOS is a modular AI Operating System designed to understand "
                "intent, reason about tasks, coordinate tools, and execute "
                "approved actions safely."
            ),
            capabilities=self.capability_registry.list_capabilities(),
            limitations=self.limitation_registry.list_limitations(),
        )