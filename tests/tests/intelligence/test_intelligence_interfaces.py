"""Tests for JAOS AI Intelligence Platform interfaces."""

import inspect

import pytest

from jaos.intelligence import (
    AgentOrchestrator,
    ConversationEngine,
    ExecutionProposalBuilder,
    IntelligenceComponent,
    IntelligenceContextManager,
    IntelligenceContextSource,
    IntelligenceEngine,
    PlanningEngine,
    ReasoningEngine,
)

INTERFACE_TYPES = (
    IntelligenceComponent,
    IntelligenceContextManager,
    IntelligenceContextSource,
    ConversationEngine,
    ReasoningEngine,
    PlanningEngine,
    AgentOrchestrator,
    ExecutionProposalBuilder,
    IntelligenceEngine,
)


@pytest.mark.parametrize("interface_type", INTERFACE_TYPES)
def test_intelligence_interfaces_are_abstract(
    interface_type: type[IntelligenceComponent],
) -> None:
    assert inspect.isabstract(interface_type)


@pytest.mark.parametrize("interface_type", INTERFACE_TYPES)
def test_intelligence_interfaces_cannot_be_instantiated(
    interface_type: type[IntelligenceComponent],
) -> None:
    with pytest.raises(TypeError):
        interface_type()


@pytest.mark.parametrize(
    "interface_type",
    INTERFACE_TYPES[1:],
)
def test_component_interfaces_inherit_shared_lifecycle(
    interface_type: type[IntelligenceComponent],
) -> None:
    assert issubclass(interface_type, IntelligenceComponent)


@pytest.mark.parametrize(
    ("interface_type", "required_methods"),
    [
        (
            IntelligenceComponent,
            {
                "component_name",
                "is_ready",
                "initialize",
                "shutdown",
            },
        ),
        (
            IntelligenceContextManager,
            {
                "assemble_context",
                "validate_context",
            },
        ),
        (
            IntelligenceContextSource,
            {
                "source_name",
                "collect_context",
            },
        ),
        (
            ConversationEngine,
            {
                "start_session",
                "get_session",
                "process_turn",
                "close_session",
            },
        ),
        (
            ReasoningEngine,
            {"reason"},
        ),
        (
            PlanningEngine,
            {"create_plan"},
        ),
        (
            AgentOrchestrator,
            {
                "register_agent",
                "unregister_agent",
                "find_agents",
                "route_task",
                "record_result",
                "get_result",
            },
        ),
        (
            ExecutionProposalBuilder,
            {"build_proposal"},
        ),
        (
            IntelligenceEngine,
            {"process_request"},
        ),
    ],
)
def test_interfaces_define_required_abstract_operations(
    interface_type: type[IntelligenceComponent],
    required_methods: set[str],
) -> None:
    assert required_methods.issubset(interface_type.__abstractmethods__)


class ConcreteTestComponent(IntelligenceComponent):
    """Minimal concrete component used to verify the lifecycle contract."""

    def __init__(self) -> None:
        self._ready = False

    @property
    def component_name(self) -> str:
        return "test-component"

    @property
    def is_ready(self) -> bool:
        return self._ready

    def initialize(self) -> None:
        self._ready = True

    def shutdown(self) -> None:
        self._ready = False


def test_lifecycle_contract_can_be_implemented() -> None:
    component = ConcreteTestComponent()

    assert component.component_name == "test-component"
    assert component.is_ready is False

    component.initialize()

    assert component.is_ready is True

    component.shutdown()

    assert component.is_ready is False