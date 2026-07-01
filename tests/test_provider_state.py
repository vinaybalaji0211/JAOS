import pytest

from jaos.ai.provider import AIProviderLifecycleState, AIProviderState


def test_provider_state_normalizes_name():
    state = AIProviderState(name="  OpenAI  ")

    assert state.name == "openai"


def test_provider_state_rejects_empty_name():
    with pytest.raises(ValueError):
        AIProviderState(name="   ")


def test_provider_state_defaults():
    state = AIProviderState(name="mock")

    assert state.lifecycle == AIProviderLifecycleState.CREATED
    assert state.enabled is True
    assert state.available is False
    assert state.healthy is False
    assert state.request_count == 0
    assert state.success_count == 0
    assert state.failure_count == 0
    assert state.average_latency_seconds == 0.0


def test_mark_initializing():
    state = AIProviderState(name="mock")

    state.mark_initializing()

    assert state.lifecycle == AIProviderLifecycleState.INITIALIZING
    assert state.available is False
    assert state.healthy is False


def test_mark_initialized():
    state = AIProviderState(name="mock")

    state.mark_initialized(model=" llama3 ")

    assert state.lifecycle == AIProviderLifecycleState.INITIALIZED
    assert state.available is True
    assert state.healthy is True
    assert state.current_model == "llama3"
    assert state.last_error is None
    assert state.last_initialized_at is not None


def test_mark_shutdown():
    state = AIProviderState(name="mock")

    state.mark_shutdown()

    assert state.lifecycle == AIProviderLifecycleState.SHUTDOWN
    assert state.available is False
    assert state.healthy is False
    assert state.last_shutdown_at is not None


def test_mark_failed():
    state = AIProviderState(name="mock")

    state.mark_failed("boom")

    assert state.lifecycle == AIProviderLifecycleState.FAILED
    assert state.available is False
    assert state.healthy is False
    assert state.last_error == "boom"


def test_health_check_healthy():
    state = AIProviderState(name="mock")

    state.mark_health_check(healthy=True)

    assert state.healthy is True
    assert state.available is True
    assert state.last_error is None
    assert state.last_health_check_at is not None


def test_health_check_unhealthy():
    state = AIProviderState(name="mock")

    state.mark_health_check(healthy=False, error="offline")

    assert state.healthy is False
    assert state.available is False
    assert state.last_error == "offline"
    assert state.last_health_check_at is not None


def test_disable_and_enable():
    state = AIProviderState(name="mock")

    state.mark_health_check(healthy=True)
    state.disable()

    assert state.enabled is False
    assert state.available is False

    state.enable()

    assert state.enabled is True
    assert state.available is True


def test_record_success():
    state = AIProviderState(name="mock")

    state.record_success(latency_seconds=0.5)
    state.record_success(latency_seconds=1.5)

    assert state.request_count == 2
    assert state.success_count == 2
    assert state.failure_count == 0
    assert state.total_latency_seconds == 2.0
    assert state.last_latency_seconds == 1.5
    assert state.average_latency_seconds == 1.0


def test_record_success_rejects_negative_latency():
    state = AIProviderState(name="mock")

    with pytest.raises(ValueError):
        state.record_success(latency_seconds=-1)


def test_record_failure():
    state = AIProviderState(name="mock")

    state.record_failure("generation failed")

    assert state.request_count == 1
    assert state.success_count == 0
    assert state.failure_count == 1
    assert state.last_error == "generation failed"


def test_record_restart():
    state = AIProviderState(name="mock")

    state.record_restart()
    state.record_restart()

    assert state.restart_count == 2


def test_reset_metrics():
    state = AIProviderState(name="mock")

    state.record_success(latency_seconds=1.0)
    state.record_failure("failed")
    state.reset_metrics()

    assert state.request_count == 0
    assert state.success_count == 0
    assert state.failure_count == 0
    assert state.total_latency_seconds == 0.0
    assert state.last_latency_seconds is None