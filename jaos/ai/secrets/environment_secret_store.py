import os

from jaos.ai.secrets.exceptions import SecretNotFoundError
from jaos.ai.secrets.secret_models import SecretReference, SecretStatus
from jaos.ai.secrets.secret_store import SecretStore


class EnvironmentSecretStore(SecretStore):
    """
    Reads secrets from environment variables.

    This store never logs or exposes secret values.
    """

    def get_secret(self, reference: SecretReference) -> str:
        value = os.getenv(reference.name)

        if value is None or not value.strip():
            raise SecretNotFoundError(f"Secret not found: {reference.name}")

        return value

    def get_status(self, reference: SecretReference) -> SecretStatus:
        value = os.getenv(reference.name)

        return SecretStatus(
            name=reference.name,
            exists=value is not None and bool(value.strip()),
        )