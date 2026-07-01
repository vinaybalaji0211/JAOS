from jaos_platform.runtime_context import RuntimeContext


def test_set_get():
    ctx = RuntimeContext()

    ctx.set("user", "Vinay")

    assert ctx.get("user") == "Vinay"


def test_default():
    ctx = RuntimeContext()

    assert ctx.get("missing", "default") == "default"


def test_remove():
    ctx = RuntimeContext()

    ctx.set("x", 1)
    ctx.remove("x")

    assert not ctx.contains("x")


def test_clear():
    ctx = RuntimeContext()

    ctx.set("a", 1)
    ctx.set("b", 2)

    ctx.clear()

    assert ctx.keys() == []


def test_keys():
    ctx = RuntimeContext()

    ctx.set("b", 1)
    ctx.set("a", 2)

    assert ctx.keys() == ["a", "b"]