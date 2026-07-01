from jaos_platform.event_bus import EventBus


def test_publish_event():
    bus = EventBus()

    received = []

    def handler(data):
        received.append(data)

    bus.subscribe("test", handler)

    bus.publish("test", 123)

    assert received == [123]


def test_multiple_handlers():
    bus = EventBus()

    result = []

    def a(data):
        result.append(("a", data))

    def b(data):
        result.append(("b", data))

    bus.subscribe("event", a)
    bus.subscribe("event", b)

    bus.publish("event", "hello")

    assert len(result) == 2


def test_subscriber_count():
    bus = EventBus()

    bus.subscribe("x", lambda _: None)
    bus.subscribe("x", lambda _: None)

    assert bus.subscriber_count("x") == 2


def test_clear():
    bus = EventBus()

    bus.subscribe("x", lambda _: None)

    bus.clear()

    assert bus.subscriber_count("x") == 0