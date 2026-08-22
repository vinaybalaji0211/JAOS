"""FORTRESS-02H containment tests for ConfigManager.

Repository settings are read-only defaults. Mutable per-profile settings
must be written only beneath an explicitly injected absolute path.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from core.config_manager import ConfigManager


_REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
_REPOSITORY_SETTINGS = _REPOSITORY_ROOT / "config" / "settings.json"


def _write_defaults(path: Path, payload: dict[str, object]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=4),
        encoding="utf-8",
    )
    return path


def test_loading_repository_defaults_does_not_modify_them(
    protected_repository_state: None,
) -> None:
    """C1: reading the real defaults changes neither bytes nor mtime."""

    if not _REPOSITORY_SETTINGS.exists():
        pytest.skip("repository settings defaults are absent")

    original_bytes = _REPOSITORY_SETTINGS.read_bytes()
    original_mtime_ns = _REPOSITORY_SETTINGS.stat().st_mtime_ns

    config = ConfigManager.load_config()

    assert isinstance(config, dict)
    assert _REPOSITORY_SETTINGS.read_bytes() == original_bytes
    assert _REPOSITORY_SETTINGS.stat().st_mtime_ns == original_mtime_ns


def test_missing_profile_overlay_returns_defaults_without_writing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """C2: an absent overlay yields defaults and creates no overlay file."""

    defaults_path = _write_defaults(
        tmp_path / "repository" / "settings.json",
        {
            "jarvis_name": "JARVIS OS",
            "mode": "NORMAL",
            "ai_provider": "NONE",
        },
    )
    monkeypatch.setattr(
        ConfigManager,
        "FILE_PATH",
        str(defaults_path),
    )

    overlay_path = tmp_path / "profile" / "config" / "settings.json"

    config = ConfigManager.load_config(
        profile_settings_path=overlay_path,
    )

    assert config["mode"] == "NORMAL"
    assert config["ai_provider"] == "NONE"
    assert not overlay_path.exists()
    assert not overlay_path.parent.exists()


def test_profile_overlay_overrides_mutable_values(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """C3: overlay mutable keys win over repository defaults."""

    defaults_path = _write_defaults(
        tmp_path / "repository" / "settings.json",
        {
            "jarvis_name": "JARVIS OS",
            "mode": "NORMAL",
            "ai_provider": "NONE",
        },
    )
    monkeypatch.setattr(
        ConfigManager,
        "FILE_PATH",
        str(defaults_path),
    )

    overlay_path = _write_defaults(
        tmp_path / "profile" / "config" / "settings.json",
        {
            "mode": "FOCUS",
            "ai_provider": "ollama",
            "jarvis_name": "IGNORED",
        },
    )

    config = ConfigManager.load_config(
        profile_settings_path=overlay_path,
    )

    assert config["mode"] == "FOCUS"
    assert config["ai_provider"] == "ollama"
    assert config["jarvis_name"] == "JARVIS OS"


def test_loading_creates_no_repository_file_or_directory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    protected_repository_state: None,
) -> None:
    """C4: an absent defaults file is never created on load."""

    absent_defaults = tmp_path / "absent" / "settings.json"
    monkeypatch.setattr(
        ConfigManager,
        "FILE_PATH",
        str(absent_defaults),
    )

    config = ConfigManager.load_config()

    assert config == ConfigManager.DEFAULT_CONFIG
    assert config is not ConfigManager.DEFAULT_CONFIG
    assert not absent_defaults.exists()
    assert not absent_defaults.parent.exists()


def test_save_writes_only_beneath_supplied_profile_path(
    tmp_path: Path,
    protected_repository_state: None,
) -> None:
    """C5: mutation lands only under the injected profile location."""

    overlay_path = tmp_path / "profile" / "config" / "settings.json"

    written_path = ConfigManager.save_config(
        {
            "jarvis_name": "SHOULD NOT PERSIST",
            "mode": "FOCUS",
            "ai_provider": "ollama",
        },
        profile_settings_path=overlay_path,
    )

    assert written_path == overlay_path
    assert overlay_path.is_file()

    persisted = json.loads(overlay_path.read_text(encoding="utf-8"))

    assert persisted == {
        "mode": "FOCUS",
        "ai_provider": "ollama",
    }
    assert "jarvis_name" not in persisted


def test_save_without_profile_target_fails_closed(
    protected_repository_state: None,
) -> None:
    """C6: mutation never falls back to the repository defaults file."""

    original_bytes = (
        _REPOSITORY_SETTINGS.read_bytes()
        if _REPOSITORY_SETTINGS.exists()
        else None
    )

    with pytest.raises(ValueError):
        ConfigManager.save_config({"mode": "FOCUS"})

    if original_bytes is not None:
        assert _REPOSITORY_SETTINGS.read_bytes() == original_bytes


@pytest.mark.parametrize(
    "relative_path",
    [
        "settings.json",
        "./settings.json",
        "config/settings.json",
    ],
)
def test_relative_profile_paths_are_rejected(
    relative_path: str,
    protected_repository_state: None,
) -> None:
    """C7: relative overlay paths are rejected on load and on save."""

    with pytest.raises(ValueError):
        ConfigManager.load_config(
            profile_settings_path=relative_path,
        )

    with pytest.raises(ValueError):
        ConfigManager.save_config(
            {"mode": "FOCUS"},
            profile_settings_path=relative_path,
        )


def test_config_manager_does_not_resolve_runtime_roots() -> None:
    """C8: ConfigManager never derives a runtime root itself."""

    import core.config_manager as config_manager_module

    source = Path(config_manager_module.__file__).read_text(
        encoding="utf-8",
    )

    forbidden = (
        "getcwd",
        "cwd(",
        "JAOS_RUNTIME_DIR",
        "LOCALAPPDATA",
        "XDG_DATA_HOME",
        "Path.home",
        ".git",
        "RuntimePathResolver",
        "C:\\JARVIS",
        "C:/JARVIS",
    )

    for token in forbidden:
        assert token not in source, token


def test_load_ignores_runtime_directory_environment(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """C8: JAOS_RUNTIME_DIR does not influence ConfigManager."""

    defaults_path = _write_defaults(
        tmp_path / "repository" / "settings.json",
        {"jarvis_name": "JARVIS OS", "mode": "NORMAL", "ai_provider": "NONE"},
    )
    monkeypatch.setattr(
        ConfigManager,
        "FILE_PATH",
        str(defaults_path),
    )
    monkeypatch.setenv(
        "JAOS_RUNTIME_DIR",
        str(tmp_path / "unused-runtime-root"),
    )

    config = ConfigManager.load_config()

    assert config["mode"] == "NORMAL"
    assert not (tmp_path / "unused-runtime-root").exists()
