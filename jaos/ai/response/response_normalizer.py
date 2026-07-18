from jaos.ai.provider import AIResponse


class ResponseNormalizer:
    """
    Normalizes provider responses before parsing.

    The normalizer performs safe formatting cleanup only.
    It does not validate business rules.
    """

    def normalize(self, response: AIResponse) -> AIResponse:
        if not isinstance(response, AIResponse):
            raise TypeError("ResponseNormalizer expects an AIResponse instance")

        return AIResponse(
            text=response.text.strip(),
            provider=response.provider.strip().lower(),
            model=response.model.strip() if response.model is not None else None,
            metadata=dict(response.metadata or {}),
        )