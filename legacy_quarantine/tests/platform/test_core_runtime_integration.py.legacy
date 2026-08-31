from core.engine import JarvisEngine
from jaos_platform.platform_runtime import PlatformRuntime


def test_engine_accepts_platform_runtime():
    runtime = PlatformRuntime()

    engine = JarvisEngine(runtime=runtime)

    assert engine.runtime is runtime


def test_engine_registers_itself_in_container():
    runtime = PlatformRuntime()

    engine = JarvisEngine(runtime=runtime)

    assert runtime.container.resolve("jarvis_engine") is engine


def test_engine_updates_runtime_context():
    runtime = PlatformRuntime()

    JarvisEngine(runtime=runtime)

    assert runtime.context.get("engine_status") == "INITIALIZED"