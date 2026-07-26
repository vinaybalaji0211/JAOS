"""Tests for prompt composition contracts and interface."""

import pytest

from jaos.ai.prompt import (
    PromptBuildRequest,
    PromptBuilder,
    PromptSection,
    PromptSectionType,
)
from jaos.ai.provider.provider_config import AIProviderCapability
from jaos.intelligence import (
    ContextBundle,
    IntelligenceIdentity,
    IntelligenceRequest,
    IntelligenceRequestType,
    IntelligenceScope,
)
from jaos.intelligence.interfaces.prompt_composer import (
    PromptComposer,
)
from jaos.intelligence.prompt.prompt_composer import (
    IntelligencePromptComposer,
)
from jaos.intelligence.prompt.prompt_composition_models import (
    PromptCompositionRequest,
    PromptCompositionResult,
)


def create_request() -> IntelligenceRequest:
    identity = IntelligenceIdentity(
        IntelligenceScope.USER,
        "vinay",
    )

    return IntelligenceRequest(
        objective="Explain JAOS.",
        request_type=IntelligenceRequestType.CONVERSATION,
        identity=identity,
        request_id="request-1",
    )


def create_bundle(
    request: IntelligenceRequest,
) -> ContextBundle:
    return ContextBundle(
        request_id=request.request_id,
        identity=request.identity,
        bundle_id="bundle-1",
    )


def create_section() -> PromptSection:
    return PromptSection(
        section_type=PromptSectionType.SYSTEM,
        content="Approved system instruction",
        priority=10,
    )


def compile_with_sections(
    sections: tuple[PromptSection, ...],
):
    return PromptBuilder().compile(
        PromptBuildRequest(
            user_prompt="User objective",
            sections=sections,
        )
    )


def test_prompt_composer_interface_is_abstract() -> None:
    with pytest.raises(TypeError):
        PromptComposer()


def test_concrete_composer_implements_prompt_interface() -> None:
    assert issubclass(
        IntelligencePromptComposer,
        PromptComposer,
    )


def test_composition_request_normalizes_and_copies_values() -> None:
    request = create_request()
    bundle = create_bundle(request)
    output_schema = {"type": "object"}
    metadata = {"source": "test"}

    composition_request = PromptCompositionRequest(
        request=request,
        context_bundle=bundle,
        template_id=" General ",
        template_version=" 1.0 ",
        output_schema=output_schema,
        metadata=metadata,
    )

    output_schema["type"] = "changed"
    metadata["source"] = "changed"

    assert composition_request.template_id == "General"
    assert composition_request.template_version == "1.0"
    assert composition_request.output_schema == {
        "type": "object"
    }
    assert composition_request.metadata == {"source": "test"}


def test_composition_request_rejects_empty_template_id() -> None:
    request = create_request()

    with pytest.raises(
        ValueError,
        match="template_id must not be empty",
    ):
        PromptCompositionRequest(
            request=request,
            context_bundle=create_bundle(request),
            template_id=" ",
        )


def test_composition_request_rejects_invalid_template_version() -> None:
    request = create_request()

    with pytest.raises(
        TypeError,
        match="template_version",
    ):
        PromptCompositionRequest(
            request=request,
            context_bundle=create_bundle(request),
            template_id="general",
            template_version=1,
        )


def test_composition_request_rejects_invalid_provider_config() -> None:
    request = create_request()

    with pytest.raises(
        TypeError,
        match="provider_config",
    ):
        PromptCompositionRequest(
            request=request,
            context_bundle=create_bundle(request),
            template_id="general",
            provider_config="provider",
        )


def test_composition_result_validates_and_normalizes_trace() -> None:
    section = create_section()
    compiled_prompt = compile_with_sections((section,))

    result = PromptCompositionResult(
        compiled_prompt=compiled_prompt,
        template_reference=" general@1.0 ",
        supplemental_sections=(section,),
        context_item_ids=("item-1",),
        estimated_prompt_tokens=20,
        required_provider_capabilities=(
            AIProviderCapability.CHAT,
            AIProviderCapability.CHAT,
        ),
        redacted_item_ids=("item-1",),
        contained_item_ids=("item-1",),
        metadata={"trace": True},
    )

    assert result.template_reference == "general@1.0"
    assert result.required_provider_capabilities == (
        AIProviderCapability.CHAT,
    )
    assert result.context_item_ids == ("item-1",)
    assert result.redacted_item_ids == ("item-1",)
    assert result.contained_item_ids == ("item-1",)


def test_composition_result_rejects_section_count_mismatch() -> None:
    section = create_section()
    compiled_prompt = compile_with_sections(())

    with pytest.raises(
        ValueError,
        match="section count does not match",
    ):
        PromptCompositionResult(
            compiled_prompt=compiled_prompt,
            template_reference="general@1.0",
            supplemental_sections=(section,),
            context_item_ids=(),
            estimated_prompt_tokens=10,
        )


def test_composition_result_rejects_duplicate_context_ids() -> None:
    compiled_prompt = compile_with_sections(())

    with pytest.raises(
        ValueError,
        match="must not contain duplicates",
    ):
        PromptCompositionResult(
            compiled_prompt=compiled_prompt,
            template_reference="general@1.0",
            supplemental_sections=(),
            context_item_ids=("item-1", "item-1"),
            estimated_prompt_tokens=10,
        )


def test_composition_result_rejects_unknown_redacted_id() -> None:
    compiled_prompt = compile_with_sections(())

    with pytest.raises(
        ValueError,
        match="redacted_item_ids",
    ):
        PromptCompositionResult(
            compiled_prompt=compiled_prompt,
            template_reference="general@1.0",
            supplemental_sections=(),
            context_item_ids=("item-1",),
            estimated_prompt_tokens=10,
            redacted_item_ids=("missing",),
        )


def test_composition_result_rejects_unknown_contained_id() -> None:
    compiled_prompt = compile_with_sections(())

    with pytest.raises(
        ValueError,
        match="contained_item_ids",
    ):
        PromptCompositionResult(
            compiled_prompt=compiled_prompt,
            template_reference="general@1.0",
            supplemental_sections=(),
            context_item_ids=("item-1",),
            estimated_prompt_tokens=10,
            contained_item_ids=("missing",),
        )


@pytest.mark.parametrize(
    "estimated_tokens",
    (0, True),
)
def test_composition_result_rejects_invalid_token_count(
    estimated_tokens: object,
) -> None:
    compiled_prompt = compile_with_sections(())

    expected_exception = (
        TypeError if isinstance(estimated_tokens, bool) else ValueError
    )

    with pytest.raises(expected_exception):
        PromptCompositionResult(
            compiled_prompt=compiled_prompt,
            template_reference="general@1.0",
            supplemental_sections=(),
            context_item_ids=(),
                       estimated_prompt_tokens=estimated_tokens,
        )


def test_composition_result_rejects_empty_capabilities() -> None:
    compiled_prompt = compile_with_sections(())

    with pytest.raises(
        ValueError,
        match="must not be empty",
    ):
        PromptCompositionResult(
            compiled_prompt=compiled_prompt,
            template_reference="general@1.0",
            supplemental_sections=(),
            context_item_ids=(),
            estimated_prompt_tokens=10,
            required_provider_capabilities=(),
        )


def test_composition_result_rejects_invalid_section() -> None:
    compiled_prompt = compile_with_sections(())

    with pytest.raises(
        TypeError,
        match="must be a PromptSection",
    ):
        PromptCompositionResult(
            compiled_prompt=compiled_prompt,
            template_reference="general@1.0",
            supplemental_sections=("invalid",),
            context_item_ids=(),
            estimated_prompt_tokens=10,
        )
