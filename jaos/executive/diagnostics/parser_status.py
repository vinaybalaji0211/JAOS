from jaos.executive.diagnostics.models import DiagnosticStatus
from jaos.executive.parser.filesystem_parser import FilesystemIntentParser


class ParserStatusProvider:
    """
    Reports diagnostics for the Executive Parser.
    """

    def __init__(self) -> None:
        self.filesystem_parser = FilesystemIntentParser()

    def get_status(self) -> DiagnosticStatus:
        return DiagnosticStatus(
            component="Executive Parser",
            healthy=True,
            message="Parser is operational.",
            details={
                "loaded_parsers": [
                    "FilesystemIntentParser",
                ],
                "parser_count": 1,
            },
        )