from dataclasses import dataclass


@dataclass
class AIMetrics:
    """
    Runtime metrics for the AI Platform.
    """

    requests_total: int = 0
    requests_succeeded: int = 0
    requests_failed: int = 0
    last_provider: str | None = None
    last_model: str | None = None

    def record_success(
        self,
        *,
        provider: str,
        model: str | None = None,
    ) -> None:
        self.requests_total += 1
        self.requests_succeeded += 1
        self.last_provider = provider
        self.last_model = model

    def record_failure(
        self,
        *,
        provider: str | None = None,
        model: str | None = None,
    ) -> None:
        self.requests_total += 1
        self.requests_failed += 1
        self.last_provider = provider
        self.last_model = model

    def success_rate(self) -> float:
        if self.requests_total == 0:
            return 0.0

        return self.requests_succeeded / self.requests_total