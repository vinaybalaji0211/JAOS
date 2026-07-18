from jaos.executive.models import (
    ExecutiveIntent,
    ExecutiveIntentType,
)


def unknown(raw_input: str) -> ExecutiveIntent:
    return ExecutiveIntent(
        intent_type=ExecutiveIntentType.UNKNOWN,
        confidence=0.0,
        arguments={"raw_input": raw_input},
    )


def parse_path_intent(
    cleaned_input: str,
    intent_type: ExecutiveIntentType,
) -> ExecutiveIntent:
    first_space = cleaned_input.find(" ")

    if first_space == -1:
        return unknown(cleaned_input)

    path = cleaned_input[first_space + 1:].strip()

    return ExecutiveIntent(
        intent_type=intent_type,
        confidence=1.0,
        arguments={"path": path},
    )


def parse_two_path_intent(
    cleaned_input: str,
    intent_type: ExecutiveIntentType,
) -> ExecutiveIntent:
    parts = cleaned_input.split(maxsplit=2)

    if len(parts) < 3:
        return unknown(cleaned_input)

    return ExecutiveIntent(
        intent_type=intent_type,
        confidence=1.0,
        arguments={
            "source": parts[1],
            "destination": parts[2],
        },
    )


def parse_write_intent(
    cleaned_input: str,
) -> ExecutiveIntent:
    parts = cleaned_input.split(maxsplit=2)

    if len(parts) < 3:
        return unknown(cleaned_input)

    return ExecutiveIntent(
        intent_type=ExecutiveIntentType.WRITE_FILE,
        confidence=1.0,
        arguments={
            "path": parts[1],
            "content": parts[2],
        },
    )


def parse_rename_intent(
    cleaned_input: str,
) -> ExecutiveIntent:
    parts = cleaned_input.split(maxsplit=2)

    if len(parts) < 3:
        return unknown(cleaned_input)

    return ExecutiveIntent(
        intent_type=ExecutiveIntentType.RENAME_FILE,
        confidence=1.0,
        arguments={
            "source": parts[1],
            "new_name": parts[2],
        },
    )


def parse_delete_intent(
    cleaned_input: str,
) -> ExecutiveIntent:
    parts = cleaned_input.split()

    if len(parts) < 2:
        return unknown(cleaned_input)

    approved = "--confirm" in parts
    path_parts = [p for p in parts[1:] if p != "--confirm"]

    if len(path_parts) != 1:
        return unknown(cleaned_input)

    return ExecutiveIntent(
        intent_type=ExecutiveIntentType.DELETE_FILE,
        confidence=1.0,
        arguments={
            "path": path_parts[0],
            "approved": approved,
        },
    )


def parse_search_intent(
    cleaned_input: str,
) -> ExecutiveIntent:
    parts = cleaned_input.split(maxsplit=2)

    if len(parts) < 3:
        return unknown(cleaned_input)

    return ExecutiveIntent(
        intent_type=ExecutiveIntentType.SEARCH_FILE,
        confidence=1.0,
        arguments={
            "root": parts[1],
            "pattern": parts[2],
        },
    )