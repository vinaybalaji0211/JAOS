import webbrowser

import pytest

from executive_brain.tools.browser.web_search_tool import WebSearchTool
from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolStatus,
)


def test_web_search_tool_name():
    tool = WebSearchTool()

    assert tool.tool_name == "web_search"


def test_web_search_default_provider(monkeypatch):
    opened = {}

    def fake_open(url):
        opened["url"] = url
        return True

    monkeypatch.setattr(webbrowser, "open", fake_open)

    tool = WebSearchTool()

    response = tool.execute(
        ToolRequest(
            tool_name="web_search",
            parameters={
                "query": "jarvis ai",
            },
        )
    )

    assert response.status == ToolStatus.SUCCESS
    assert response.message == "Search opened successfully"
    assert response.data["provider"] == "duckduckgo"
    assert "jarvis+ai" in opened["url"]


def test_web_search_google(monkeypatch):
    opened = {}

    def fake_open(url):
        opened["url"] = url
        return True

    monkeypatch.setattr(webbrowser, "open", fake_open)

    tool = WebSearchTool()

    response = tool.execute(
        ToolRequest(
            tool_name="web_search",
            parameters={
                "query": "python",
                "provider": "google",
            },
        )
    )

    assert response.status == ToolStatus.SUCCESS
    assert "google.com" in opened["url"]


def test_web_search_bing(monkeypatch):
    opened = {}

    def fake_open(url):
        opened["url"] = url
        return True

    monkeypatch.setattr(webbrowser, "open", fake_open)

    tool = WebSearchTool()

    response = tool.execute(
        ToolRequest(
            tool_name="web_search",
            parameters={
                "query": "openai",
                "provider": "bing",
            },
        )
    )

    assert response.status == ToolStatus.SUCCESS
    assert "bing.com" in opened["url"]


def test_web_search_unknown_provider():
    tool = WebSearchTool()

    response = tool.execute(
        ToolRequest(
            tool_name="web_search",
            parameters={
                "query": "test",
                "provider": "unknown",
            },
        )
    )

    assert response.status == ToolStatus.FAILURE
    assert response.message == "Unsupported search provider"
    assert "google" in response.data["supported_providers"]


def test_web_search_browser_failure(monkeypatch):
    monkeypatch.setattr(webbrowser, "open", lambda url: False)

    tool = WebSearchTool()

    response = tool.execute(
        ToolRequest(
            tool_name="web_search",
            parameters={
                "query": "jarvis",
            },
        )
    )

    assert response.status == ToolStatus.FAILURE
    assert response.message == "Failed to open search"


def test_web_search_requires_tool_request():
    tool = WebSearchTool()

    with pytest.raises(TypeError):
        tool.execute("invalid-request")


def test_web_search_requires_query():
    tool = WebSearchTool()

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="web_search",
                parameters={},
            )
        )


def test_web_search_requires_provider_string():
    tool = WebSearchTool()

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="web_search",
                parameters={
                    "query": "jarvis",
                    "provider": "",
                },
            )
        )