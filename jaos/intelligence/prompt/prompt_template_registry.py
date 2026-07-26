"""Prompt template registry for the JAOS Intelligence Platform."""

from __future__ import annotations

from threading import RLock

from jaos.intelligence.exceptions import IntelligenceValidationError
from jaos.intelligence.prompt.prompt_template import (
    IntelligencePromptTemplate,
)


def _normalize_template_id(template_id: str) -> str:
    """Validate and normalize a template identifier."""

    if not isinstance(template_id, str):
        raise TypeError("template_id must be a string")

    normalized = template_id.strip().lower()

    if not normalized:
        raise ValueError("template_id must not be empty")

    return normalized


def _normalize_version(version: str) -> str:
    """Validate and normalize a version string."""

    if not isinstance(version, str):
        raise TypeError("version must be a string")

    normalized = version.strip()

    if not normalized:
        raise ValueError("version must not be empty")

    return normalized


class PromptTemplateRegistry:
    """Thread-safe registry of versioned prompt templates."""

    def __init__(self) -> None:
        self._templates: dict[
            str,
            dict[str, IntelligencePromptTemplate],
        ] = {}
        self._default_versions: dict[str, str] = {}
        self._lock = RLock()

    def register_template(
        self,
        template: IntelligencePromptTemplate,
        *,
        make_default: bool = False,
        replace: bool = False,
    ) -> None:
        """Register one prompt template version."""

        if not isinstance(template, IntelligencePromptTemplate):
            raise TypeError(
                "template must be an IntelligencePromptTemplate"
            )

        if not isinstance(make_default, bool):
            raise TypeError("make_default must be a boolean")

        if not isinstance(replace, bool):
            raise TypeError("replace must be a boolean")

        with self._lock:
            versions = self._templates.setdefault(
                template.template_id,
                {},
            )

            if template.version in versions and not replace:
                raise IntelligenceValidationError(
                    "prompt template version already registered",
                    details={
                        "template_id": template.template_id,
                        "version": template.version,
                    },
                )

            versions[template.version] = template

            if (
                template.template_id
                not in self._default_versions
                or make_default
            ):
                self._default_versions[
                    template.template_id
                ] = template.version

    def get_template(
        self,
        template_id: str,
        version: str,
    ) -> IntelligencePromptTemplate:
        """Return an exact template version."""

        normalized_id = _normalize_template_id(template_id)
        normalized_version = _normalize_version(version)

        with self._lock:
            template = self._templates.get(
                normalized_id,
                {},
            ).get(normalized_version)

        if template is None:
            raise IntelligenceValidationError(
                "prompt template version not found",
                details={
                    "template_id": normalized_id,
                    "version": normalized_version,
                },
            )

        return template

    def resolve_template(
        self,
        template_id: str,
        version: str | None = None,
    ) -> IntelligencePromptTemplate:
        """Resolve an exact or default template version."""

        normalized_id = _normalize_template_id(template_id)

        if version is not None:
            return self.get_template(normalized_id, version)

        with self._lock:
            default_version = self._default_versions.get(
                normalized_id
            )

        if default_version is None:
            raise IntelligenceValidationError(
                "prompt template not found",
                details={"template_id": normalized_id},
            )

        return self.get_template(
            normalized_id,
            default_version,
        )

    def set_default_version(
        self,
        template_id: str,
        version: str,
    ) -> None:
        """Set the default version of a registered template."""

        template = self.get_template(template_id, version)

        with self._lock:
            self._default_versions[
                template.template_id
            ] = template.version

    def unregister_template(
        self,
        template_id: str,
        version: str,
    ) -> IntelligencePromptTemplate:
        """Remove and return one template version."""

        normalized_id = _normalize_template_id(template_id)
        normalized_version = _normalize_version(version)

        with self._lock:
            versions = self._templates.get(normalized_id)

            if (
                versions is None
                or normalized_version not in versions
            ):
                raise IntelligenceValidationError(
                    "prompt template version not found",
                    details={
                        "template_id": normalized_id,
                        "version": normalized_version,
                    },
                )

            template = versions.pop(normalized_version)

            if not versions:
                self._templates.pop(normalized_id)
                self._default_versions.pop(normalized_id, None)
            elif (
                self._default_versions.get(normalized_id)
                == normalized_version
            ):
                self._default_versions[normalized_id] = sorted(
                    versions
                )[-1]

        return template

    def list_templates(
        self,
        template_id: str | None = None,
    ) -> tuple[IntelligencePromptTemplate, ...]:
        """Return registered templates in deterministic order."""

        with self._lock:
            if template_id is None:
                templates = [
                    template
                    for versions in self._templates.values()
                    for template in versions.values()
                ]
            else:
                normalized_id = _normalize_template_id(
                    template_id
                )
                templates = list(
                    self._templates.get(
                        normalized_id,
                        {},
                    ).values()
                )

        return tuple(
            sorted(
                templates,
                key=lambda template: (
                    template.template_id,
                    template.version,
                ),
            )
        )

    def contains(
        self,
        template_id: str,
        version: str | None = None,
    ) -> bool:
        """Return whether a template or exact version exists."""

        normalized_id = _normalize_template_id(template_id)

        with self._lock:
            if version is None:
                return normalized_id in self._templates

            normalized_version = _normalize_version(version)

            return normalized_version in self._templates.get(
                normalized_id,
                {},
            )

    def __len__(self) -> int:
        """Return the total number of template versions."""

        with self._lock:
            return sum(
                len(versions)
                for versions in self._templates.values()
            )