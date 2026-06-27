from brain.tool_audit_logger import (
    ToolAuditLogger
)

audit = (
    ToolAuditLogger()
)

audit.log_action(
    "WebSearch",
    "Search AI research papers"
)

audit.log_action(
    "PythonExecutor",
    "Generate metrics report"
)

audit.log_action(
    "PDFReader",
    "Read quantum paper"
)

audit.show_logs()