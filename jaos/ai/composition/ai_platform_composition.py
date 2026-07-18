from dataclasses import dataclass

from jaos.ai.context import ContextManager
from jaos.ai.prompt import PromptManager
from jaos.ai.provider import ProviderManager
from jaos.ai.response import ResponseManager
from jaos.ai.routing import ProviderRouter


@dataclass(slots=True)
class AIPlatformComposition:
    """
    Internal composition root for the AI Platform.

    This object owns references to the core AI Platform managers.
    It does not contain business logic. Its responsibility is to
    centralize dependency wiring while keeping AIManager as the
    single public entry point.
    """

    provider_manager: ProviderManager
    context_manager: ContextManager
    prompt_manager: PromptManager
    provider_router: ProviderRouter
    response_manager: ResponseManager