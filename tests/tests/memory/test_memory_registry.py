import pytest

from executive_brain.memory.memory_registry import MemoryRegistry
from executive_brain.memory.working_memory import WorkingMemory


def test_registry_initializes():
    registry = MemoryRegistry()
    assert registry.count() == 0


def test_add_memory():
    registry = MemoryRegistry()
    memory = WorkingMemory()

    registry.add_memory(memory)

    assert registry.count() == 1


def test_get_memory():
    registry = MemoryRegistry()
    memory = WorkingMemory()

    registry.add_memory(memory)

    assert registry.get_memory() == memory


def test_update_memory():
    registry = MemoryRegistry()
    memory = WorkingMemory()

    registry.add_memory(memory)
    memory.set_user_request("Open Chrome")
    registry.update_memory(memory)

    assert registry.get_memory().current_user_request == "Open Chrome"


def test_remove_memory():
    registry = MemoryRegistry()
    memory = WorkingMemory()

    registry.add_memory(memory)
    removed = registry.remove_memory()

    assert removed == memory
    assert registry.count() == 0


def test_has_memory():
    registry = MemoryRegistry()

    assert registry.has_memory() is False

    registry.add_memory(WorkingMemory())

    assert registry.has_memory() is True


def test_invalid_memory():
    registry = MemoryRegistry()

    with pytest.raises(TypeError):
        registry.add_memory("invalid")