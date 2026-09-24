"""
JAOS Clipboard Tool

Phase 4 — JAOS-M-0031

Reads the current clipboard text.
"""

from __future__ import annotations

import tkinter as tk

from executive_brain.tools.core.tool_interface import ToolInterface
from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolResponse,
    ToolStatus,
)


class ClipboardTool(ToolInterface):
    """
    Tool for reading clipboard text.
    """

    @property
    def tool_name(self) -> str:
        return "clipboard"

    def execute(self, request: ToolRequest) -> ToolResponse:
        if not isinstance(request, ToolRequest):
            raise TypeError("request must be a ToolRequest")

        root = tk.Tk()
        root.withdraw()

        try:
            text = root.clipboard_get()
        except tk.TclError:
            text = ""
        finally:
            root.destroy()

        return ToolResponse(
            status=ToolStatus.SUCCESS,
            message="Clipboard read successfully",
            data={
                "text": text,
                "length": len(text),
            },
        )