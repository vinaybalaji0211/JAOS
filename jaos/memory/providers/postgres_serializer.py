from __future__ import annotations

import json
from datetime import datetime
from enum import Enum
from typing import Any, Mapping

from jaos.memory.models.memory_identity import MemoryIdentity
from jaos.memory.models.memory_lifecycle_state import (
    MemoryLifecycleState,
)
from jaos.memory.models.memory_metadata import MemoryMetadata
from jaos.memory.models.memory_record import MemoryRecord
from jaos.memory.models.memory_scope import MemoryScope
from jaos.memory.models.memory_statistics import MemoryStatistics
from jaos.memory.models.memory_type import MemoryType


class PostgreSQLMemorySerializer:
    """
    Serialize MemoryRecord objects for PostgreSQL persistence.

    The serializer keeps PostgreSQL-specific row conversion outside
    PostgreSQLStore and uses explicit, safe JSON encoding instead of pickle.

    Rows returned by the PostgreSQL provider are expected to implement the
    Mapping interface, such as dictionaries returned by Psycopg's dict_row
    row factory.
    """

    COLUMN_NAMES = (
        "memory_id",
        "content",
        "memory_type",
        "memory_scope",
        "identity_json",
        "source",
        "importance",
        "confidence",
        "lifecycle_state",
        "metadata_json",
        "statistics_json",
        "created_at",
        "updated_at",
    )

    @classmethod
    def to_parameters(
        cls,
        record: MemoryRecord,
    ) -> tuple[Any, ...]:
        """
        Convert a MemoryRecord into parameters matching the memories table.
        """
        if not isinstance(record, MemoryRecord):
            raise TypeError("record must be a MemoryRecord")

        identity_payload = {
            "scope": record.identity.scope.value,
            "identity_id": record.identity.identity_id,
        }

        statistics_payload = {
            "access_count": record.statistics.access_count,
            "last_accessed_at": (
                record.statistics.last_accessed_at.isoformat()
                if record.statistics.last_accessed_at is not None
                else None
            ),
        }

        return (
            record.memory_id,
            record.content,
            record.memory_type.value,
            record.identity.scope.value,
            cls._dumps(identity_payload),
            record.source,
            record.importance,
            record.confidence,
            record.lifecycle_state.value,
            cls._dumps(record.metadata.to_dict()),
            cls._dumps(statistics_payload),
            record.created_at.isoformat(),
            record.updated_at.isoformat(),
        )

    @classmethod
    def to_mapping(
        cls,
        record: MemoryRecord,
    ) -> dict[str, Any]:
        """
        Convert a MemoryRecord into a column-name mapping.
        """
        return dict(
            zip(
                cls.COLUMN_NAMES,
                cls.to_parameters(record),
            )
        )

    @classmethod
    def from_row(
        cls,
        row: Mapping[str, Any],
    ) -> MemoryRecord:
        """
        Reconstruct a MemoryRecord from a PostgreSQL row mapping.
        """
        if not isinstance(row, Mapping):
            raise TypeError(
                "row must be a mapping"
            )

        identity_payload = cls._decode_json_field(
            row,
            "identity_json",
        )
        metadata_payload = cls._decode_json_field(
            row,
            "metadata_json",
        )
        statistics_payload = cls._decode_json_field(
            row,
            "statistics_json",
        )

        if not isinstance(identity_payload, dict):
            raise ValueError(
                "identity_json must decode to an object"
            )

        if not isinstance(metadata_payload, dict):
            raise ValueError(
                "metadata_json must decode to an object"
            )

        if not isinstance(statistics_payload, dict):
            raise ValueError(
                "statistics_json must decode to an object"
            )

        stored_scope = MemoryScope(
            cls._required_string(
                row,
                "memory_scope",
            )
        )

        identity_scope = MemoryScope(
            cls._required_string(
                identity_payload,
                "scope",
            )
        )

        if stored_scope is not identity_scope:
            raise ValueError(
                "memory_scope does not match identity_json scope"
            )

        identity_id = identity_payload.get(
            "identity_id"
        )

        if identity_id is not None and not isinstance(
            identity_id,
            str,
        ):
            raise ValueError(
                "identity_id must be a string or null"
            )

        last_accessed_raw = statistics_payload.get(
            "last_accessed_at"
        )

        if last_accessed_raw is None:
            last_accessed_at = None
        elif isinstance(last_accessed_raw, datetime):
            last_accessed_at = cls._validate_datetime(
                last_accessed_raw,
                field_name="last_accessed_at",
            )
        elif isinstance(last_accessed_raw, str):
            last_accessed_at = cls._parse_datetime(
                last_accessed_raw,
                field_name="last_accessed_at",
            )
        else:
            raise ValueError(
                "last_accessed_at must be a string, datetime, or null"
            )

        access_count = statistics_payload.get(
            "access_count"
        )

        if not isinstance(access_count, int) or isinstance(
            access_count,
            bool,
        ):
            raise ValueError(
                "statistics access_count must be an integer"
            )

        return MemoryRecord(
            memory_id=cls._required_string(
                row,
                "memory_id",
            ),
            content=cls._required_string(
                row,
                "content",
            ),
            memory_type=MemoryType(
                cls._required_string(
                    row,
                    "memory_type",
                )
            ),
            identity=MemoryIdentity(
                scope=identity_scope,
                identity_id=identity_id,
            ),
            source=cls._required_string(
                row,
                "source",
            ),
            importance=cls._required_number(
                row,
                "importance",
            ),
            confidence=cls._required_number(
                row,
                "confidence",
            ),
            lifecycle_state=MemoryLifecycleState(
                cls._required_string(
                    row,
                    "lifecycle_state",
                )
            ),
            metadata=MemoryMetadata(
                values=metadata_payload,
            ),
            statistics=MemoryStatistics(
                access_count=access_count,
                last_accessed_at=last_accessed_at,
            ),
            created_at=cls._required_datetime(
                row,
                "created_at",
            ),
            updated_at=cls._required_datetime(
                row,
                "updated_at",
            ),
        )

    @classmethod
    def _decode_json_field(
        cls,
        row: Mapping[str, Any],
        key: str,
    ) -> Any:
        """
        Decode a JSON-backed PostgreSQL field.

        Psycopg may return JSON/JSONB columns as native Python objects or as
        strings depending on connection and type-adapter configuration.
        """
        try:
            value = row[key]
        except KeyError as error:
            raise ValueError(
                f"missing required PostgreSQL field: {key}"
            ) from error

        if isinstance(value, str):
            return cls._loads(value)

        if isinstance(
            value,
            (
                dict,
                list,
                int,
                float,
                bool,
            ),
        ) or value is None:
            return cls._decode_value(value)

        raise ValueError(
            f"PostgreSQL field {key!r} must contain JSON-compatible data"
        )

    @classmethod
    def _dumps(
        cls,
        value: Any,
    ) -> str:
        """
        Encode a value as deterministic JSON while preserving supported types.
        """
        encoded = cls._encode_value(value)

        try:
            return json.dumps(
                encoded,
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            )
        except (TypeError, ValueError) as error:
            raise ValueError(
                "value cannot be serialized to PostgreSQL JSON"
            ) from error

    @classmethod
    def _loads(
        cls,
        value: str,
    ) -> Any:
        """
        Decode JSON created by this serializer.
        """
        if not isinstance(value, str):
            raise TypeError(
                "PostgreSQL JSON payload must be a string"
            )

        try:
            decoded = json.loads(value)
        except json.JSONDecodeError as error:
            raise ValueError(
                "invalid PostgreSQL JSON payload"
            ) from error

        return cls._decode_value(decoded)

    @classmethod
    def _encode_value(
        cls,
        value: Any,
    ) -> Any:
        """
        Recursively convert supported Python values into JSON-safe values.
        """
        if value is None or isinstance(
            value,
            (
                str,
                int,
                float,
                bool,
            ),
        ):
            return value

        if isinstance(value, datetime):
            return {
                "__jaos_type__": "datetime",
                "value": value.isoformat(),
            }

        if isinstance(value, Enum):
            return {
                "__jaos_type__": "enum",
                "enum_class": value.__class__.__name__,
                "value": value.value,
            }

        if isinstance(value, tuple):
            return {
                "__jaos_type__": "tuple",
                "items": [
                    cls._encode_value(item)
                    for item in value
                ],
            }

        if isinstance(value, set):
            return {
                "__jaos_type__": "set",
                "items": [
                    cls._encode_value(item)
                    for item in sorted(
                        value,
                        key=repr,
                    )
                ],
            }

        if isinstance(value, frozenset):
            return {
                "__jaos_type__": "frozenset",
                "items": [
                    cls._encode_value(item)
                    for item in sorted(
                        value,
                        key=repr,
                    )
                ],
            }

        if isinstance(value, list):
            return [
                cls._encode_value(item)
                for item in value
            ]

        if isinstance(value, Mapping):
            encoded_mapping: dict[str, Any] = {}

            for key, item in value.items():
                if not isinstance(key, str):
                    raise TypeError(
                        "JSON mapping keys must be strings"
                    )

                encoded_mapping[key] = cls._encode_value(
                    item
                )

            return encoded_mapping

        raise TypeError(
            "unsupported metadata value type: "
            f"{type(value).__name__}"
        )

    @classmethod
    def _decode_value(
        cls,
        value: Any,
    ) -> Any:
        """
        Restore Python values from the tagged JSON representation.
        """
        if isinstance(value, list):
            return [
                cls._decode_value(item)
                for item in value
            ]

        if not isinstance(value, dict):
            return value

        type_marker = value.get(
            "__jaos_type__"
        )

        if type_marker is None:
            return {
                key: cls._decode_value(item)
                for key, item in value.items()
            }

        if type_marker == "datetime":
            raw_value = value.get(
                "value"
            )

            if not isinstance(raw_value, str):
                raise ValueError(
                    "serialized datetime value must be a string"
                )

            return cls._parse_datetime(
                raw_value,
                field_name="metadata datetime",
            )

        if type_marker in {
            "tuple",
            "set",
            "frozenset",
        }:
            raw_items = value.get(
                "items"
            )

            if not isinstance(raw_items, list):
                raise ValueError(
                    f"serialized {type_marker} items must be a list"
                )

            decoded_items = [
                cls._decode_value(item)
                for item in raw_items
            ]

            if type_marker == "tuple":
                return tuple(
                    decoded_items
                )

            if type_marker == "set":
                return set(
                    decoded_items
                )

            return frozenset(
                decoded_items
            )

        if type_marker == "enum":
            return value.get(
                "value"
            )

        raise ValueError(
            f"unknown JAOS serialized type: {type_marker!r}"
        )

    @staticmethod
    def _required_string(
        values: Mapping[str, Any],
        key: str,
    ) -> str:
        """
        Read a required string field.
        """
        try:
            value = values[key]
        except KeyError as error:
            raise ValueError(
                f"missing required PostgreSQL field: {key}"
            ) from error

        if not isinstance(value, str):
            raise ValueError(
                f"PostgreSQL field {key!r} must be a string"
            )

        return value

    @staticmethod
    def _required_number(
        values: Mapping[str, Any],
        key: str,
    ) -> float:
        """
        Read a required numeric field.
        """
        try:
            value = values[key]
        except KeyError as error:
            raise ValueError(
                f"missing required PostgreSQL field: {key}"
            ) from error

        if (
            not isinstance(value, (int, float))
            or isinstance(value, bool)
        ):
            raise ValueError(
                f"PostgreSQL field {key!r} must be numeric"
            )

        return float(value)

    @classmethod
    def _required_datetime(
        cls,
        values: Mapping[str, Any],
        key: str,
    ) -> datetime:
        """
        Read a required timezone-aware datetime field.

        PostgreSQL timestamp columns may be returned as datetime objects,
        while mocked rows and compatibility paths may provide ISO strings.
        """
        try:
            value = values[key]
        except KeyError as error:
            raise ValueError(
                f"missing required PostgreSQL field: {key}"
            ) from error

        if isinstance(value, datetime):
            return cls._validate_datetime(
                value,
                field_name=key,
            )

        if isinstance(value, str):
            return cls._parse_datetime(
                value,
                field_name=key,
            )

        raise ValueError(
            f"PostgreSQL field {key!r} must be a datetime or string"
        )

    @staticmethod
    def _validate_datetime(
        value: datetime,
        *,
        field_name: str,
    ) -> datetime:
        """
        Validate that a datetime contains timezone information.
        """
        if value.tzinfo is None:
            raise ValueError(
                f"{field_name} must be timezone-aware"
            )

        return value

    @classmethod
    def _parse_datetime(
        cls,
        value: str,
        *,
        field_name: str,
    ) -> datetime:
        """
        Parse and validate an ISO-8601 timezone-aware datetime.
        """
        try:
            parsed = datetime.fromisoformat(
                value
            )
        except ValueError as error:
            raise ValueError(
                f"{field_name} must be a valid ISO-8601 datetime"
            ) from error

        return cls._validate_datetime(
            parsed,
            field_name=field_name,
        )