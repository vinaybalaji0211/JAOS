from jaos.tools.tool_interface import ToolInterface


class ToolRegistryError(Exception):
    """Base exception for tool registry errors."""


class ToolAlreadyRegisteredError(ToolRegistryError):
    """Raised when a tool is registered more than once."""


class ToolNotFoundError(ToolRegistryError):
    """Raised when a requested tool does not exist."""


class ToolRegistry:
    """
    Stores registered JAOS tools.
    """

    def __init__(self) -> None:
        self._tools: dict[str, ToolInterface] = {}

    def register(self, tool: ToolInterface) -> None:
        name = tool.metadata().name.strip().lower()

        if name in self._tools:
            raise ToolAlreadyRegisteredError(f"Tool already registered: {name}")

        self._tools[name] = tool

    def get(self, name: str) -> ToolInterface:
        normalized_name = name.strip().lower()

        if normalized_name not in self._tools:
            raise ToolNotFoundError(f"Tool not found: {normalized_name}")

        return self._tools[normalized_name]

    def has(self, name: str) -> bool:
        return name.strip().lower() in self._tools

    def list_tools(self) -> tuple[str, ...]:
        return tuple(sorted(self._tools.keys()))