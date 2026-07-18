from jaos.executive.diagnostics.models import DiagnosticStatus


class ExecutionStatusProvider:
    """
    Reports diagnostics for Executive execution coordination.
    """

    def get_status(self) -> DiagnosticStatus:
        return DiagnosticStatus(
            component="Executive Execution Coordinator",
            healthy=True,
            message="Execution coordinator is ready.",
            details={
                "execution_mode": "sequential",
                "supports_multi_step_plans": True,
            },
        )