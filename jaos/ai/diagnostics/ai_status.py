from jaos.ai.diagnostics.models import DiagnosticStatus
from jaos.ai.provider import ProviderManager
from jaos.ai.provider.health import AIProviderHealthStatus


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

        healthy = False
        message = "AI Platform has no registered providers."

        if default_provider is not None:
            try:
                health = self.provider_manager.health_check(default_provider)
                healthy = health.status == AIProviderHealthStatus.HEALTHY
                message = (
                    "AI Platform is online."
                    if healthy
                    else f"AI Platform default provider is {health.status.value}."
                )
            except Exception as exc:
                message = f"AI Platform default provider health check failed: {exc}"

        return DiagnosticStatus(
            component="AI Platform",
            healthy=healthy,
            message=message,
            details={
                "provider_count": provider_count,
                "default_provider": default_provider,
                "providers": self.provider_manager.list_provider_names(),
            },
        )