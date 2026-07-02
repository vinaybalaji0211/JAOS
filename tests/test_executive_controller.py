from pathlib import Path

from jaos.bootstrap.tool_loader import load_tools
from jaos.executive.controller import ExecutiveController
from jaos.tools.tool_manager import ToolManager


def test_read_file_workflow(tmp_path: Path) -> None:
    sample = tmp_path / "sample.txt"
    sample.write_text("hello jaos", encoding="utf-8")

    manager = ToolManager()
    load_tools(manager)

    controller = ExecutiveController(manager)

    response = controller.process(f"read {sample}")

    assert response.success
    assert response.output["content"] == "hello jaos"


def test_open_alias(tmp_path: Path) -> None:
    sample = tmp_path / "sample.txt"
    sample.write_text("alias works", encoding="utf-8")

    manager = ToolManager()
    load_tools(manager)

    controller = ExecutiveController(manager)

    response = controller.process(f"open {sample}")

    assert response.success
    assert response.output["content"] == "alias works"


def test_unknown_command() -> None:
    manager = ToolManager()
    load_tools(manager)

    controller = ExecutiveController(manager)

    response = controller.process("hello")

    assert not response.success