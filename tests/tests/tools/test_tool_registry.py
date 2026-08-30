"""Canonical ToolRegistry requirements.

FORTRESS-06D2B migrated these requirements off the retired
``executive_brain.tools.core`` Tool Platform onto ``jaos.tools``. The legacy
payload is preserved byte-identically at
``legacy_quarantine/tests/tools/core/test_tool_registry.py.legacy``.

Canonical mapping notes:

- Legacy duplicate registration raised ``ValueError``; canonical registration
  raises ``ToolAlreadyRegisteredError``.
- Legacy missing lookup raised ``KeyError``; canonical lookup raises
  ``ToolNotFoundError``.
- Legacy ``list_tools`` returned a ``list``; canonical enumeration returns a
  sorted ``tuple``.
- Legacy ``count()`` has no canonical method. The requirement survives as the
  length of the canonical enumeration.
- Legacy registry identity was the raw tool name. Canonical identity is the
  stripped, lower-cased tool name from ``metadata()``.
"""

import pytest

from jaos.tools import (
    ToolAlreadyRegisteredError,
    ToolInterface,
    ToolMetadata,
    ToolNotFoundError,
    ToolRegistry,
    ToolRequest,
    ToolResult,
)


class RegistryProbeTool(ToolInterface):
    """Minimal canonical tool with a caller-supplied identity."""

    def __init__(self, name: str = "dummy") -> None:
        self._name = name

    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name=self._name,
            version="1.0.0",
            description="Registry probe tool",
        )

    def execute(self, request: ToolRequest) -> ToolResult:
        return ToolResult(success=True, output=request.payload)


def test_new_registry_is_empty():
    """A fresh registry holds nothing."""

    registry = ToolRegistry()

    assert registry.list_tools() == ()
    assert registry.has("dummy") is False


def test_register_tool_preserves_lookup_identity():
    """Registration makes the exact tool instance retrievable by name."""

    registry = ToolRegistry()
    tool = RegistryProbeTool()

    registry.register(tool)

    assert registry.has("dummy") is True
    assert registry.get("dummy") is tool


def test_register_duplicate_tool():
    """A tool name may be registered only once."""

    registry = ToolRegistry()
    tool = RegistryProbeTool()

    registry.register(tool)

    with pytest.raises(ToolAlreadyRegisteredError):
        registry.register(tool)


def test_get_missing_tool():
    """Missing lookups fail with the canonical registry error."""

    registry = ToolRegistry()

    with pytest.raises(ToolNotFoundError):
        registry.get("missing")


def test_list_tools_enumerates_registered_names_in_sorted_order():
    """Enumeration returns every registered name, sorted, as a tuple."""

    registry = ToolRegistry()

    registry.register(RegistryProbeTool("write"))
    registry.register(RegistryProbeTool("read"))

    assert registry.list_tools() == ("read", "write")
    assert len(registry.list_tools()) == 2
