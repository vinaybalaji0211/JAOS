import webbrowser

import pytest

from executive_brain.tools.browser.downloads_tool import DownloadsTool
from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolStatus,
)


def test_downloads_tool_name():
    tool = DownloadsTool()

    assert tool.tool_name == "downloads"


def test_downloads_chrome(monkeypatch):
    opened = {}

    def fake_open(url):
        opened["url"] = url
        return True

    monkeypatch.setattr(webbrowser, "open", fake_open)

    tool = DownloadsTool()

    response = tool.execute(
        ToolRequest(
            tool_name="downloads",
            parameters={"provider": "chrome"},
        )
    )

    assert response.status == ToolStatus.SUCCESS
    assert response.message == "Downloads page opened successfully"
    assert response.data["provider"] == "chrome"
    assert opened["url"] == "chrome://downloads/"


def test_downloads_edge(monkeypatch):
    opened = {}

    monkeypatch.setattr(
        webbrowser,
        "open",
        lambda url: opened.setdefault("url", url) or True,
    )

    tool = DownloadsTool()

    response = tool.execute(
        ToolRequest(
            tool_name="downloads",
            parameters={"provider": "edge"},
        )
    )

    assert response.status == ToolStatus.SUCCESS
    assert opened["url"] == "edge://downloads/"


def test_downloads_brave(monkeypatch):
    opened = {}

    monkeypatch.setattr(
        webbrowser,
        "open",
        lambda url: opened.setdefault("url", url) or True,
    )

    tool = DownloadsTool()

    response = tool.execute(
        ToolRequest(
            tool_name="downloads",
            parameters={"provider": "brave"},
        )
    )

    assert response.status == ToolStatus.SUCCESS
    assert opened["url"] == "brave://downloads/"


def test_downloads_unknown_provider():
    tool = DownloadsTool()

    response = tool.execute(
        ToolRequest(
            tool_name="downloads",
            parameters={"provider": "unknown"},
        )
    )

    assert response.status == ToolStatus.FAILURE
    assert response.message == "Unsupported browser provider"
    assert "chrome" in response.data["supported_providers"]


def test_downloads_browser_failure(monkeypatch):
    monkeypatch.setattr(webbrowser, "open", lambda url: False)

    tool = DownloadsTool()

    response = tool.execute(
        ToolRequest(
            tool_name="downloads",
            parameters={"provider": "chrome"},
        )
    )

    assert response.status == ToolStatus.FAILURE
    assert response.message == "Failed to open downloads page"


def test_downloads_requires_tool_request():
    tool = DownloadsTool()

    with pytest.raises(TypeError):
        tool.execute("invalid-request")


def test_downloads_requires_provider_string():
    tool = DownloadsTool()

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="downloads",
                parameters={"provider": ""},
            )
        )