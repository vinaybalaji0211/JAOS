from jaos.tools.tool_models import ToolMetadata


class ToolPermissionError(Exception):
    """Raised when tool permission validation fails."""


class ToolPermissionManager:
    """
    Validates whether a tool is allowed to execute.

    Alpha implementation supports an allow-list permission model.
    """

    def __init__(self, allowed_permissions: tuple[str, ...] = ()) -> None:
        self._allowed_permissions = set(allowed_permissions)

    def authorize(self, metadata: ToolMetadata) -> None:
        missing_permissions = [
            permission
            for permission in metadata.permissions
            if permission not in self._allowed_permissions
        ]

        if missing_permissions:
            raise ToolPermissionError(
                "Missing tool permissions: "
                + ", ".join(sorted(missing_permissions))
            )

    def grant(self, permission: str) -> None:
        normalized = permission.strip()

        if not normalized:
            raise ValueError("Permission cannot be empty")

        self._allowed_permissions.add(normalized)

    def revoke(self, permission: str) -> None:
        self._allowed_permissions.discard(permission.strip())

    def list_permissions(self) -> tuple[str, ...]:
        return tuple(sorted(self._allowed_permissions))