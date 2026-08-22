from jaos.executive.diagnostics.executive_status import ExecutiveStatusProvider
from jaos.executive.intent_registry import ExecutiveIntentRegistry


class FakeHandler:
    def can_handle(self, intent):
        return True

    def create_plan(self, intent):
        raise NotImplementedError


def test_status_is_unhealthy_with_no_registered_handlers():
    registry = ExecutiveIntentRegistry()

    status = ExecutiveStatusProvider(registry).get_status()

    assert status.healthy is False


def test_status_is_healthy_with_a_registered_handler():
    registry = ExecutiveIntentRegistry()
    registry.register(FakeHandler())

    status = ExecutiveStatusProvider(registry).get_status()

    assert status.healthy is True


def test_status_details_still_surface_parser_and_execution_reports():
    registry = ExecutiveIntentRegistry()

    status = ExecutiveStatusProvider(registry).get_status()

    assert "parser" in status.details
    assert "execution" in status.details
