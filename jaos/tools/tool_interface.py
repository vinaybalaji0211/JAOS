from abc import ABC, abstractmethod

from jaos.tools.tool_models import ToolMetadata, ToolRequest, ToolResult


class ToolInterface(ABC):
    """
    Base contract for all JAOS tools.

    Tools execute work. They do not make strategic decisions.
    """

    @abstractmethod
    def metadata(self) -> ToolMetadata:
        """Return tool metadata."""

    @abstractmethod
    def execute(self, request: ToolRequest) -> ToolResult:
        """Execute the tool request."""