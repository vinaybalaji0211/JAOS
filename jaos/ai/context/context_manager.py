from jaos.ai.context.context_models import (
    ContextAssemblyRequest,
    ContextItem,
    ContextType,
    ConversationTurn,
)
from jaos.ai.prompt import PromptSection, PromptSectionType


class ContextManager:
    """
    Stores, filters, and assembles AI context.

    Alpha responsibilities:
    - store context items
    - store conversation turns
    - filter context by type/source
    - assemble selected context deterministically
    - convert context into prompt sections
    - act as a prompt contributor
    """

    def __init__(self) -> None:
        self._items: list[ContextItem] = []
        self._conversation: list[ConversationTurn] = []

    def add_context(self, item: ContextItem) -> None:
        if not isinstance(item, ContextItem):
            raise TypeError("ContextManager.add_context expects a ContextItem")

        self._items.append(item)

    def add_conversation_turn(
        self,
        role: str,
        content: str,
        *,
        source: str = "conversation",
    ) -> None:
        self._conversation.append(
            ConversationTurn(
                role=role,
                content=content,
                source=source,
            )
        )

    def list_context(
        self,
        *,
        context_type: ContextType | None = None,
        source: str | None = None,
    ) -> tuple[ContextItem, ...]:
        items = tuple(self._items)

        if context_type is not None:
            items = tuple(item for item in items if item.context_type == context_type)

        if source is not None:
            normalized_source = source.strip().lower()
            items = tuple(item for item in items if item.source == normalized_source)

        return items

    def list_conversation(
        self,
        *,
        role: str | None = None,
        source: str | None = None,
    ) -> tuple[ConversationTurn, ...]:
        turns = tuple(self._conversation)

        if role is not None:
            normalized_role = role.strip().lower()
            turns = tuple(turn for turn in turns if turn.role == normalized_role)

        if source is not None:
            normalized_source = source.strip().lower()
            turns = tuple(turn for turn in turns if turn.source == normalized_source)

        return turns

    def assemble_context(
        self,
        request: ContextAssemblyRequest | None = None,
    ) -> tuple[ContextItem, ...]:
        assembly_request = request or ContextAssemblyRequest()

        items = tuple(self._items)

        if assembly_request.context_types:
            allowed_types = set(assembly_request.context_types)
            items = tuple(item for item in items if item.context_type in allowed_types)

        if assembly_request.sources:
            allowed_sources = set(assembly_request.sources)
            items = tuple(item for item in items if item.source in allowed_sources)

        ordered_items = tuple(
            sorted(
                items,
                key=lambda item: (
                    item.priority,
                    item.created_at,
                    item.item_id,
                ),
            )
        )

        if assembly_request.max_items is not None:
            ordered_items = ordered_items[: assembly_request.max_items]

        return ordered_items

    def remove_context(self, item_id: str) -> bool:
        normalized_item_id = item_id.strip()

        if not normalized_item_id:
            raise ValueError("Context item ID cannot be empty")

        original_count = len(self._items)
        self._items = [
            item for item in self._items if item.item_id != normalized_item_id
        ]

        return len(self._items) != original_count

    def clear_context(self) -> None:
        self._items.clear()

    def clear_conversation(self) -> None:
        self._conversation.clear()

    def clear_all(self) -> None:
        self.clear_context()
        self.clear_conversation()

    def build_prompt_sections(
        self,
        request: ContextAssemblyRequest | None = None,
    ) -> tuple[PromptSection, ...]:
        assembly_request = request or ContextAssemblyRequest()
        sections: list[PromptSection] = []

        for item in self.assemble_context(assembly_request):
            sections.append(
                PromptSection(
                    section_type=self._map_context_type(item.context_type),
                    content=item.content,
                    priority=item.priority,
                    metadata={
                        "context_item_id": item.item_id,
                        "context_type": item.context_type.value,
                        "source": item.source,
                        **item.metadata,
                    },
                )
            )

        if assembly_request.include_conversation and self._conversation:
            conversation_text = "\n".join(
                f"{turn.role}: {turn.content}" for turn in self._conversation
            )
            sections.append(
                PromptSection(
                    section_type=PromptSectionType.CONTEXT,
                    content=conversation_text,
                    priority=500,
                    metadata={
                        "context_type": ContextType.CONVERSATION.value,
                        "source": "conversation",
                        "turn_count": len(self._conversation),
                    },
                )
            )

        return tuple(sections)

    def contribute(self) -> tuple[PromptSection, ...]:
        return self.build_prompt_sections()

    @staticmethod
    def _map_context_type(context_type: ContextType) -> PromptSectionType:
        mapping = {
            ContextType.CONVERSATION: PromptSectionType.CONTEXT,
            ContextType.MEMORY: PromptSectionType.MEMORY,
            ContextType.IDENTITY: PromptSectionType.IDENTITY,
            ContextType.ENVIRONMENT: PromptSectionType.CONTEXT,
            ContextType.TASK: PromptSectionType.CONTEXT,
            ContextType.USER: PromptSectionType.CONTEXT,
            ContextType.SYSTEM: PromptSectionType.SYSTEM,
        }

        return mapping[context_type]