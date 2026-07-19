from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

import pytest

from jaos.memory.models.memory_identity import MemoryIdentity
from jaos.memory.models.memory_lifecycle_state import (
    MemoryLifecycleState,
)
from jaos.memory.models.memory_metadata import MemoryMetadata
from jaos.memory.models.memory_record import MemoryRecord
from jaos.memory.models.memory_scope import MemoryScope
from jaos.memory.models.memory_statistics import MemoryStatistics
from jaos.memory.models.memory_type import MemoryType
from jaos.memory.providers.postgres_serializer import (
    PostgreSQLMemorySerializer,
)


class ExampleMetadataEnum(Enum):
    """
    Enum used to verify metadata enum serialization.
    """

    FIRST = "first"
    SECOND = "second"


@pytest.fixture
def memory_type() -> MemoryType:
    """
    Return one valid memory type.
    """
    return next(iter(MemoryType))


@pytest.fixture
def lifecycle_state() -> MemoryLifecycleState:
    """
    Return one valid lifecycle state.
    """
    return next(iter(MemoryLifecycleState))


@pytest.fixture
def aware_datetime() -> datetime:
    """
    Return a deterministic timezone-aware datetime.
    """
    return datetime(
        2026,
        7,
        19,
        10,
        30,
        45,
        123456,
        tzinfo=timezone.utc,
    )


@pytest.fixture
def record(
    memory_type: MemoryType,
    lifecycle_state: MemoryLifecycleState,
    aware_datetime: datetime,
) -> MemoryRecord:
    """
    Return a fully populated memory record.
    """
    return MemoryRecord(
        memory_id="postgres-memory-001",
        content="JAOS PostgreSQL serializer memory.",
        memory_type=memory_type,
        identity=MemoryIdentity(
            scope=MemoryScope.USER,
            identity_id="user-001",
        ),
        source="postgres-serializer-test",
        importance=0.85,
        confidence=0.95,
        lifecycle_state=lifecycle_state,
        metadata=MemoryMetadata(
            values={
                "tags": (
                    "jaos",
                    "postgresql",
                ),
                "nested": {
                    "enabled": True,
                    "count": 3,
                },
                "created": aware_datetime,
                "enum_value": ExampleMetadataEnum.FIRST,
                "set_value": {
                    "memory",
                    "database",
                },
                "frozen_value": frozenset(
                    {
                        "provider",
                        "storage",
                    }
                ),
                "list_value": [
                    1,
                    "two",
                    False,
                    None,
                ],
            }
        ),
        statistics=MemoryStatistics(
            access_count=4,
            last_accessed_at=aware_datetime,
        ),
        created_at=aware_datetime,
        updated_at=aware_datetime,
    )


def build_row(
    record: MemoryRecord,
) -> dict[str, Any]:
    """
    Build a PostgreSQL-compatible row mapping from a record.
    """
    return PostgreSQLMemorySerializer.to_mapping(record)


def test_column_names_match_memory_table_order() -> None:
    assert PostgreSQLMemorySerializer.COLUMN_NAMES == (
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


def test_to_parameters_serializes_memory_record(
    record: MemoryRecord,
) -> None:
    parameters = PostgreSQLMemorySerializer.to_parameters(
        record
    )

    assert len(parameters) == len(
        PostgreSQLMemorySerializer.COLUMN_NAMES
    )

    assert parameters[0] == record.memory_id
    assert parameters[1] == record.content
    assert parameters[2] == record.memory_type.value
    assert parameters[3] == record.identity.scope.value
    assert parameters[5] == record.source
    assert parameters[6] == record.importance
    assert parameters[7] == record.confidence
    assert parameters[8] == record.lifecycle_state.value
    assert parameters[11] == record.created_at.isoformat()
    assert parameters[12] == record.updated_at.isoformat()


def test_to_parameters_rejects_invalid_record_type() -> None:
    with pytest.raises(
        TypeError,
        match="record must be a MemoryRecord",
    ):
        PostgreSQLMemorySerializer.to_parameters(
            object()  # type: ignore[arg-type]
        )


def test_to_mapping_returns_named_columns(
    record: MemoryRecord,
) -> None:
    mapping = PostgreSQLMemorySerializer.to_mapping(
        record
    )

    assert tuple(mapping.keys()) == (
        PostgreSQLMemorySerializer.COLUMN_NAMES
    )
    assert mapping["memory_id"] == record.memory_id
    assert mapping["content"] == record.content
    assert mapping["memory_type"] == record.memory_type.value
    assert (
        mapping["memory_scope"]
        == record.identity.scope.value
    )


def test_record_round_trip_from_string_json(
    record: MemoryRecord,
) -> None:
    row = build_row(record)

    restored = PostgreSQLMemorySerializer.from_row(
        row
    )

    assert restored.memory_id == record.memory_id
    assert restored.content == record.content
    assert restored.memory_type == record.memory_type
    assert restored.identity == record.identity
    assert restored.source == record.source
    assert restored.importance == record.importance
    assert restored.confidence == record.confidence
    assert restored.lifecycle_state == record.lifecycle_state
    assert restored.statistics == record.statistics
    assert restored.created_at == record.created_at
    assert restored.updated_at == record.updated_at

    expected_metadata = record.metadata.to_dict()
    expected_metadata["enum_value"] = (
        ExampleMetadataEnum.FIRST.value
    )

    assert restored.metadata.to_dict() == expected_metadata


def test_record_round_trip_from_native_json(
    record: MemoryRecord,
) -> None:
    row = build_row(record)

    row["identity_json"] = (
        PostgreSQLMemorySerializer._loads(
            row["identity_json"]
        )
    )
    row["metadata_json"] = (
        PostgreSQLMemorySerializer._loads(
            row["metadata_json"]
        )
    )
    row["statistics_json"] = (
        PostgreSQLMemorySerializer._loads(
            row["statistics_json"]
        )
    )

    restored = PostgreSQLMemorySerializer.from_row(
        row
    )

    assert restored.memory_id == record.memory_id
    assert restored.content == record.content
    assert restored.memory_type == record.memory_type
    assert restored.identity == record.identity
    assert restored.source == record.source
    assert restored.importance == record.importance
    assert restored.confidence == record.confidence
    assert restored.lifecycle_state == record.lifecycle_state
    assert restored.statistics == record.statistics
    assert restored.created_at == record.created_at
    assert restored.updated_at == record.updated_at

    expected_metadata = record.metadata.to_dict()
    expected_metadata["enum_value"] = (
        ExampleMetadataEnum.FIRST.value
    )

    assert restored.metadata.to_dict() == expected_metadata


def test_from_row_accepts_datetime_columns(
    record: MemoryRecord,
) -> None:
    row = build_row(record)
    row["created_at"] = record.created_at
    row["updated_at"] = record.updated_at

    restored = PostgreSQLMemorySerializer.from_row(
        row
    )

    assert restored.created_at == record.created_at
    assert restored.updated_at == record.updated_at


def test_from_row_rejects_non_mapping() -> None:
    with pytest.raises(
        TypeError,
        match="row must be a mapping",
    ):
        PostgreSQLMemorySerializer.from_row(
            ("invalid",)  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "field_name",
    [
        "identity_json",
        "metadata_json",
        "statistics_json",
    ],
)
def test_from_row_rejects_missing_json_field(
    record: MemoryRecord,
    field_name: str,
) -> None:
    row = build_row(record)
    del row[field_name]

    with pytest.raises(
        ValueError,
        match=f"missing required PostgreSQL field: {field_name}",
    ):
        PostgreSQLMemorySerializer.from_row(
            row
        )


@pytest.mark.parametrize(
    ("field_name", "invalid_value"),
    [
        ("identity_json", []),
        ("metadata_json", []),
        ("statistics_json", []),
    ],
)
def test_from_row_requires_json_objects(
    record: MemoryRecord,
    field_name: str,
    invalid_value: object,
) -> None:
    row = build_row(record)
    row[field_name] = invalid_value

    with pytest.raises(
        ValueError,
        match=f"{field_name} must decode to an object",
    ):
        PostgreSQLMemorySerializer.from_row(
            row
        )


def test_from_row_rejects_invalid_json_field_type(
    record: MemoryRecord,
) -> None:
    row = build_row(record)
    row["metadata_json"] = object()

    with pytest.raises(
        ValueError,
        match=(
            "PostgreSQL field 'metadata_json' must contain "
            "JSON-compatible data"
        ),
    ):
        PostgreSQLMemorySerializer.from_row(
            row
        )


def test_from_row_rejects_mismatched_identity_scope(
    record: MemoryRecord,
) -> None:
    row = build_row(record)

    different_scope = next(
        scope
        for scope in MemoryScope
        if scope is not record.identity.scope
    )

    identity_payload = (
        PostgreSQLMemorySerializer._loads(
            row["identity_json"]
        )
    )
    identity_payload["scope"] = different_scope.value
    row["identity_json"] = (
        PostgreSQLMemorySerializer._dumps(
            identity_payload
        )
    )

    with pytest.raises(
        ValueError,
        match=(
            "memory_scope does not match "
            "identity_json scope"
        ),
    ):
        PostgreSQLMemorySerializer.from_row(
            row
        )


def test_from_row_rejects_invalid_identity_id_type(
    record: MemoryRecord,
) -> None:
    row = build_row(record)

    identity_payload = (
        PostgreSQLMemorySerializer._loads(
            row["identity_json"]
        )
    )
    identity_payload["identity_id"] = 123
    row["identity_json"] = (
        PostgreSQLMemorySerializer._dumps(
            identity_payload
        )
    )

    with pytest.raises(
        ValueError,
        match="identity_id must be a string or null",
    ):
        PostgreSQLMemorySerializer.from_row(
            row
        )


def test_from_row_accepts_null_last_accessed_at(
    record: MemoryRecord,
) -> None:
    row = build_row(record)

    statistics_payload = (
        PostgreSQLMemorySerializer._loads(
            row["statistics_json"]
        )
    )
    statistics_payload["access_count"] = 0
    statistics_payload["last_accessed_at"] = None

    row["statistics_json"] = (
        PostgreSQLMemorySerializer._dumps(
            statistics_payload
        )
    )

    restored = PostgreSQLMemorySerializer.from_row(
        row
    )

    assert restored.statistics.access_count == 0
    assert restored.statistics.last_accessed_at is None


def test_from_row_accepts_datetime_last_accessed_at(
    record: MemoryRecord,
) -> None:
    row = build_row(record)

    statistics_payload = (
        PostgreSQLMemorySerializer._loads(
            row["statistics_json"]
        )
    )
    statistics_payload["last_accessed_at"] = (
        record.statistics.last_accessed_at
    )
    row["statistics_json"] = statistics_payload

    restored = PostgreSQLMemorySerializer.from_row(
        row
    )

    assert (
        restored.statistics.last_accessed_at
        == record.statistics.last_accessed_at
    )


def test_from_row_rejects_invalid_last_accessed_type(
    record: MemoryRecord,
) -> None:
    row = build_row(record)

    statistics_payload = (
        PostgreSQLMemorySerializer._loads(
            row["statistics_json"]
        )
    )
    statistics_payload["last_accessed_at"] = 123
    row["statistics_json"] = (
        PostgreSQLMemorySerializer._dumps(
            statistics_payload
        )
    )

    with pytest.raises(
        ValueError,
        match=(
            "last_accessed_at must be a string, "
            "datetime, or null"
        ),
    ):
        PostgreSQLMemorySerializer.from_row(
            row
        )


@pytest.mark.parametrize(
    "invalid_access_count",
    [
        "4",
        1.5,
        True,
        None,
    ],
)
def test_from_row_rejects_invalid_access_count(
    record: MemoryRecord,
    invalid_access_count: object,
) -> None:
    row = build_row(record)

    statistics_payload = (
        PostgreSQLMemorySerializer._loads(
            row["statistics_json"]
        )
    )
    statistics_payload["access_count"] = (
        invalid_access_count
    )
    row["statistics_json"] = (
        PostgreSQLMemorySerializer._dumps(
            statistics_payload
        )
    )

    with pytest.raises(
        ValueError,
        match=(
            "statistics access_count must be an integer"
        ),
    ):
        PostgreSQLMemorySerializer.from_row(
            row
        )


def test_dumps_is_deterministic() -> None:
    first = PostgreSQLMemorySerializer._dumps(
        {
            "z": 1,
            "a": 2,
        }
    )
    second = PostgreSQLMemorySerializer._dumps(
        {
            "a": 2,
            "z": 1,
        }
    )

    assert first == second
    assert first == '{"a":2,"z":1}'


def test_dumps_and_loads_preserve_supported_values(
    aware_datetime: datetime,
) -> None:
    value = {
        "none": None,
        "text": "JAOS",
        "integer": 4,
        "number": 0.75,
        "boolean": True,
        "datetime": aware_datetime,
        "enum": ExampleMetadataEnum.SECOND,
        "tuple": (
            "a",
            2,
        ),
        "set": {
            "x",
            "y",
        },
        "frozenset": frozenset(
            {
                "m",
                "n",
            }
        ),
        "list": [
            1,
            "two",
        ],
        "mapping": {
            "nested": False,
        },
    }

    encoded = PostgreSQLMemorySerializer._dumps(
        value
    )
    decoded = PostgreSQLMemorySerializer._loads(
        encoded
    )

    assert decoded["none"] is None
    assert decoded["text"] == "JAOS"
    assert decoded["integer"] == 4
    assert decoded["number"] == 0.75
    assert decoded["boolean"] is True
    assert decoded["datetime"] == aware_datetime
    assert decoded["enum"] == ExampleMetadataEnum.SECOND.value
    assert decoded["tuple"] == ("a", 2)
    assert decoded["set"] == {"x", "y"}
    assert decoded["frozenset"] == frozenset({"m", "n"})
    assert decoded["list"] == [1, "two"]
    assert decoded["mapping"] == {
        "nested": False,
    }


def test_encode_value_rejects_non_string_mapping_key() -> None:
    with pytest.raises(
        TypeError,
        match="JSON mapping keys must be strings",
    ):
        PostgreSQLMemorySerializer._encode_value(
            {
                1: "invalid",
            }
        )


def test_encode_value_rejects_unsupported_type() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "unsupported metadata value type: object"
        ),
    ):
        PostgreSQLMemorySerializer._encode_value(
            object()
        )


def test_loads_rejects_non_string_payload() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "PostgreSQL JSON payload must be a string"
        ),
    ):
        PostgreSQLMemorySerializer._loads(
            {}  # type: ignore[arg-type]
        )


def test_loads_rejects_invalid_json() -> None:
    with pytest.raises(
        ValueError,
        match="invalid PostgreSQL JSON payload",
    ):
        PostgreSQLMemorySerializer._loads(
            "{invalid-json"
        )


def test_decode_value_rejects_invalid_datetime_payload() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "serialized datetime value must be a string"
        ),
    ):
        PostgreSQLMemorySerializer._decode_value(
            {
                "__jaos_type__": "datetime",
                "value": 123,
            }
        )


@pytest.mark.parametrize(
    "type_marker",
    [
        "tuple",
        "set",
        "frozenset",
    ],
)
def test_decode_value_rejects_invalid_collection_items(
    type_marker: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            f"serialized {type_marker} items must be a list"
        ),
    ):
        PostgreSQLMemorySerializer._decode_value(
            {
                "__jaos_type__": type_marker,
                "items": "invalid",
            }
        )


def test_decode_value_rejects_unknown_type_marker() -> None:
    with pytest.raises(
        ValueError,
        match="unknown JAOS serialized type",
    ):
        PostgreSQLMemorySerializer._decode_value(
            {
                "__jaos_type__": "unknown",
            }
        )


@pytest.mark.parametrize(
    "field_name",
    [
        "memory_id",
        "content",
        "memory_type",
        "memory_scope",
        "source",
        "lifecycle_state",
    ],
)
def test_from_row_rejects_missing_required_string(
    record: MemoryRecord,
    field_name: str,
) -> None:
    row = build_row(record)
    del row[field_name]

    with pytest.raises(
        ValueError,
        match=f"missing required PostgreSQL field: {field_name}",
    ):
        PostgreSQLMemorySerializer.from_row(
            row
        )


@pytest.mark.parametrize(
    "field_name",
    [
        "memory_id",
        "content",
        "memory_type",
        "memory_scope",
        "source",
        "lifecycle_state",
    ],
)
def test_from_row_rejects_invalid_required_string(
    record: MemoryRecord,
    field_name: str,
) -> None:
    row = build_row(record)
    row[field_name] = 123

    with pytest.raises(
        ValueError,
        match=(
            f"PostgreSQL field '{field_name}' "
            "must be a string"
        ),
    ):
        PostgreSQLMemorySerializer.from_row(
            row
        )


@pytest.mark.parametrize(
    "field_name",
    [
        "importance",
        "confidence",
    ],
)
def test_from_row_rejects_missing_required_number(
    record: MemoryRecord,
    field_name: str,
) -> None:
    row = build_row(record)
    del row[field_name]

    with pytest.raises(
        ValueError,
        match=f"missing required PostgreSQL field: {field_name}",
    ):
        PostgreSQLMemorySerializer.from_row(
            row
        )


@pytest.mark.parametrize(
    ("field_name", "invalid_value"),
    [
        ("importance", "high"),
        ("importance", True),
        ("confidence", "certain"),
        ("confidence", False),
    ],
)
def test_from_row_rejects_invalid_required_number(
    record: MemoryRecord,
    field_name: str,
    invalid_value: object,
) -> None:
    row = build_row(record)
    row[field_name] = invalid_value

    with pytest.raises(
        ValueError,
        match=(
            f"PostgreSQL field '{field_name}' "
            "must be numeric"
        ),
    ):
        PostgreSQLMemorySerializer.from_row(
            row
        )


@pytest.mark.parametrize(
    "field_name",
    [
        "created_at",
        "updated_at",
    ],
)
def test_from_row_rejects_missing_datetime(
    record: MemoryRecord,
    field_name: str,
) -> None:
    row = build_row(record)
    del row[field_name]

    with pytest.raises(
        ValueError,
        match=f"missing required PostgreSQL field: {field_name}",
    ):
        PostgreSQLMemorySerializer.from_row(
            row
        )


@pytest.mark.parametrize(
    "field_name",
    [
        "created_at",
        "updated_at",
    ],
)
def test_from_row_rejects_invalid_datetime_type(
    record: MemoryRecord,
    field_name: str,
) -> None:
    row = build_row(record)
    row[field_name] = 123

    with pytest.raises(
        ValueError,
        match=(
            f"PostgreSQL field '{field_name}' "
            "must be a datetime or string"
        ),
    ):
        PostgreSQLMemorySerializer.from_row(
            row
        )


@pytest.mark.parametrize(
    "field_name",
    [
        "created_at",
        "updated_at",
    ],
)
def test_from_row_rejects_invalid_datetime_string(
    record: MemoryRecord,
    field_name: str,
) -> None:
    row = build_row(record)
    row[field_name] = "not-a-datetime"

    with pytest.raises(
        ValueError,
        match=(
            f"{field_name} must be a valid "
            "ISO-8601 datetime"
        ),
    ):
        PostgreSQLMemorySerializer.from_row(
            row
        )


@pytest.mark.parametrize(
    "field_name",
    [
        "created_at",
        "updated_at",
    ],
)
def test_from_row_rejects_naive_datetime_string(
    record: MemoryRecord,
    field_name: str,
) -> None:
    row = build_row(record)
    row[field_name] = "2026-07-19T10:30:45"

    with pytest.raises(
        ValueError,
        match=f"{field_name} must be timezone-aware",
    ):
        PostgreSQLMemorySerializer.from_row(
            row
        )


@pytest.mark.parametrize(
    "field_name",
    [
        "created_at",
        "updated_at",
    ],
)
def test_from_row_rejects_naive_datetime_object(
    record: MemoryRecord,
    field_name: str,
) -> None:
    row = build_row(record)
    row[field_name] = datetime(
        2026,
        7,
        19,
        10,
        30,
        45,
    )

    with pytest.raises(
        ValueError,
        match=f"{field_name} must be timezone-aware",
    ):
        PostgreSQLMemorySerializer.from_row(
            row
        )