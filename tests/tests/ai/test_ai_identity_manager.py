from jaos.ai.identity.identity_manager import IdentityManager
from jaos.version import JAOS_VERSION


def test_jaos_version_is_certified_baseline() -> None:
    assert JAOS_VERSION == "v0.9.0-alpha"


def test_identity_manager_version_matches_jaos_version() -> None:
    identity = IdentityManager().get_identity()
    assert identity.version == JAOS_VERSION


def test_stale_long_term_memory_limitation_is_absent() -> None:
    identity = IdentityManager().get_identity()
    limitation_names = [limitation.name for limitation in identity.limitations]
    assert "No Long-Term Memory Yet" not in limitation_names


def test_memory_platform_not_connected_limitation_is_present() -> None:
    identity = IdentityManager().get_identity()
    memory_limitations = [
        limitation
        for limitation in identity.limitations
        if limitation.name == "Memory Platform Not Connected to This Shell"
    ]
    assert len(memory_limitations) == 1
    assert memory_limitations[0].description == (
        f"The Memory Platform is implemented and certified at {JAOS_VERSION}, "
        f"but it is not initialized or accessible through the current JAOS "
        f"Shell runtime."
    )


def test_identity_capabilities_do_not_claim_memory() -> None:
    identity = IdentityManager().get_identity()
    for capability in identity.capabilities:
        assert "memory" not in capability.name.lower()
