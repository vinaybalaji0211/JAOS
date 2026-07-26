"""Structured exceptions for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from typing import Any


def _normalize_optional_text(
    value: str | None,
    field_name: str,
) -> str | None:
    """Validate and normalize optional exception context."""

    if value is None:
        return None

    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string or None")

    normalized = value.strip()

    if not normalized:
        raise ValueError(f"{field_name} must not be empty")

    return normalized


class IntelligencePlatformError(Exception):
    """Base exception for all AI Intelligence Platform failures."""

    error_code = "intelligence_platform_error"
    default_component = "intelligence"

    def __init__(
        self,
        message: str,
        *,
        request_id: str | None = None,
        component: str | None = None,
        retryable: bool = False,
        details: dict[str, Any] | None = None,
    ) -> None:
        if not isinstance(message, str):
            raise TypeError("message must be a string")

        normalized_message = message.strip()

        if not normalized_message:
            raise ValueError("message must not be empty")

        if not isinstance(retryable, bool):
            raise TypeError("retryable must be a boolean")

        if details is not None and not isinstance(details, dict):
            raise TypeError("details must be a dictionary or None")

        normalized_component = _normalize_optional_text(
            component,
            "component",
        )

        self.message = normalized_message
        self.request_id = _normalize_optional_text(
            request_id,
            "request_id",
        )
        self.component = normalized_component or self.default_component
        self.retryable = retryable
        self.details = dict(details or {})

        super().__init__(self.message)

    def to_dict(self) -> dict[str, Any]:
        """Return a serialization-safe representation of the failure."""

        return {
            "error_type": type(self).__name__,
            "error_code": self.error_code,
            "message": self.message,
            "request_id": self.request_id,
            "component": self.component,
            "retryable": self.retryable,
            "details": dict(self.details),
        }


class IntelligenceValidationError(IntelligencePlatformError):
    """Raised when an intelligence operation receives invalid input."""

    error_code = "intelligence_validation_error"
    default_component = "validation"


class IntelligenceRequestError(IntelligencePlatformError):
    """Raised when an intelligence request cannot be processed."""

    error_code = "intelligence_request_error"
    default_component = "request"


class IntelligenceContextError(IntelligencePlatformError):
    """Raised when context cannot be collected or assembled safely."""

    error_code = "intelligence_context_error"
    default_component = "context"


class IntelligenceConversationError(IntelligencePlatformError):
    """Raised when conversation processing fails."""

    error_code = "intelligence_conversation_error"
    default_component = "conversation"


class IntelligenceReasoningError(IntelligencePlatformError):
    """Raised when structured reasoning cannot be completed."""

    error_code = "intelligence_reasoning_error"
    default_component = "reasoning"


class IntelligencePlanningError(IntelligencePlatformError):
    """Raised when plan proposal generation fails."""

    error_code = "intelligence_planning_error"
    default_component = "planning"


class IntelligenceAgentError(IntelligencePlatformError):
    """Raised when agent discovery, routing, or delegation fails."""

    error_code = "intelligence_agent_error"
    default_component = "agent_orchestration"


class IntelligenceExecutionProposalError(IntelligencePlatformError):
    """Raised when an execution proposal cannot be produced."""

    error_code = "intelligence_execution_proposal_error"
    default_component = "execution_proposal"


class IntelligencePermissionError(IntelligencePlatformError):
    """Raised when an operation violates its permission boundary."""

    error_code = "intelligence_permission_error"
    default_component = "permissions"


class IntelligenceApprovalRequiredError(IntelligencePlatformError):
    """Raised when an operation requires explicit approval."""

    error_code = "intelligence_approval_required"
    default_component = "approval"


class IntelligenceComponentStateError(IntelligencePlatformError):
    """Raised when a component is unavailable or in an invalid state."""

    error_code = "intelligence_component_state_error"
    default_component = "lifecycle"