"""Conversation policy registry for the JAOS Intelligence Platform."""

from __future__ import annotations

from copy import deepcopy
from threading import RLock

from jaos.intelligence.conversation.conversation_policy import (
    ConversationPolicy,
)
from jaos.intelligence.exceptions import IntelligenceConversationError


def _normalize_policy_name(policy_name: str) -> str:
    """Validate and normalize a conversation policy name."""

    if not isinstance(policy_name, str):
        raise TypeError("policy_name must be a string")

    normalized = policy_name.strip().lower()

    if not normalized:
        raise ValueError("policy_name must not be empty")

    return normalized


class ConversationPolicyRegistry:
    """Thread-safe registry of approved conversation policies."""

    def __init__(self) -> None:
        self._policies: dict[str, ConversationPolicy] = {}
        self._default_policy_name: str | None = None
        self._lock = RLock()

    @property
    def default_policy_name(self) -> str | None:
        """Return the current default policy name."""

        with self._lock:
            return self._default_policy_name

    def register_policy(
        self,
        policy: ConversationPolicy,
        *,
        make_default: bool = False,
        replace: bool = False,
    ) -> None:
        """Register one approved conversation policy."""

        if not isinstance(policy, ConversationPolicy):
            raise TypeError(
                "policy must be a ConversationPolicy"
            )

        if not isinstance(make_default, bool):
            raise TypeError("make_default must be a boolean")

        if not isinstance(replace, bool):
            raise TypeError("replace must be a boolean")

        with self._lock:
            if (
                policy.policy_name in self._policies
                and not replace
            ):
                raise IntelligenceConversationError(
                    "conversation policy already registered",
                    component="conversation_policy_registry",
                    details={
                        "policy_name": policy.policy_name,
                    },
                )

            self._policies[policy.policy_name] = deepcopy(policy)

            if (
                self._default_policy_name is None
                or make_default
            ):
                self._default_policy_name = policy.policy_name

    def get_policy(
        self,
        policy_name: str,
    ) -> ConversationPolicy:
        """Return an isolated copy of an exact policy."""

        normalized_name = _normalize_policy_name(policy_name)

        with self._lock:
            policy = self._policies.get(normalized_name)

        if policy is None:
            raise IntelligenceConversationError(
                "conversation policy not found",
                component="conversation_policy_registry",
                details={"policy_name": normalized_name},
            )

        return deepcopy(policy)

    def resolve_policy(
        self,
        policy_name: str | None = None,
    ) -> ConversationPolicy:
        """Resolve an explicit policy or the registered default."""

        if policy_name is not None:
            return self.get_policy(policy_name)

        with self._lock:
            default_policy_name = self._default_policy_name

        if default_policy_name is None:
            raise IntelligenceConversationError(
                "default conversation policy is not configured",
                component="conversation_policy_registry",
            )

        return self.get_policy(default_policy_name)

    def set_default_policy(
        self,
        policy_name: str,
    ) -> None:
        """Set the default to an existing policy."""

        policy = self.get_policy(policy_name)

        with self._lock:
            self._default_policy_name = policy.policy_name

    def unregister_policy(
        self,
        policy_name: str,
    ) -> ConversationPolicy:
        """Remove and return one registered policy."""

        normalized_name = _normalize_policy_name(policy_name)

        with self._lock:
            policy = self._policies.pop(
                normalized_name,
                None,
            )

            if policy is None:
                raise IntelligenceConversationError(
                    "conversation policy not found",
                    component="conversation_policy_registry",
                    details={"policy_name": normalized_name},
                )

            if self._default_policy_name == normalized_name:
                self._default_policy_name = (
                    sorted(self._policies)[0]
                    if self._policies
                    else None
                )

        return deepcopy(policy)

    def list_policies(self) -> tuple[ConversationPolicy, ...]:
        """Return isolated policies in deterministic name order."""

        with self._lock:
            policies = tuple(
                self._policies[name]
                for name in sorted(self._policies)
            )

        return tuple(deepcopy(policy) for policy in policies)

    def contains(self, policy_name: str) -> bool:
        """Return whether a policy name is registered."""

        normalized_name = _normalize_policy_name(policy_name)

        with self._lock:
            return normalized_name in self._policies

    def __len__(self) -> int:
        """Return the number of registered policies."""

        with self._lock:
            return len(self._policies)