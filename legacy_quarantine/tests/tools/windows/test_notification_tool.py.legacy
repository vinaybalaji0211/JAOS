import ctypes

import pytest

from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolStatus,
)
from executive_brain.tools.windows.notification_tool import (
    NotificationTool,
)


class FakeUser32:
    def __init__(self):
        self.called = False
        self.args = None

    def MessageBoxW(self, hwnd, message, title, flags):
        self.called = True
        self.args = (hwnd, message, title, flags)
        return 1


def test_notification_tool_name():
    tool = NotificationTool()

    assert tool.tool_name == "notification"


def test_notification_success(monkeypatch):
    fake = FakeUser32()

    monkeypatch.setattr(
        ctypes,
        "windll",
        type("FakeWindll", (), {"user32": fake}),
        raising=False,
    )

    tool = NotificationTool()

    response = tool.execute(
        ToolRequest(
            tool_name="notification",
            parameters={
                "title": "JAOS",
                "message": "Hello",
            },
        )
    )

    assert response.status == ToolStatus.SUCCESS
    assert response.message == "Notification displayed successfully"
    assert response.data["title"] == "JAOS"
    assert response.data["message"] == "Hello"

    assert fake.called is True
    assert fake.args == (0, "Hello", "JAOS", 0)


def test_notification_default_title(monkeypatch):
    fake = FakeUser32()

    monkeypatch.setattr(
        ctypes,
        "windll",
        type("FakeWindll", (), {"user32": fake}),
        raising=False,
    )

    tool = NotificationTool()

    response = tool.execute(
        ToolRequest(
            tool_name="notification",
            parameters={
                "message": "Hello",
            },
        )
    )

    assert response.status == ToolStatus.SUCCESS
    assert response.data["title"] == "JAOS"


def test_notification_failure(monkeypatch):
    class BrokenUser32:
        def MessageBoxW(self, *args):
            raise RuntimeError("notification failed")

    monkeypatch.setattr(
        ctypes,
        "windll",
        type("FakeWindll", (), {"user32": BrokenUser32()}),
        raising=False,
    )

    tool = NotificationTool()

    response = tool.execute(
        ToolRequest(
            tool_name="notification",
            parameters={
                "message": "Hello",
            },
        )
    )

    assert response.status == ToolStatus.FAILURE
    assert response.message == "Notification failed"
    assert response.data["error"] == "notification failed"


def test_notification_requires_tool_request():
    tool = NotificationTool()

    with pytest.raises(TypeError):
        tool.execute("invalid-request")


def test_notification_requires_message():
    tool = NotificationTool()

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="notification",
                parameters={},
            )
        )


def test_notification_requires_string_title():
    tool = NotificationTool()

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="notification",
                parameters={
                    "title": 123,
                    "message": "Hello",
                },
            )
        )