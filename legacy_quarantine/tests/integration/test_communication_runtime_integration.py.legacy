from communication.communication_hub import CommunicationHub
from jaos_platform.platform_runtime import PlatformRuntime


def test_communication_hub_registers_with_runtime():
    runtime = PlatformRuntime()

    hub = CommunicationHub(runtime)

    assert runtime.container.resolve("communication_hub") is hub


def test_communication_hub_updates_runtime_context():
    runtime = PlatformRuntime()

    CommunicationHub(runtime)

    assert runtime.context.get("communication_hub_status") == "READY"


def test_communication_event_still_works():
    runtime = PlatformRuntime()

    hub = CommunicationHub(runtime)
    hub.add_event("email", "inbox", "New message")

    assert hub.events == [
        {
            "source": "email",
            "category": "inbox",
            "message": "New message",
        }
    ]