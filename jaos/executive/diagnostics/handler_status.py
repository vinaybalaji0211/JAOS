from jaos.executive.diagnostics.models import DiagnosticStatus
from jaos.executive.intent_registry import ExecutiveIntentRegistry


class HandlerStatusProvider:
    """
    Reports diagnostics for registered Executive intent handlers.
    """

    def __init__(self, registry: ExecutiveIntentRegistry) -> None:
        self.registry = registry

    def get_status(self) -> DiagnosticStatus:
        handlers = self.registry.list_handlers()

        return DiagnosticStatus(
            component="Executive Handlers",
            healthy=bool(handlers),
            message=f"{len(handlers)} handler(s) registered.",
            details={
                "handler_count": len(handlers),
                "handlers": handlers,
            },
        )