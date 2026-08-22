from __future__ import annotations

import os
from pathlib import Path

import pytest

from jaos_platform.runtime_paths import RUNTIME_DIRECTORY_ENV, RuntimePaths


_REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
_RUNTIME_ENVIRONMENT_VARIABLES = (
    RUNTIME_DIRECTORY_ENV,
    "LOCALAPPDATA",
    "XDG_DATA_HOME",
    "HOME",
)


def _create_temporary_repository(tmp_path: Path) -> Path:
    repository_root = tmp_path / "repository"
    for area_name in ("data", "config", "logs", "exports"):
        (repository_root / area_name).mkdir(parents=True)
    (repository_root / "data" / "existing.json").write_text(
        '{"state": "original"}',
        encoding="utf-8",
    )
    return repository_root


def test_jaos_runtime_paths_uses_tmp_path_owned_root(
    tmp_path: Path,
    jaos_runtime_paths: RuntimePaths,
) -> None:
    assert jaos_runtime_paths.runtime_root == (
        tmp_path / "jaos-runtime"
    ).resolve()
    assert jaos_runtime_paths.profile_id == "pytest"
    assert not jaos_runtime_paths.runtime_root.exists()


def test_jaos_runtime_paths_root_is_outside_repository(
    jaos_runtime_paths: RuntimePaths,
) -> None:
    with pytest.raises(ValueError):
        jaos_runtime_paths.runtime_root.relative_to(_REPOSITORY_ROOT)


def test_independent_runtime_contexts_do_not_share_state(
    tmp_path: Path,
    jaos_runtime_paths_factory,
) -> None:
    first = jaos_runtime_paths_factory(tmp_path / "first-context")
    second = jaos_runtime_paths_factory(tmp_path / "second-context")

    first.state.mkdir(parents=True)
    (first.state / "sentinel.json").write_text("{}", encoding="utf-8")

    assert first.runtime_root != second.runtime_root
    assert not second.profile_root.exists()
    assert not (second.state / "sentinel.json").exists()


def test_jaos_runtime_paths_uses_canonical_layout(
    jaos_runtime_paths: RuntimePaths,
) -> None:
    version_root = jaos_runtime_paths.runtime_root / "v1"
    profile_root = version_root / "profiles" / "pytest"

    assert jaos_runtime_paths.version_root == version_root
    assert jaos_runtime_paths.profile_root == profile_root
    assert jaos_runtime_paths.config == profile_root / "config"
    assert jaos_runtime_paths.memory == profile_root / "memory"
    assert jaos_runtime_paths.state == profile_root / "state"
    assert jaos_runtime_paths.recovery == profile_root / "recovery"
    assert jaos_runtime_paths.audit == profile_root / "audit"
    assert jaos_runtime_paths.logs == profile_root / "logs"
    assert jaos_runtime_paths.exports == profile_root / "exports"
    assert jaos_runtime_paths.backups == profile_root / "backups"
    assert jaos_runtime_paths.migrations == profile_root / "migrations"
    assert jaos_runtime_paths.tmp == profile_root / "tmp"


def test_runtime_environment_context_restores_all_related_variables(
    jaos_runtime_paths: RuntimePaths,
    jaos_runtime_environment_context,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(RUNTIME_DIRECTORY_ENV, "original-runtime-root")
    before = {
        name: os.environ.get(name)
        for name in _RUNTIME_ENVIRONMENT_VARIABLES
    }

    with jaos_runtime_environment_context() as active_paths:
        assert active_paths is jaos_runtime_paths
        assert os.environ[RUNTIME_DIRECTORY_ENV] == str(
            jaos_runtime_paths.runtime_root
        )
        for name in _RUNTIME_ENVIRONMENT_VARIABLES[1:]:
            assert os.environ.get(name) == before[name]

    after = {
        name: os.environ.get(name)
        for name in _RUNTIME_ENVIRONMENT_VARIABLES
    }
    assert after == before


def test_runtime_environment_fixture_exposes_isolated_root(
    jaos_runtime_environment: RuntimePaths,
) -> None:
    assert os.environ[RUNTIME_DIRECTORY_ENV] == str(
        jaos_runtime_environment.runtime_root
    )


def test_repository_write_guard_passes_without_changes(
    tmp_path: Path,
    repository_write_guard,
) -> None:
    repository_root = _create_temporary_repository(tmp_path)

    with repository_write_guard(repository_root):
        pass


def test_repository_write_guard_detects_created_file(
    tmp_path: Path,
    repository_write_guard,
) -> None:
    repository_root = _create_temporary_repository(tmp_path)

    with pytest.raises(AssertionError) as failure:
        with repository_write_guard(repository_root):
            (repository_root / "data" / "created.json").write_text(
                "{}",
                encoding="utf-8",
            )

    assert "created: data/created.json" in str(failure.value)


def test_repository_write_guard_detects_modified_file(
    tmp_path: Path,
    repository_write_guard,
) -> None:
    repository_root = _create_temporary_repository(tmp_path)
    protected_file = repository_root / "data" / "existing.json"

    with pytest.raises(AssertionError) as failure:
        with repository_write_guard(repository_root):
            protected_file.write_text(
                '{"state": "changed"}',
                encoding="utf-8",
            )

    assert "modified: data/existing.json" in str(failure.value)


def test_repository_write_guard_detects_deleted_file(
    tmp_path: Path,
    repository_write_guard,
) -> None:
    repository_root = _create_temporary_repository(tmp_path)
    protected_file = repository_root / "data" / "existing.json"

    with pytest.raises(AssertionError) as failure:
        with repository_write_guard(repository_root):
            protected_file.unlink()

    assert "deleted: data/existing.json" in str(failure.value)


def test_repository_write_guard_reports_renamed_paths(
    tmp_path: Path,
    repository_write_guard,
) -> None:
    repository_root = _create_temporary_repository(tmp_path)
    source = repository_root / "data" / "existing.json"
    destination = repository_root / "data" / "renamed.json"

    with pytest.raises(AssertionError) as failure:
        with repository_write_guard(repository_root):
            source.rename(destination)

    message = str(failure.value)
    assert "deleted: data/existing.json" in message
    assert "created: data/renamed.json" in message


def test_repository_write_guard_accepts_preexisting_dirty_state(
    tmp_path: Path,
    repository_write_guard,
) -> None:
    repository_root = _create_temporary_repository(tmp_path)
    dirty_file = repository_root / "data" / "existing.json"
    dirty_file.write_text(
        '{"state": "already-dirty"}',
        encoding="utf-8",
    )

    with repository_write_guard(repository_root):
        pass


def test_isolation_infrastructure_does_not_modify_protected_repository(
    protected_repository_state,
    jaos_runtime_paths: RuntimePaths,
) -> None:
    assert not jaos_runtime_paths.runtime_root.exists()
