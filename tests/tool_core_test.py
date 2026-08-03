from brain.tool_core import ToolCore

core = ToolCore()

core.register_tool(
    "PDFReader",
    "Reads PDF documents"
)

core.register_tool(
    "WebSearch",
    "Searches the internet"
)

core.register_tool(
    "PythonExecutor",
    "Executes Python code"
)

core.show_tools()

print(
    core.get_tool(
        "WebSearch"
    )
)