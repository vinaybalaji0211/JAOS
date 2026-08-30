from pathlib import Path

import pytest

from executive_brain.tools.browser.cookies_tool import CookiesTool
from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolStatus,
)


def test_cookies_tool_name():
    tool = CookiesTool()

    assert tool.tool_name == "cookies"


def test_cookies_success(monkeypatch):
    cookie_paths = {
        "chrome": Path("chrome"),
        "edge": Path("edge"),
        "brave": Path("brave"),
    }

    monkeypatch.setattr(
        CookiesTool,
        "COOKIE_PATHS",
        cookie_paths,
    )

    monkeypatch.setattr(
        Path,
        "exists",
        lambda self: self.name == "chrome",
    )

    tool = CookiesTool()

    response = tool.execute(
        ToolRequest(tool_name="cookies")
    )

    assert response.status == ToolStatus.SUCCESS
    assert response.message == "Cookie locations inspected successfully"

    browsers = response.data["browsers"]

    assert len(browsers) == 3

    assert browsers[0]["browser"] == "chrome"
    assert browsers[0]["available"] is True

    assert browsers[1]["browser"] == "edge"
    assert browsers[1]["available"] is False


def test_cookies_requires_tool_request():
    tool = CookiesTool()

    with pytest.raises(TypeError):
        tool.execute("invalid-request")