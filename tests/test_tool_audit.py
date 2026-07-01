from datetime import datetime, timezone

import pytest

from jaos.tools.tool_audit import (
    ToolAuditLogger,
    ToolAuditRecord,
)


def test_audit_record_creation():
    record = ToolAuditRecord(
        tool_name="read_file",
        success=True,
    )

    assert record.tool_name == "read_file"
    assert record.success is True
    assert record.error is None
    assert isinstance(record.created_at, datetime)
    assert record.created_at.tzinfo == timezone.utc


def test_audit_record_rejects_empty_tool_name():
    with pytest.raises(ValueError):
        ToolAuditRecord(
            tool_name="",
            success=True,
        )


def test_audit_logger_records_entries():
    logger = ToolAuditLogger()

    record = ToolAuditRecord(
        tool_name="read_file",
        success=True,
    )

    logger.record(record)

    records = logger.list_records()

    assert len(records) == 1
    assert records[0] == record


def test_audit_logger_returns_tuple():
    logger = ToolAuditLogger()

    logger.record(
        ToolAuditRecord(
            tool_name="tool",
            success=True,
        )
    )

    records = logger.list_records()

    assert isinstance(records, tuple)


def test_audit_logger_preserves_order():
    logger = ToolAuditLogger()

    first = ToolAuditRecord(
        tool_name="first",
        success=True,
    )

    second = ToolAuditRecord(
        tool_name="second",
        success=False,
        error="failure",
    )

    logger.record(first)
    logger.record(second)

    records = logger.list_records()

    assert records[0] == first
    assert records[1] == second


def test_audit_logger_clear():
    logger = ToolAuditLogger()

    logger.record(
        ToolAuditRecord(
            tool_name="tool",
            success=True,
        )
    )

    assert len(logger.list_records()) == 1

    logger.clear()

    assert logger.list_records() == ()


def test_audit_record_is_immutable():
    record = ToolAuditRecord(
        tool_name="tool",
        success=True,
    )

    with pytest.raises(Exception):
        record.tool_name = "changed"