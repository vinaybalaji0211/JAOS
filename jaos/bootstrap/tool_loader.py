from jaos.tools.filesystem.copy_file_tool import CopyFileTool
from jaos.tools.filesystem.delete_file_tool import DeleteFileTool
from jaos.tools.filesystem.move_file_tool import MoveFileTool
from jaos.tools.filesystem.read_file_tool import ReadFileTool
from jaos.tools.filesystem.rename_file_tool import RenameFileTool
from jaos.tools.filesystem.search_file_tool import SearchFileTool
from jaos.tools.filesystem.write_file_tool import WriteFileTool
from jaos.tools.tool_manager import ToolManager


def grant_alpha_filesystem_permissions(tool_manager: ToolManager) -> None:
    """
    Grant Alpha-stage filesystem permissions.

    In later phases, permissions will come from the Security Platform.
    """

    tool_manager._permissions.grant("filesystem.read")
    tool_manager._permissions.grant("filesystem.write")
    tool_manager._permissions.grant("filesystem.copy")
    tool_manager._permissions.grant("filesystem.move")
    tool_manager._permissions.grant("filesystem.rename")
    tool_manager._permissions.grant("filesystem.delete")
    tool_manager._permissions.grant("filesystem.search")


def register_filesystem_tools(tool_manager: ToolManager) -> None:
    """
    Register filesystem tools with the Tool Platform.
    """

    tool_manager.register_tool(ReadFileTool())
    tool_manager.register_tool(WriteFileTool())
    tool_manager.register_tool(SearchFileTool())
    tool_manager.register_tool(CopyFileTool())
    tool_manager.register_tool(MoveFileTool())
    tool_manager.register_tool(RenameFileTool())
    tool_manager.register_tool(DeleteFileTool())


def load_tools(tool_manager: ToolManager) -> None:
    """
    Load all Alpha-stage JAOS tools.
    """

    grant_alpha_filesystem_permissions(tool_manager)
    register_filesystem_tools(tool_manager)