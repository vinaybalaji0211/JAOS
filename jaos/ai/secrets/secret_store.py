from abc import ABC, abstractmethod

from jaos.ai.secrets.secret_models import SecretReference, SecretStatus


class SecretStore(ABC):
    """
    Interface for secret storage backends.
    """

    @abstractmethod
    def get_secret(self, reference: SecretReference) -> str:
        """
        Return the secret value for a reference.
        """

    @abstractmethod
    def get_status(self, reference: SecretReference) -> SecretStatus:
        """
        Return public secret status without exposing the value.
        """