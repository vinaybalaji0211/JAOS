from jaos.ai.prompt.prompt_builder import PromptBuilder
from jaos.ai.prompt.prompt_contributor import PromptContributor
from jaos.ai.prompt.prompt_models import (
    CompiledPrompt,
    PromptBuildRequest,
    PromptSection,
)


class PromptManager:
    """
    High-level prompt interface used by the AI Platform.

    PromptManager is the public entry point for prompt construction.
    It supports direct sections and registered contributors.
    """

    def __init__(
        self,
        builder: PromptBuilder | None = None,
        contributors: tuple[PromptContributor, ...] = (),
    ) -> None:
        self._builder = builder or PromptBuilder()
        self._contributors: list[PromptContributor] = list(contributors)

    def register_contributor(self, contributor: PromptContributor) -> None:
        self._contributors.append(contributor)

    def list_contributors(self) -> tuple[PromptContributor, ...]:
        return tuple(self._contributors)

    def clear_contributors(self) -> None:
        self._contributors.clear()

    def build_prompt(
        self,
        user_prompt: str,
        sections: tuple[PromptSection, ...] = (),
    ) -> str:
        request = PromptBuildRequest(
            user_prompt=user_prompt,
            sections=self._collect_sections(sections),
        )
        return self._builder.build(request)

    def compile_prompt(
        self,
        user_prompt: str,
        sections: tuple[PromptSection, ...] = (),
        metadata: dict[str, object] | None = None,
    ) -> CompiledPrompt:
        request = PromptBuildRequest(
            user_prompt=user_prompt,
            sections=self._collect_sections(sections),
            metadata=dict(metadata or {}),
        )
        return self._builder.compile(request)

    def _collect_sections(
        self,
        sections: tuple[PromptSection, ...],
    ) -> tuple[PromptSection, ...]:
        collected_sections: list[PromptSection] = []

        for contributor in self._contributors:
            contributed_sections = contributor.contribute()
            collected_sections.extend(contributed_sections)

        collected_sections.extend(sections)

        return tuple(collected_sections)