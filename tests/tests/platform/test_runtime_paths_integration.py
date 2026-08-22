from __future__ import annotations

import os
from pathlib import Path

import pytest

import jaos_platform.platform_runtime as platform_runtime_module
from jaos_platform.platform_runtime import PlatformRuntime
from jaos_platform.runtime_context import RuntimeContext
from jaos_platform.runtime_paths import (
    RUNTIME_DIRECTORY_ENV,
    RuntimePathConfigurationError,
    RuntimePathResolver,
    RuntimePaths,
)


def test_platform_runtime_accepts_and_preserves_injected_paths(
    tmp_path: Path,
) -> None:
    paths = RuntimePaths(tmp_path / "runtime")

    runtime = PlatformRuntime(runtime_paths=paths)

    assert runtime.runtime_paths is paths
    assert runtime.context.runtime_paths is paths
    assert runtime.container.resolve("runtime_context") is runtime.context
    with pytest.raises(AttributeError):
        runtime.runtime_paths = RuntimePaths(tmp_path / "replacement")


def test_runtime_context_carries_injected_paths_without_constructing_them(
    tmp_path: Path,
) -> None:
    paths = RuntimePaths(tmp_path / "runtime")

    context = RuntimeContext(runtime_paths=paths)

    assert context.runtime_paths is paths
    assert RuntimeContext().runtime_paths is None


def test_injected_paths_bypass_resolver_and_environment(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    paths = RuntimePaths(tmp_path / "runtime")
    monkeypatch.setenv(RUNTIME_DIRECTORY_ENV, "relative-and-invalid")

    def fail_if_constructed() -> RuntimePathResolver:
        raise AssertionError("RuntimePathResolver must not be constructed")

    monkeypatch.setattr(
        platform_runtime_module,
        "RuntimePathResolver",
        fail_if_constructed,
    )

    runtime = PlatformRuntime(runtime_paths=paths)

    assert runtime.runtime_paths is paths
    assert runtime.context.runtime_paths is paths


def test_platform_runtime_resolves_paths_exactly_once(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class CountingResolver(RuntimePathResolver):
        def __init__(self) -> None:
            super().__init__(
                environ={},
                platform_name="Linux",
                home_directory=tmp_path / "home",
            )
            self.calls = 0

        def resolve(self, **kwargs: object) -> RuntimePaths:
            self.calls += 1
            return super().resolve(**kwargs)

    resolver = CountingResolver()
    monkeypatch.setattr(
        platform_runtime_module,
        "RuntimePathResolver",
        lambda: resolver,
    )
    runtime_root = tmp_path / "runtime"

    runtime = PlatformRuntime(
        runtime_root=runtime_root,
        profile_id="profile_1",
    )

    assert resolver.calls == 1
    assert runtime.runtime_paths.runtime_root == runtime_root.resolve()
    assert runtime.runtime_paths.profile_id == "profile_1"
    assert runtime.context.runtime_paths is runtime.runtime_paths


def test_environment_runtime_root_resolves_through_platform_runtime(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runtime_root = tmp_path / "environment-runtime"
    monkeypatch.setenv(RUNTIME_DIRECTORY_ENV, str(runtime_root))

    runtime = PlatformRuntime()

    assert runtime.runtime_paths.runtime_root == runtime_root.resolve()
    assert runtime.context.runtime_paths is runtime.runtime_paths


def test_invalid_environment_runtime_root_fails_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(RUNTIME_DIRECTORY_ENV, "relative-runtime")

    with pytest.raises(RuntimePathConfigurationError):
        PlatformRuntime()


def test_repository_contained_runtime_root_fails_closed(
    tmp_path: Path,
) -> None:
    repository_root = tmp_path / "repository"

    with pytest.raises(RuntimePathConfigurationError):
        PlatformRuntime(
            runtime_root=repository_root / "runtime",
            repository_root=repository_root,
        )


def test_construction_has_no_filesystem_or_environment_side_effects(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runtime_root = tmp_path / "runtime"
    monkeypatch.setenv(RUNTIME_DIRECTORY_ENV, str(runtime_root))
    environment_before = dict(os.environ)
    filesystem_before = set(tmp_path.rglob("*"))

    runtime = PlatformRuntime()

    assert runtime.runtime_paths.runtime_root == runtime_root.resolve()
    assert dict(os.environ) == environment_before
    assert set(tmp_path.rglob("*")) == filesystem_before
    assert not runtime_root.exists()
