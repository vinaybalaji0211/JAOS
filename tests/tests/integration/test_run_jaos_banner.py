from run_jaos import JAOSApplication
from jaos.version import JAOS_VERSION


def test_boot_banner_reports_canonical_jaos_version(capsys) -> None:
    JAOSApplication().boot()

    output = capsys.readouterr().out

    assert f"JAOS {JAOS_VERSION}" in output
    assert "v0.7.0-alpha" not in output
