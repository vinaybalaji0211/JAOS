from jaos.ai.secrets.environment_secret_store import EnvironmentSecretStore
from jaos.ai.secrets.secret_models import SecretReference, SecretStatus
from jaos.ai.secrets.secret_store import SecretStore


class SecretManager:
    """
    Public interface for retrieving provider secrets safely.

    SecretManager returns secret values only to trusted provider code.
    CLI/status paths should use get_status instead.
    """

    def __init__(self, store: SecretStore | None = None) -> None:
        self._store = store or EnvironmentSecretStore()

    def get_secret(self, name: str) -> str:
        return self._store.get_secret(SecretReference(name))

    def get_status(self, name: str) -> SecretStatus:
        return self._store.get_status(SecretReference(name))

    def has_secret(self, name: str) -> bool:
        return self.get_status(name).exists