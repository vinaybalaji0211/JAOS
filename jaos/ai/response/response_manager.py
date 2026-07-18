from jaos.ai.provider import AIResponse
from jaos.ai.response.response_models import ParsedResponse
from jaos.ai.response.response_normalizer import ResponseNormalizer
from jaos.ai.response.response_parser import ResponseParser
from jaos.ai.response.response_validator import ResponseValidator


class ResponseManager:
    """
    Public interface for the Response Platform.

    Pipeline:
    validate -> normalize -> parse -> ParsedResponse
    """

    def __init__(
        self,
        *,
        validator: ResponseValidator | None = None,
        normalizer: ResponseNormalizer | None = None,
        parser: ResponseParser | None = None,
    ) -> None:
        self._validator = validator or ResponseValidator()
        self._normalizer = normalizer or ResponseNormalizer()
        self._parser = parser or ResponseParser()

    def process(self, response: AIResponse) -> ParsedResponse:
        self._validator.validate(response)
        normalized_response = self._normalizer.normalize(response)
        return self._parser.parse(normalized_response)