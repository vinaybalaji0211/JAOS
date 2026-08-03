from brain.tool_registry import ToolRegistry

registry = (
    ToolRegistry()
)

registry.register(
    "PDFReader",
    "DOCUMENT",
    "Reads PDF files"
)

registry.register(
    "WebSearch",
    "INTERNET",
    "Searches the web"
)

registry.register(
    "PythonExecutor",
    "EXECUTION",
    "Runs Python code"
)

registry.show_registry()

print(
    registry.get_tool(
        "WebSearch"
    )
)