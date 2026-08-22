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


def test_subscriber_failure_does_not_propagate():
    bus = EventBus()

    def broken(_data):
        raise RuntimeError("subscriber exploded")

    bus.subscribe("event", broken)

    bus.publish("event", "payload")


def test_subscriber_failure_does_not_block_other_subscribers():
    bus = EventBus()

    result = []

    def broken(_data):
        raise RuntimeError("subscriber exploded")

    def healthy(data):
        result.append(data)

    bus.subscribe("event", broken)
    bus.subscribe("event", healthy)

    bus.publish("event", "payload")

    assert result == ["payload"]