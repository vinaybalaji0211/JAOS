from jaos.tools import (
    ToolCapability,
    ToolMetadata,
)


def test_tool_metadata_supports_capabilities():
    metadata = ToolMetadata(
        name="reader",
        version="1.0.0",
        description="Reads files",
        capabilities=(
            ToolCapability.FILESYSTEM_READ,
        ),
    )

    assert metadata.capabilities == (
        ToolCapability.FILESYSTEM_READ,
    )


def test_capability_values_are_unique():
    values = [cap.value for cap in ToolCapability]

    assert len(values) == len(set(values))