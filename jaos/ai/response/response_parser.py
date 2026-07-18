from jaos.ai.provider import AIResponse
from jaos.ai.response.response_models import (
    ParsedResponse,
    ResponseFinishReason,
    ResponseMetadata,
)


class ResponseParser:
    """
    Converts normalized provider responses into a standardized response model.

    Validation and normalization are handled before parsing by ResponseManager.
    """

    def parse(self, response: AIResponse) -> ParsedResponse:
        if not isinstance(response, AIResponse):
            raise TypeError("ResponseParser expects an AIResponse instance")

        source_metadata = dict(response.metadata)

        metadata = ResponseMetadata(
            provider=response.provider,
            model=response.model,
            latency_seconds=source_metadata.get("latency_seconds"),
            token_count=source_metadata.get("token_count"),
            finish_reason=source_metadata.get(
                "finish_reason",
                ResponseFinishReason.UNKNOWN,
            ),
            source_metadata=source_metadata,
        )

        return ParsedResponse(
            text=response.text,
            metadata=metadata,
        )