"""FORTRESS-02J writer, reachability, and disposition enrichment tests.

Every check is read-only. Legacy writer modules are inspected with AST over
their source text and are never imported. Synthetic artifact trees live under
``tmp_path``; the real ``data/`` tree is never written.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

import pytest

from jaos_platform.runtime_state_inventory import (
    DOCUMENTED_INVENTORY_EXCLUSIONS,
    EXCLUDED_DEVELOPER_WRITERS,
    UNOWNED_RUNTIME_STATE_LOCATIONS,
    ArtifactFamily,
    ArtifactValidationStatus,
    FortressDisposition,
    LegacyRuntimeStateInventory,
    RuntimeStateWriter,
    UnownedRuntimeStateLocation,
    WriterReachability,
    _ARTIFACT_SPECIFICATIONS,
)


_REPOSITORY_ROOT = Path(__file__).resolve().parents[3]

_LEGACY_WRITER_ROOTS = ("brain", "memory", "core", "executive_brain")


def _specification_for(source_pattern: str):
    for specification in _ARTIFACT_SPECIFICATIONS:
        if specification.source_pattern == source_pattern:
            return specification
    raise AssertionError(f"no specification for {source_pattern}")


def _all_writers() -> tuple[RuntimeStateWriter, ...]:
    return tuple(
        writer
        for specification in _ARTIFACT_SPECIFICATIONS
        for writer in specification.writers
    )


def _module_source_path(module: str) -> Path:
    return _REPOSITORY_ROOT.joinpath(*module.split(".")).with_suffix(".py")


def extract_class_constant(
    source_path: Path,
    symbol: str,
    constant: str,
) -> str | None:
    """Return a class-level string constant without importing the module."""

    tree = ast.parse(source_path.read_text(encoding="utf-8"))

    for node in tree.body:
        if not isinstance(node, ast.ClassDef) or node.name != symbol:
            continue
        for statement in node.body:
            if not isinstance(statement, ast.Assign):
                continue
            for target in statement.targets:
                if not isinstance(target, ast.Name) or target.id != constant:
                    continue
                value = statement.value
                if isinstance(value, ast.Constant) and isinstance(
                    value.value, str
                ):
                    return value.value
    return None


# --------------------------------------------------------------------------
# J1, J2 — serialization of writer identity and reachability
# --------------------------------------------------------------------------


def test_writer_metadata_serializes(tmp_path: Path) -> None:
    """J1: writer identity round-trips into metadata output."""

    report = LegacyRuntimeStateInventory(tmp_path).collect()
    goals = next(
        artifact
        for artifact in report.artifacts
        if artifact.family is ArtifactFamily.GOALS
    )

    payload = goals.to_dict()

    assert payload["writers"] == [
        {
            "module": "brain.goal_tracker",
            "symbol": "GoalTracker",
            "reachability": ["EXCLUDED_TEST"],
            "fortress_disposition": "QUARANTINE_FORTRESS_06",
            "path_constant": "FILE_PATH",
            "declared_path_literal": "data/goals/goals.json",
            "notes": None,
        }
    ]


def test_multiple_reachability_values_serialize_deterministically(
    tmp_path: Path,
) -> None:
    """J2: several reachability values keep a stable declared order."""

    report = LegacyRuntimeStateInventory(tmp_path).collect()
    settings = next(
        artifact
        for artifact in report.artifacts
        if artifact.family is ArtifactFamily.SETTINGS
    )

    assert settings.to_dict()["reachability"] == [
        "MAIN",
        "CONFIGURED_TEST",
    ]

    repeated = LegacyRuntimeStateInventory(tmp_path).collect()
    assert repeated.to_dict() == report.to_dict()


def test_multiple_writers_are_modelled_without_loss(tmp_path: Path) -> None:
    """A shared artifact retains every declared writer."""

    report = LegacyRuntimeStateInventory(tmp_path).collect()
    long_term = next(
        artifact
        for artifact in report.artifacts
        if artifact.family is ArtifactFamily.LONG_TERM_MEMORY
    )

    identifiers = [writer.identifier for writer in long_term.writers]

    assert identifiers == [
        "memory.long_term_memory.LongTermMemory",
        "memory.memory_cleanup.MemoryCleanup",
    ]


def test_artifact_without_writer_reports_no_known_caller(
    tmp_path: Path,
) -> None:
    """A writer-less artifact is modelled truthfully, not invented."""

    report = LegacyRuntimeStateInventory(tmp_path).collect()
    system_log = next(
        artifact
        for artifact in report.artifacts
        if artifact.family is ArtifactFamily.SYSTEM_LOG
    )

    assert system_log.writers == ()
    assert system_log.reachability == (WriterReachability.NO_KNOWN_CALLER,)
    assert system_log.reachable_from_run_jaos is False


# --------------------------------------------------------------------------
# J3 — canonical containment
# --------------------------------------------------------------------------


def test_no_artifact_is_reachable_from_run_jaos(tmp_path: Path) -> None:
    """J3: every legacy artifact is isolated from the canonical path."""

    report = LegacyRuntimeStateInventory(tmp_path).collect()

    assert report.artifacts_reachable_from_run_jaos == ()

    for artifact in report.artifacts:
        assert artifact.reachable_from_run_jaos is False
        assert artifact.to_dict()["reachable_from_run_jaos"] is False


def test_no_declared_writer_claims_run_jaos_reachability() -> None:
    """J3: the specification table declares no canonical writer."""

    for writer in _all_writers():
        assert WriterReachability.RUN_JAOS not in writer.reachability, (
            writer.identifier
        )


# --------------------------------------------------------------------------
# J4, J5, J6, J7 — dispositions
# --------------------------------------------------------------------------


def test_settings_uses_config_split() -> None:
    """J4: settings carries the configuration-split disposition."""

    specification = _specification_for("config/settings.json")

    assert (
        specification.fortress_disposition
        is FortressDisposition.CONFIG_SPLIT
    )


def test_provider_configuration_decision_is_deferred() -> None:
    """J5: provider catalog ownership is recorded as deferred."""

    specification = _specification_for("config/providers.json")

    assert (
        specification.fortress_disposition
        is FortressDisposition.DEFERRED_ARCHITECTURE_DECISION
    )


@pytest.mark.parametrize(
    "source_pattern",
    [
        "data/snapshots/*.json",
        "data/backups/*/actions.json",
        "exports/memory_export_*.json",
        "logs/system.log",
    ],
)
def test_archive_only_dispositions_preserved(source_pattern: str) -> None:
    """J6: archive-only artifacts keep that disposition."""

    specification = _specification_for(source_pattern)

    assert (
        specification.fortress_disposition
        is FortressDisposition.ARCHIVE_ONLY
    )


def test_no_artifact_is_falsely_marked_migrated() -> None:
    """J7: nothing is recorded as externalized, because nothing migrated."""

    for specification in _ARTIFACT_SPECIFICATIONS:
        assert (
            specification.fortress_disposition
            is not FortressDisposition.CANONICAL_EXTERNALIZED
        ), specification.source_pattern


def test_only_config_manager_writer_is_externalized() -> None:
    """The one externalized write path is recorded at writer level only."""

    externalized = [
        writer.identifier
        for writer in _all_writers()
        if writer.fortress_disposition
        is FortressDisposition.CANONICAL_EXTERNALIZED
    ]

    assert externalized == ["core.config_manager.ConfigManager"]


# --------------------------------------------------------------------------
# J8, J9 — specification table integrity
# --------------------------------------------------------------------------


def test_specification_patterns_are_unique() -> None:
    """J8: no duplicate artifact path specification exists."""

    patterns = [
        specification.source_pattern
        for specification in _ARTIFACT_SPECIFICATIONS
    ]

    assert len(patterns) == len(set(patterns))


def test_writer_identifiers_are_unique_per_artifact() -> None:
    """J8: an artifact never declares the same writer twice."""

    for specification in _ARTIFACT_SPECIFICATIONS:
        identifiers = [
            writer.identifier for writer in specification.writers
        ]
        assert len(identifiers) == len(set(identifiers)), (
            specification.source_pattern
        )


def test_families_are_unique_and_fully_covered() -> None:
    """J9: every declared family appears exactly once."""

    families = [
        specification.family for specification in _ARTIFACT_SPECIFICATIONS
    ]

    assert len(families) == len(set(families))
    assert set(families) == set(ArtifactFamily)


def test_every_specification_declares_a_disposition() -> None:
    """J9: disposition metadata is mandatory, never defaulted silently."""

    for specification in _ARTIFACT_SPECIFICATIONS:
        assert isinstance(
            specification.fortress_disposition, FortressDisposition
        ), specification.source_pattern
        for writer in specification.writers:
            assert isinstance(
                writer.fortress_disposition, FortressDisposition
            ), writer.identifier
            assert writer.reachability, writer.identifier


def test_writer_reachability_cannot_be_empty() -> None:
    """A writer must declare at least one reachability value."""

    with pytest.raises(Exception):
        RuntimeStateWriter(
            module="brain.example",
            symbol="Example",
            reachability=(),
            fortress_disposition=(
                FortressDisposition.QUARANTINE_FORTRESS_06
            ),
        )


# --------------------------------------------------------------------------
# J10, J11, J12 — static writer/path consistency without importing
# --------------------------------------------------------------------------


def test_declared_writer_paths_match_source_constants() -> None:
    """J10: AST cross-check of every statically verifiable writer."""

    checked = 0

    for specification in _ARTIFACT_SPECIFICATIONS:
        for writer in specification.writers:
            if not writer.statically_verifiable_path:
                continue

            source_path = _module_source_path(writer.module)
            assert source_path.is_file(), writer.identifier

            source_declared = extract_class_constant(
                source_path,
                writer.symbol,
                writer.path_constant or "",
            )

            assert source_declared is not None, (
                f"{writer.identifier}: {writer.path_constant} not found "
                f"in {source_path}"
            )
            assert source_declared == writer.declared_path_literal, (
                f"{writer.identifier}: inventory expects "
                f"{writer.declared_path_literal!r} but source declares "
                f"{source_declared!r} in {source_path}"
            )
            checked += 1

    assert checked >= 11


def test_non_verifiable_writers_are_explicitly_recorded() -> None:
    """J10: dynamic path declarations are documented, not silently skipped."""

    unverifiable = [
        writer
        for writer in _all_writers()
        if not writer.statically_verifiable_path
    ]

    assert [writer.identifier for writer in unverifiable] == [
        "memory.memory_cleanup.MemoryCleanup",
        "core.snapshot_manager.SnapshotManager",
        "core.backup_manager.BackupManager",
    ]

    for writer in unverifiable:
        assert writer.notes, writer.identifier


def test_synthetic_path_drift_is_detected(tmp_path: Path) -> None:
    """J11: a mismatch between source and inventory is caught."""

    module_path = tmp_path / "legacy_writer.py"
    module_path.write_text(
        'class LegacyWriter:\n'
        '    FILE_PATH = "data/goals/renamed_goals.json"\n',
        encoding="utf-8",
    )

    source_declared = extract_class_constant(
        module_path,
        "LegacyWriter",
        "FILE_PATH",
    )

    assert source_declared == "data/goals/renamed_goals.json"
    assert source_declared != "data/goals/goals.json"


def test_missing_constant_is_detected(tmp_path: Path) -> None:
    """J11: a removed constant is reported rather than silently passing."""

    module_path = tmp_path / "legacy_writer.py"
    module_path.write_text(
        "class LegacyWriter:\n    OTHER = 1\n",
        encoding="utf-8",
    )

    assert (
        extract_class_constant(module_path, "LegacyWriter", "FILE_PATH")
        is None
    )


def _legacy_modules_in(names: object) -> set[str]:
    return {
        name
        for name in names  # type: ignore[union-attr]
        if any(
            name == root or name.startswith(f"{root}.")
            for root in _LEGACY_WRITER_ROOTS
        )
    }


def test_ast_inspection_imports_no_legacy_writer_module() -> None:
    """J12: static inspection adds no legacy module to sys.modules.

    The assertion is a delta rather than absolute absence, because other
    configured tests legitimately import ``core`` for their own purposes.
    """

    before = _legacy_modules_in(set(sys.modules))

    for specification in _ARTIFACT_SPECIFICATIONS:
        for writer in specification.writers:
            if writer.statically_verifiable_path:
                extract_class_constant(
                    _module_source_path(writer.module),
                    writer.symbol,
                    writer.path_constant or "",
                )

    after = _legacy_modules_in(set(sys.modules))

    assert after - before == set()


def test_inventory_module_imports_no_legacy_writer() -> None:
    """J12: the production inventory never imports a writer module."""

    inventory_source = (
        _REPOSITORY_ROOT / "jaos_platform" / "runtime_state_inventory.py"
    )
    tree = ast.parse(inventory_source.read_text(encoding="utf-8"))

    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)

    assert _legacy_modules_in(imported) == set()


# --------------------------------------------------------------------------
# J13, J14, J15 — read-only behaviour, privacy, missing artifacts
# --------------------------------------------------------------------------


def test_inventory_remains_read_only(tmp_path: Path) -> None:
    """J13: collecting never creates, modifies, or removes anything."""

    goals = tmp_path / "data" / "goals"
    goals.mkdir(parents=True)
    (goals / "goals.json").write_text("[]", encoding="utf-8")

    def snapshot() -> dict[str, tuple[int, int]]:
        return {
            path.relative_to(tmp_path).as_posix(): (
                path.stat().st_size,
                path.stat().st_mtime_ns,
            )
            for path in sorted(tmp_path.rglob("*"))
            if path.is_file()
        }

    before = snapshot()

    inventory = LegacyRuntimeStateInventory(tmp_path)
    inventory.collect()
    inventory.collect()

    assert snapshot() == before


def test_serialization_excludes_payloads(tmp_path: Path) -> None:
    """J14: artifact contents never reach the metadata output."""

    marker = "SENSITIVE_PAYLOAD_MARKER_02J"
    goals = tmp_path / "data" / "goals"
    goals.mkdir(parents=True)
    (goals / "goals.json").write_text(
        json.dumps({"goals": [{"detail": marker}]}),
        encoding="utf-8",
    )

    report = LegacyRuntimeStateInventory(tmp_path).collect()
    serialized = json.dumps(report.to_dict())

    assert marker not in serialized

    goals_artifact = next(
        artifact
        for artifact in report.artifacts
        if artifact.family is ArtifactFamily.GOALS
    )
    assert goals_artifact.record_count == 1
    assert "source_path" not in goals_artifact.to_dict()


def test_missing_artifacts_retain_writer_metadata(tmp_path: Path) -> None:
    """J15: MISSING entries stay truthful and keep their writer identity."""

    report = LegacyRuntimeStateInventory(tmp_path).collect()

    behavior = next(
        artifact
        for artifact in report.artifacts
        if artifact.family is ArtifactFamily.BEHAVIOR_PATTERNS
    )

    assert behavior.validation_status is ArtifactValidationStatus.MISSING
    assert behavior.exists is False
    assert behavior.writers
    assert behavior.writers[0].identifier == (
        "brain.behavior_tracker.BehaviorTracker"
    )
    assert (
        behavior.fortress_disposition
        is FortressDisposition.PRESERVE_FOR_MIGRATION
    )


# --------------------------------------------------------------------------
# J16, J17, J18 — orphan directories, developer tooling, tool paths
# --------------------------------------------------------------------------


def test_orphan_directories_are_explicit(tmp_path: Path) -> None:
    """J16: the unowned runtime-state locations are modelled explicitly."""

    locations = {
        location.location: location
        for location in UNOWNED_RUNTIME_STATE_LOCATIONS
    }

    assert set(locations) == {"data/cache", "data/diagnostics"}

    for location in locations.values():
        assert isinstance(location, UnownedRuntimeStateLocation)
        assert location.reachability == (
            WriterReachability.NO_KNOWN_CALLER,
        )
        assert (
            location.fortress_disposition
            is FortressDisposition.DEFERRED_ARCHITECTURE_DECISION
        )
        assert location.notes

    report = LegacyRuntimeStateInventory(tmp_path).collect()
    serialized = report.to_dict()["unowned_locations"]

    assert [entry["location"] for entry in serialized] == [
        "data/cache",
        "data/diagnostics",
    ]


def test_orphan_directories_are_not_artifacts() -> None:
    """J16: unowned directories never enter the artifact model."""

    patterns = {
        specification.source_pattern
        for specification in _ARTIFACT_SPECIFICATIONS
    }

    for location in UNOWNED_RUNTIME_STATE_LOCATIONS:
        assert not any(
            pattern.startswith(location.location) for pattern in patterns
        ), location.location


def test_developer_tooling_is_outside_runtime_state_scope(
    tmp_path: Path,
) -> None:
    """J17: documentation tooling is recorded separately, not as state."""

    developer_modules = {
        writer.module for writer in EXCLUDED_DEVELOPER_WRITERS
    }

    assert "scripts.generate_dg1_docs" in developer_modules

    for writer in EXCLUDED_DEVELOPER_WRITERS:
        assert writer.reachability == (WriterReachability.DEVELOPER_TOOL,)
        assert writer.notes

    for writer in _all_writers():
        assert writer.module not in developer_modules, writer.identifier

    report = LegacyRuntimeStateInventory(tmp_path).collect()
    serialized = report.to_dict()["excluded_developer_writers"]

    assert [entry["module"] for entry in serialized] == [
        "scripts.generate_dg1_docs"
    ]


def test_user_directed_tool_paths_are_not_runtime_state(
    tmp_path: Path,
) -> None:
    """J18: filesystem tools and shadow stacks own no artifact."""

    for writer in _all_writers():
        assert not writer.module.startswith("jaos."), writer.identifier
        assert not writer.module.startswith("executive_brain"), (
            writer.identifier
        )

    exclusions = " ".join(DOCUMENTED_INVENTORY_EXCLUSIONS)

    assert "jaos.tools.filesystem" in exclusions
    assert "executive_brain.tools.file" in exclusions

    report = LegacyRuntimeStateInventory(tmp_path).collect()

    assert report.to_dict()["documented_exclusions"] == list(
        DOCUMENTED_INVENTORY_EXCLUSIONS
    )


def test_canonical_and_legacy_namespaces_are_not_conflated() -> None:
    """Root legacy memory and canonical jaos.memory stay distinct."""

    modules = {writer.module for writer in _all_writers()}

    assert "memory.long_term_memory" in modules
    assert not any(module.startswith("jaos.memory") for module in modules)

    provider_writers = {
        writer.identifier
        for writer in _all_writers()
        if writer.symbol == "ProviderRouter"
    }

    assert provider_writers == {"brain.provider_router.ProviderRouter"}
