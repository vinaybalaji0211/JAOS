from jaos_platform.platform_runtime import PlatformRuntime
from knowledge.knowledge_base import KnowledgeBase


def test_knowledge_base_registers_with_runtime():
    runtime = PlatformRuntime()

    knowledge = KnowledgeBase(runtime)

    assert runtime.container.resolve("knowledge_base") is knowledge


def test_knowledge_base_updates_runtime_context():
    runtime = PlatformRuntime()

    KnowledgeBase(runtime)

    assert runtime.context.get("knowledge_base_status") == "READY"


def test_knowledge_entry_still_works():
    runtime = PlatformRuntime()

    knowledge = KnowledgeBase(runtime)
    knowledge.add_entry("JAOS", "AI operating system")

    assert knowledge.entries["JAOS"] == "AI operating system"