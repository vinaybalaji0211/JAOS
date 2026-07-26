"""Context policy registry for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from threading import RLock

from jaos.intelligence.context.context_policy import ContextPolicy
from jaos.intelligence.exceptions import IntelligenceContextError


def _normalize_policy_name(policy_name: str) -> str:
    """Validate and normalize a context policy name."""

    if not isinstance(policy_name, str):
        raise TypeError("policy_name must be a string")

    normalized = policy_name.strip().lower()

    if not normalized:
        raise ValueError("policy_name must not be empty")

    return normalized


class ContextPolicyRegistry:
    """Thread-safe registry and resolver for named context policies."""

    DEFAULT_POLICY_NAME = "default"

    def __init__(
        self,
        default_policy: ContextPolicy | None = None,
    ) -> None:
        if (
            default_policy is not None
            and not isinstance(default_policy, ContextPolicy)
        ):
            raise TypeError(
                "default_policy must be a ContextPolicy or None"
            )

        self._policies: dict[str, ContextPolicy] = {
            self.DEFAULT_POLICY_NAME: default_policy or ContextPolicy()
        }
        self._lock = RLock()

    def register_policy(
        self,
        policy_name: str,
        policy: ContextPolicy,
        *,
        replace: bool = False,
    ) -> None:
        """Register a named context policy."""

        normalized_name = _normalize_policy_name(policy_name)

        if not isinstance(policy, ContextPolicy):
            raise TypeError(
                "policy must be an instance of ContextPolicy"
            )

        if not isinstance(replace, bool):
            raise TypeError("replace must be a boolean")

        with self._lock:
            if normalized_name in self._policies and not replace:
                raise IntelligenceContextError(
                    f"context policy already registered: "
                    f"{normalized_name}",
                    details={"policy_name": normalized_name},
                )

            self._policies[normalized_name] = policy

    def unregister_policy(
        self,
        policy_name: str,
    ) -> ContextPolicy:
        """Remove and return a non-default context policy."""

        normalized_name = _normalize_policy_name(policy_name)

        if normalized_name == self.DEFAULT_POLICY_NAME:
            raise IntelligenceContextError(
                "the default context policy cannot be unregistered",
                details={"policy_name": normalized_name},
            )

        with self._lock:
            policy = self._policies.pop(normalized_name, None)

        if policy is None:
            raise IntelligenceContextError(
                f"context policy not found: {normalized_name}",
                details={"policy_name": normalized_name},
            )

        return policy

    def get_policy(
        self,
        policy_name: str,
    ) -> ContextPolicy:
        """Return a registered context policy."""

        normalized_name = _normalize_policy_name(policy_name)

        with self._lock:
            policy = self._policies.get(normalized_name)

        if policy is None:
            raise IntelligenceContextError(
                f"context policy not found: {normalized_name}",
                details={"policy_name": normalized_name},
            )

        return policy

    def resolve(
        self,
        policy_name: str | None,
    ) -> ContextPolicy:
        """Resolve an optional request policy name."""

        if policy_name is None:
            return self.get_policy(self.DEFAULT_POLICY_NAME)

        return self.get_policy(policy_name)

    def contains(self, policy_name: str) -> bool:
        """Return whether a policy name is registered."""

        normalized_name = _normalize_policy_name(policy_name)

        with self._lock:
            return normalized_name in self._policies

    def list_policy_names(self) -> tuple[str, ...]:
        """Return registered policy names in registration order."""

        with self._lock:
            return tuple(self._policies)

    def __len__(self) -> int:
        """Return the number of registered policies."""

        with self._lock:
            return len(self._policies)