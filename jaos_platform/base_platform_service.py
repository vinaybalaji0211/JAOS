from __future__ import annotations

from jaos_platform.platform_runtime import PlatformRuntime


class BasePlatformService:
    """
    Base class for all runtime-managed JAOS services.
    """

    SERVICE_NAME = "base_service"
    INITIAL_STATUS = "READY"

    def __init__(self, runtime: PlatformRuntime | None = None):
        self.runtime = runtime

        if self.runtime is not None:
            self._register_platform_service()

    def _register_platform_service(self):
        if not self.runtime.container.is_registered(self.SERVICE_NAME):
            self.runtime.container.register(
                self.SERVICE_NAME,
                self,
            )

        self.runtime.context.set(
            f"{self.SERVICE_NAME}_status",
            self.INITIAL_STATUS,
        )

        self.runtime.events.publish(
            f"{self.SERVICE_NAME}_initialized",
            {
                "status": self.INITIAL_STATUS,
            },
        )