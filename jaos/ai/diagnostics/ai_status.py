from jaos.ai.diagnostics.models import DiagnosticStatus
from jaos.ai.provider import ProviderManager


class AIStatusProvider:
    """
    Reports overall AI Platform status.
    """

    def __init__(self, provider_manager: ProviderManager) -> None:
        self.provider_manager = provider_manager

    def get_status(self) -> DiagnosticStatus:
        provider_count = self.provider_manager.count()

        try:
            default_provider = self.provider_manager.get_default_provider_name()
        except Exception:
            default_provider = None

        return DiagnosticStatus(
            component="AI Platform",
            healthy=True,
            message="AI Platform is online.",
            details={
                "provider_count": provider_count,
                "default_provider": default_provider,
                "providers": self.provider_manager.list_provider_names(),
            },
        )