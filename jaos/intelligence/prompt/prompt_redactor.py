"""Sensitive-context redaction hooks for JAOS Intelligence."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from jaos.intelligence.models import ContextItem


@dataclass(frozen=True, slots=True)
class PromptRedactionResult:
    """Result returned by a prompt redaction hook."""

    content: str
    redacted: bool = False
    redaction_count: int = 0
    redaction_labels: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.content, str):
            raise TypeError("content must be a string")

        if not isinstance(self.redacted, bool):
            raise TypeError("redacted must be a boolean")

        if (
            isinstance(self.redaction_count, bool)
            or not isinstance(self.redaction_count, int)
        ):
            raise TypeError("redaction_count must be an integer")

        if self.redaction_count < 0:
            raise ValueError(
                "redaction_count must not be negative"
            )

        if not isinstance(self.redaction_labels, (tuple, list)):
            raise TypeError(
                "redaction_labels must be a tuple or list"
            )

        normalized_labels: list[str] = []

        for label in self.redaction_labels:
            if not isinstance(label, str) or not label.strip():
                raise ValueError(
                    "redaction labels must be non-empty strings"
                )

            normalized = label.strip().lower()

            if normalized not in normalized_labels:
                normalized_labels.append(normalized)

        if self.redacted and self.redaction_count == 0:
            raise ValueError(
                "redacted results must report a redaction count"
            )

        if not self.redacted and self.redaction_count != 0:
            raise ValueError(
                "unredacted results cannot report redactions"
            )

        object.__setattr__(
            self,
            "redaction_labels",
            tuple(normalized_labels),
        )


@runtime_checkable
class PromptRedactor(Protocol):
    """Contract for sensitive-context redaction hooks."""

    def redact(
        self,
        content: str,
        *,
        context_item: ContextItem,
    ) -> PromptRedactionResult:
        """Return approved prompt content for a context item."""


class MetadataSensitiveContextRedactor:
    """
    Applies redaction rules declared by trusted context adapters.

    Supported metadata:
    - sensitive: redact the complete context item.
    - sensitive_terms: redact specified terms from its content.
    """

    FULL_REDACTION_TEXT = "[REDACTED SENSITIVE CONTEXT]"
    TERM_REDACTION_TEXT = "[REDACTED]"

    def redact(
        self,
        content: str,
        *,
        context_item: ContextItem,
    ) -> PromptRedactionResult:
        """Redact sensitive context without mutating the source item."""

        if not isinstance(content, str):
            raise TypeError("content must be a string")

        if not isinstance(context_item, ContextItem):
            raise TypeError(
                "context_item must be a ContextItem"
            )

        sensitive = context_item.metadata.get(
            "sensitive",
            False,
        )

        if not isinstance(sensitive, bool):
            raise TypeError(
                "context metadata sensitive must be boolean"
            )

        if sensitive:
            return PromptRedactionResult(
                content=self.FULL_REDACTION_TEXT,
                redacted=True,
                redaction_count=1,
                redaction_labels=("full_context",),
            )

        sensitive_terms = context_item.metadata.get(
            "sensitive_terms",
            (),
        )

        if not isinstance(sensitive_terms, (tuple, list)):
            raise TypeError(
                "context metadata sensitive_terms must be "
                "a tuple or list"
            )

        redacted_content = content
        redaction_count = 0

        for term in sensitive_terms:
            if not isinstance(term, str) or not term.strip():
                raise ValueError(
                    "sensitive terms must be non-empty strings"
                )

            pattern = re.compile(
                re.escape(term.strip()),
                flags=re.IGNORECASE,
            )
            redacted_content, replacements = pattern.subn(
                self.TERM_REDACTION_TEXT,
                redacted_content,
            )
            redaction_count += replacements

        return PromptRedactionResult(
            content=redacted_content,
            redacted=redaction_count > 0,
            redaction_count=redaction_count,
            redaction_labels=(
                ("sensitive_terms",)
                if redaction_count > 0
                else ()
            ),
        )