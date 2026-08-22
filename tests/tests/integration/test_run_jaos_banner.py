from run_jaos import JAOSApplication
from jaos.version import JAOS_VERSION


def test_boot_banner_reports_canonical_jaos_version(capsys) -> None:
    JAOSApplication().boot()

    output = capsys.readouterr().out

    assert f"JAOS {JAOS_VERSION}" in output
    assert "v0.7.0-alpha" not in output


def test_boot_banner_makes_no_unverified_boot_complete_claim(capsys) -> None:
    JAOSApplication().boot()

    output = capsys.readouterr().out

    assert "Boot Complete" not in output
