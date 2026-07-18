from jaos.executive.models import ExecutiveIntent, ExecutiveIntentType
from jaos.executive.parser.filesystem_parser import FilesystemIntentParser


class ExecutiveIntentParser:
    """
    Main executive intent parser.

    Delegates domain-specific parsing to specialized parsers.
    """

    def __init__(self) -> None:
        self.filesystem_parser = FilesystemIntentParser()

    def parse(self, user_input: str) -> ExecutiveIntent:
        cleaned_input = user_input.strip()

        if not cleaned_input:
            return ExecutiveIntent(
                intent_type=ExecutiveIntentType.UNKNOWN,
                confidence=0.0,
            )

        intent = self.filesystem_parser.parse(cleaned_input)

        if intent.intent_type != ExecutiveIntentType.UNKNOWN:
            return intent

        return ExecutiveIntent(
            intent_type=ExecutiveIntentType.UNKNOWN,
            confidence=0.0,
            arguments={"raw_input": user_input},
        )