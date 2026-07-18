from jaos.ai.prompt.prompt_models import (
    CompiledPrompt,
    PromptBuildRequest,
    PromptSection,
    PromptSectionType,
)


class PromptBuilder:
    """
    Builds a final prompt from ordered prompt sections.

    The builder owns formatting only. It does not know about providers,
    routing, context storage, memory storage, or executive planning.
    """

    def build(self, request: PromptBuildRequest) -> str:
        return self.compile(request).text

    def compile(self, request: PromptBuildRequest) -> CompiledPrompt:
        if not isinstance(request, PromptBuildRequest):
            raise TypeError("PromptBuilder.compile expects a PromptBuildRequest")

        sections = list(request.sections)
        sections.append(
            PromptSection(
                section_type=PromptSectionType.USER,
                content=request.user_prompt,
                priority=1000,
            )
        )

        ordered_sections = tuple(
            sorted(sections, key=lambda section: section.priority)
        )

        text = "\n\n".join(
            self._format_section(section)
            for section in ordered_sections
        )

        return CompiledPrompt(
            text=text,
            section_count=len(ordered_sections),
            metadata={
                "section_types": tuple(
                    section.section_type.value for section in ordered_sections
                ),
                **request.metadata,
            },
        )

    @staticmethod
    def _format_section(section: PromptSection) -> str:
        title = section.section_type.value.upper()
        return f"[{title}]\n{section.content}"