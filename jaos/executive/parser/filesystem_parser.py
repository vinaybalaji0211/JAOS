from jaos.executive.intent_vocabulary import (
    BACKUP_FILE_ALIASES,
    COPY_FILE_ALIASES,
    DELETE_FILE_ALIASES,
    MOVE_FILE_ALIASES,
    READ_FILE_ALIASES,
    RENAME_FILE_ALIASES,
    SEARCH_FILE_ALIASES,
    WRITE_FILE_ALIASES,
    matches,
)
from jaos.executive.models import ExecutiveIntent, ExecutiveIntentType
from jaos.executive.parser.parser_helpers import (
    parse_delete_intent,
    parse_path_intent,
    parse_rename_intent,
    parse_search_intent,
    parse_two_path_intent,
    parse_write_intent,
    unknown,
)


class FilesystemIntentParser:
    """
    Parses filesystem-related user input into executive intents.
    """

    def parse(self, cleaned_input: str) -> ExecutiveIntent:
        if matches(cleaned_input, READ_FILE_ALIASES):
            return parse_path_intent(
                cleaned_input,
                ExecutiveIntentType.READ_FILE,
            )

        if matches(cleaned_input, WRITE_FILE_ALIASES):
            return parse_write_intent(cleaned_input)

        if matches(cleaned_input, COPY_FILE_ALIASES):
            return parse_two_path_intent(
                cleaned_input,
                ExecutiveIntentType.COPY_FILE,
            )

        if matches(cleaned_input, MOVE_FILE_ALIASES):
            return parse_two_path_intent(
                cleaned_input,
                ExecutiveIntentType.MOVE_FILE,
            )

        if matches(cleaned_input, RENAME_FILE_ALIASES):
            return parse_rename_intent(cleaned_input)

        if matches(cleaned_input, DELETE_FILE_ALIASES):
            return parse_delete_intent(cleaned_input)

        if matches(cleaned_input, SEARCH_FILE_ALIASES):
            return parse_search_intent(cleaned_input)

        if matches(cleaned_input, BACKUP_FILE_ALIASES):
            return parse_two_path_intent(
                cleaned_input,
                ExecutiveIntentType.BACKUP_FILE,
            )

        return unknown(cleaned_input)