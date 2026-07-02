from jaos.executive.intent_vocabulary import (
    READ_FILE_ALIASES,
    matches,
)


def test_matches_read() -> None:
    assert matches("read README.md", READ_FILE_ALIASES)


def test_matches_open() -> None:
    assert matches("open README.md", READ_FILE_ALIASES)


def test_matches_show() -> None:
    assert matches("show README.md", READ_FILE_ALIASES)


def test_matches_display() -> None:
    assert matches("display README.md", READ_FILE_ALIASES)


def test_non_matching_command() -> None:
    assert not matches("copy README.md", READ_FILE_ALIASES)