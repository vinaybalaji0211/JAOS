"""
JAOS Services Tool

Phase 4 — JAOS-M-0031

Lists Windows services using the built-in sc command.
"""

from __future__ import annotations

import subprocess

from executive_brain.tools.core.tool_interface import ToolInterface
from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolResponse,
    ToolStatus,
)


class ServicesTool(ToolInterface):
    """
    Tool for listing Windows services.
    """

    @property
    def tool_name(self) -> str:
        return "services"

    def execute(self, request: ToolRequest) -> ToolResponse:
        if not isinstance(request, ToolRequest):
            raise TypeError("request must be a ToolRequest")

        try:
            completed = subprocess.run(
                ["sc", "query", "type=", "service", "state=", "all"],
                capture_output=True,
                text=True,
                check=False,
            )
        except OSError as error:
            return ToolResponse(
                status=ToolStatus.FAILURE,
                message="Failed to list services",
                data={"error": str(error)},
            )

        if completed.returncode != 0:
            return ToolResponse(
                status=ToolStatus.FAILURE,
                message="Service listing failed",
                data={
                    "returncode": completed.returncode,
                    "stderr": completed.stderr,
                },
            )

        services = self._parse_services_output(completed.stdout)

        return ToolResponse(
            status=ToolStatus.SUCCESS,
            message="Services listed successfully",
            data={
                "count": len(services),
                "services": services,
            },
        )

    def _parse_services_output(self, output: str) -> list[dict[str, str]]:
        services: list[dict[str, str]] = []
        current: dict[str, str] = {}

        for line in output.splitlines():
            stripped = line.strip()

            if stripped.startswith("SERVICE_NAME:"):
                if current:
                    services.append(current)

                current = {
                    "service_name": stripped.replace("SERVICE_NAME:", "").strip()
                }

            elif stripped.startswith("DISPLAY_NAME:") and current:
                current["display_name"] = stripped.replace(
                    "DISPLAY_NAME:",
                    "",
                ).strip()

            elif stripped.startswith("STATE") and current:
                parts = stripped.split(":", 1)

                if len(parts) == 2:
                    current["state"] = parts[1].strip()

        if current:
            services.append(current)

        return services