import pytest

from jaos_platform.service_metadata import ServiceMetadata
from jaos_platform.service_registry import ServiceRegistry


def test_register_service():
    registry = ServiceRegistry()

    registry.register(ServiceMetadata(name="memory"))

    assert registry.is_registered("memory")


def test_get_service():
    registry = ServiceRegistry()

    registry.register(ServiceMetadata(name="brain"))

    assert registry.get("brain").name == "brain"


def test_update_status():
    registry = ServiceRegistry()

    registry.register(ServiceMetadata(name="workflow"))

    registry.update_status("workflow", "STOPPED")

    assert registry.get("workflow").status == "STOPPED"


def test_duplicate_registration():
    registry = ServiceRegistry()

    registry.register(ServiceMetadata(name="memory"))

    with pytest.raises(ValueError):
        registry.register(ServiceMetadata(name="memory"))


def test_unknown_service():
    registry = ServiceRegistry()

    with pytest.raises(KeyError):
        registry.get("missing")


def test_list_services():
    registry = ServiceRegistry()

    registry.register(ServiceMetadata(name="b"))
    registry.register(ServiceMetadata(name="a"))

    assert registry.list() == ["a", "b"]