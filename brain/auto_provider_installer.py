from brain.provider_router import ProviderRouter
from logs.logger import logger


class AutoProviderInstaller:

    @staticmethod
    def install_provider(
            name,
            provider_type,
            capabilities,
            priority=5,
            approved=False):

        if not approved:

            logger.warning(
                f"Provider installation blocked. Approval required: {name}"
            )

            print(
                f"Installation blocked for {name}. Approval required."
            )

            return False

        router = ProviderRouter()

        router.register_provider(
            name,
            provider_type,
            capabilities,
            priority
        )

        logger.info(
            f"Provider installed: {name}"
        )

        print(
            f"Provider installed successfully: {name}"
        )

        return True