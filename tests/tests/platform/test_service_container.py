import pytest

from jaos_platform.service_container import ServiceContainer


def test_register_service():
    container = ServiceContainer()
    obj = object()

    container.register("memory", obj)

    assert container.resolve("memory") is obj


def test_is_registered():
    container = ServiceContainer()

    container.register("brain", object())

    assert container.is_registered("brain")


def test_list_services():
    container = ServiceContainer()

    container.register("a", object())
    container.register("b", object())

    assert container.list_services() == ["a", "b"]


def test_duplicate_service_rejected():
    container = ServiceContainer()

    container.register("memory", object())

    with pytest.raises(ValueError):
        container.register("memory", object())


def test_unknown_service_rejected():
    container = ServiceContainer()

    with pytest.raises(KeyError):
        container.resolve("missing")


def test_unregister_removes_service():
    container = ServiceContainer()

    container.register("memory", object())
    container.unregister("memory")

    assert container.is_registered("memory") is False


def test_unregister_unknown_service_rejected():
    container = ServiceContainer()

    with pytest.raises(KeyError):
        container.unregister("missing")