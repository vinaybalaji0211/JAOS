"""Deterministic output-schema formatting for intelligence prompts."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class PromptOutputSchemaResult:
    """Contains a normalized output schema and its prompt representation."""

    schema: Mapping[str, Any]
    content: str
    schema_hash: str

    def __post_init__(self) -> None:
        if not isinstance(self.schema, Mapping):
            raise TypeError("schema must be a mapping")

        if not isinstance(self.content, str) or not self.content.strip():
            raise ValueError("content must be a non-empty string")

        if not isinstance(self.schema_hash, str):
            raise TypeError("schema_hash must be a string")

        schema_hash = self.schema_hash.strip().lower()

        if len(schema_hash) != 64:
            raise ValueError(
                "schema_hash must be a SHA-256 hexadecimal digest"
            )

        try:
            int(schema_hash, 16)
        except ValueError as exc:
            raise ValueError(
                "schema_hash must be a SHA-256 hexadecimal digest"
            ) from exc

        object.__setattr__(self, "schema", dict(self.schema))
        object.__setattr__(self, "content", self.content.strip())
        object.__setattr__(self, "schema_hash", schema_hash)

    def to_dict(self) -> dict[str, Any]:
        """Return a serialization-friendly representation."""

        return {
            "schema": dict(self.schema),
            "content": self.content,
            "schema_hash": self.schema_hash,
        }


class PromptOutputSchemaFormatter:
    """
    Validates and formats provider-neutral JSON output requirements.

    Formatting is deterministic so identical schemas produce identical prompt
    content and trace hashes across executions and AI providers.
    """

    _HEADER = (
        "Return only a valid JSON value that follows the schema below.\n"
        "Do not include Markdown fences, commentary, or additional fields."
    )

    def format(
        self,
        schema: Mapping[str, Any],
    ) -> PromptOutputSchemaResult:
        """Validate, normalize, hash, and format an output schema."""

        if not isinstance(schema, Mapping):
            raise TypeError("output schema must be a mapping")

        if not schema:
            raise ValueError("output schema must not be empty")

        self._validate_value(schema, path="$")

        try:
            serialized_schema = json.dumps(
                schema,
                ensure_ascii=False,
                allow_nan=False,
                indent=2,
                sort_keys=True,
                separators=(",", ": "),
            )
        except (TypeError, ValueError, RecursionError) as exc:
            raise ValueError(
                "output schema must be JSON serializable"
            ) from exc

        normalized_schema = json.loads(serialized_schema)

        schema_hash = hashlib.sha256(
            serialized_schema.encode("utf-8")
        ).hexdigest()

        content = (
            f"{self._HEADER}\n\n"
            f"Output schema:\n{serialized_schema}"
        )

        return PromptOutputSchemaResult(
            schema=normalized_schema,
            content=content,
            schema_hash=schema_hash,
        )

    def _validate_value(self, value: Any, path: str) -> None:
        """Recursively reject unsupported or ambiguous JSON structures."""

        if value is None or isinstance(value, (str, bool, int)):
            return

        if isinstance(value, float):
            if value != value or value in {float("inf"), float("-inf")}:
                raise ValueError(
                    f"output schema contains a non-finite number at {path}"
                )
            return

        if isinstance(value, Mapping):
            for key, nested_value in value.items():
                if not isinstance(key, str):
                    raise TypeError(
                        "output schema object keys must be strings "
                        f"at {path}"
                    )

                normalized_key = key.strip()

                if not normalized_key:
                    raise ValueError(
                        "output schema object keys must not be empty "
                        f"at {path}"
                    )

                self._validate_value(
                    nested_value,
                    path=f"{path}.{normalized_key}",
                )
            return

        if isinstance(value, (list, tuple)):
            for index, nested_value in enumerate(value):
                self._validate_value(
                    nested_value,
                    path=f"{path}[{index}]",
                )
            return

        raise TypeError(
            "output schema contains an unsupported value "
            f"of type {type(value).__name__} at {path}"
        )