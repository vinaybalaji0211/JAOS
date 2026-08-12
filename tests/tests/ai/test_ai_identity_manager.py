from jaos.ai.identity.identity_manager import IdentityManager
from jaos.version import JAOS_VERSION


def test_jaos_version_is_certified_baseline() -> None:
    assert JAOS_VERSION == "v0.9.0-alpha"


def test_identity_manager_version_matches_jaos_version() -> None:
    identity = IdentityManager().get_identity()
    assert identity.version == JAOS_VERSION
