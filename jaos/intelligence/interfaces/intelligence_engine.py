"""Primary engine contract for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from abc import abstractmethod

from jaos.intelligence.interfaces.intelligence_component import (
    IntelligenceComponent,
)
from jaos.intelligence.models.intelligence_request import (
    IntelligenceRequest,
)
from jaos.intelligence.models.intelligence_result import (
    IntelligenceResult,
)


class IntelligenceEngine(IntelligenceComponent):
    """
    Defines the primary provider-independent contract for the JAOS
    Intelligence Platform.

    Implementations accept validated IntelligenceRequest instances,
    coordinate the appropriate intelligence capabilities, and return a
    structured IntelligenceResult.

    This contract defines *what* an Intelligence Engine must provide,
    not *how* processing is performed. Concrete implementations may
    coordinate specialized intelligence components while preserving
    platform boundaries and without performing direct execution.
    """

    @abstractmethod
    async def process_request(
        self,
        request: IntelligenceRequest,
    ) -> IntelligenceResult:
        """
        Process an intelligence request.

        Implementations transform a validated IntelligenceRequest into a
        provider-independent IntelligenceResult while coordinating any
        required intelligence capabilities.

        Raises:
            IntelligencePlatformError:
                If the request cannot be processed.
        """

        raise NotImplementedError
