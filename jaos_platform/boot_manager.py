from __future__ import annotations

from jaos_platform.dependency_validator import DependencyValidator
from jaos_platform.lifecycle_state import RuntimeLifecycleState
from jaos_platform.platform_runtime import PlatformRuntime
from jaos_platform.runtime_health_certifier import (
    RuntimeHealthCertifier,
)
from jaos_platform.runtime_validator import RuntimeValidator
from jaos_platform.startup_validator import StartupValidator

_STOPPABLE_LIFECYCLE_STATES = frozenset(
    {
        RuntimeLifecycleState.INITIALIZED,
        RuntimeLifecycleState.READY,
        RuntimeLifecycleState.DEGRADED,
    }
)

_BOOT_TIME_CONTEXT_KEYS = (
    "runtime_report",
    "startup_report",
    "dependency_report",
    "health_report",
)


class BootManager:
    """Coordinates the complete JAOS boot lifecycle."""

    def __init__(self, runtime: PlatformRuntime | None = None):
        self.runtime = runtime or PlatformRuntime()
        self.steps = []
        self.status = "CREATED"

    def register_step(self, step_name: str) -> None:
        self.steps.append(step_name)

    def boot(self) -> bool:
        self.steps = []

        self.runtime.initialize()
        self.status = "BOOTING"

        try:
            self.runtime.start()
        except Exception:
            self.status = "FAILED"
            self.runtime.context.set("boot_status", self.status)
            self.runtime.events.publish(
                "boot_failed", {"status": self.status}
            )
            return False

        self.register_step("platform_runtime")

        runtime_report = RuntimeValidator(self.runtime).validate()
        self.register_step("runtime_validator")

        startup_report = StartupValidator(self.runtime).validate()
        self.register_step("startup_validator")

        dependency_report = DependencyValidator(self.runtime).validate()
        self.register_step("dependency_validator")

        health_report = RuntimeHealthCertifier(self.runtime).certify()
        self.register_step("runtime_health_certifier")

        self.runtime.context.set("runtime_report", runtime_report)
        self.runtime.context.set("startup_report", startup_report)
        self.runtime.context.set("dependency_report", dependency_report)
        self.runtime.context.set("health_report", health_report)

        required_ready = (
            runtime_report["healthy"]
            and startup_report["ready"]
            and dependency_report["valid"]
        )

        if not required_ready:
            self.runtime.mark_failed()
            self.status = "FAILED"
            self.runtime.context.set("boot_status", self.status)
            self.runtime.events.publish(
                "boot_failed", {"status": self.status}
            )
            return False

        self.status = "READY"
        self.runtime.context.set("boot_status", self.status)
        self.runtime.events.publish(
            "boot_completed", {"status": self.status}
        )
        return True

    def shutdown(self) -> bool:
        """Coordinate runtime-wide teardown.

        Only attempts PlatformRuntime.stop() from a state where STOPPING is a
        legal transition, so an illegal transition is never attempted rather
        than raised and reported as a failure. Stale boot-time reports are
        cleared so RuntimeContext cannot keep claiming readiness facts about
        a runtime that is no longer running, and event subscriptions are
        released as the final step, after the shutdown notification.
        """

        errors: list[str] = []

        if self.runtime.lifecycle_state in _STOPPABLE_LIFECYCLE_STATES:
            try:
                self.runtime.stop()
            except Exception as exc:
                errors.append(str(exc))

        for key in _BOOT_TIME_CONTEXT_KEYS:
            self.runtime.context.remove(key)

        if errors:
            self.status = "FAILED"
        elif self.runtime.lifecycle_state == RuntimeLifecycleState.STOPPED:
            self.status = "STOPPED"
        elif self.runtime.lifecycle_state == RuntimeLifecycleState.FAILED:
            self.status = "FAILED"
        else:
            self.status = "SHUTDOWN"

        self.runtime.context.set("boot_status", self.status)

        self.runtime.events.publish(
            "boot_shutdown", {"status": self.status, "errors": errors}
        )

        self.runtime.events.clear()

        return len(errors) == 0
