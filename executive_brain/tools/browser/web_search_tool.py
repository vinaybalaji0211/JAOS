"""
JAOS Web Search Tool

Phase 4 — JAOS-M-0032

Opens a web search query in the default browser.
"""

from __future__ import annotations

import urllib.parse
import webbrowser

from executive_brain.tools.core.tool_interface import ToolInterface
from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolResponse,
    ToolStatus,
)


class WebSearchTool(ToolInterface):
    """
    Tool for opening a web search query.
    """

    SEARCH_PROVIDERS = {
        "duckduckgo": "https://duckduckgo.com/?q={query}",
        "google": "https://www.google.com/search?q={query}",
        "bing": "https://www.bing.com/search?q={query}",
    }

    @property
    def tool_name(self) -> str:
        return "web_search"

    def execute(self, request: ToolRequest) -> ToolResponse:
        if not isinstance(request, ToolRequest):
            raise TypeError("request must be a ToolRequest")

        query = request.parameters.get("query")
        provider = request.parameters.get("provider", "duckduckgo")

        if not isinstance(query, str) or not query.strip():
            raise ValueError("query parameter is required")

        if not isinstance(provider, str) or not provider.strip():
            raise ValueError("provider must be a non-empty string")

        provider_key = provider.lower().strip()

        if provider_key not in self.SEARCH_PROVIDERS:
            return ToolResponse(
                status=ToolStatus.FAILURE,
                message="Unsupported search provider",
                data={
                    "provider": provider,
                    "supported_providers": sorted(self.SEARCH_PROVIDERS.keys()),
                },
            )

        encoded_query = urllib.parse.quote_plus(query.strip())
        url = self.SEARCH_PROVIDERS[provider_key].format(query=encoded_query)

        success = webbrowser.open(url)

        if not success:
            return ToolResponse(
                status=ToolStatus.FAILURE,
                message="Failed to open search",
                data={
                    "query": query,
                    "provider": provider_key,
                    "url": url,
                },
            )

        return ToolResponse(
            status=ToolStatus.SUCCESS,
            message="Search opened successfully",
            data={
                "query": query,
                "provider": provider_key,
                "url": url,
            },
        )