from jaos.ai.operations.provider_status_models import ProviderOperationalStatus
from jaos.ai.provider import ProviderManager
from jaos.ai.secrets import SecretManager


class ProviderStatusService:
    """
    Builds operational status views for AI providers.

    Combines provider configuration, runtime state, default provider,
    and secret availability without exposing secret values.
    """

    def __init__(
        self,
        provider_manager: ProviderManager,
        secret_manager: SecretManager | None = None,
    ) -> None:
        self.provider_manager = provider_manager
        self.secret_manager = secret_manager or SecretManager()

    def get_provider_status(self, name: str) -> ProviderOperationalStatus:
        config = self.provider_manager.get_config(name)
        state = self.provider_manager.get_state(name)
        default_provider_name = self._safe_default_provider_name()

        secret_required = config.requires_secrets()
        secret_present = all(
            self.secret_manager.has_secret(secret_ref)
            for secret_ref in config.secret_refs
        )

        return ProviderOperationalStatus(
            name=config.name,
            configured=True,
            enabled=config.enabled and state.enabled,
            is_default=config.name == default_provider_name,
            secret_required=secret_required,
            secret_present=True if not secret_required else secret_present,
            current_model=state.current_model,
        )

    def list_provider_statuses(self) -> tuple[ProviderOperationalStatus, ...]:
        return tuple(
            self.get_provider_status(provider_name)
            for provider_name in self.provider_manager.list_provider_names()
        )

    def _safe_default_provider_name(self) -> str | None:
        try:
            return self.provider_manager.get_default_provider_name()
        except Exception:
            return None