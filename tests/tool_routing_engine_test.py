from brain.tool_routing_engine import (
    ToolRoutingEngine
)

router = (
    ToolRoutingEngine()
)

router.register_route(
    "PDF_ANALYSIS",
    "PDFReader"
)

router.register_route(
    "WEB_SEARCH",
    "WebSearch"
)

router.register_route(
    "PYTHON_EXECUTION",
    "PythonExecutor"
)

router.show_routes()

print(
    router.get_tool(
        "WEB_SEARCH"
    )
)