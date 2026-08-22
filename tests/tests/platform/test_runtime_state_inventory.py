"""FORTRESS-02F tests for read-only legacy runtime-state inventory."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from jaos_platform.runtime_state_inventory import (
    ArtifactClassification,
    ArtifactFamily,
    ArtifactFormat,
    ArtifactSchemaShape,
    ArtifactValidationStatus,
    LegacyRuntimeStateInventory,
    MigrationDisposition,
    RuntimeStateArtifact,
    RuntimeStateInventoryConfigurationError,
    RuntimeStateInventoryReport,
    SensitivityClassification,
)


@pytest.fixture
def legacy_source_root(tmp_path: Path) -> Path:
    source_root = tmp_path / "synthetic-legacy-source"
    source_root.mkdir()
    return source_root


def _write_bytes(
    source_root: Path,
    relative_path: str,
    payload: bytes,
) -> Path:
    source_path = source_root / relative_path
    source_path.parent.mkdir(parents=True, exist_ok=True)
    source_path.write_bytes(payload)
    return source_path


def _find_artifact(
    report: RuntimeStateInventoryReport,
    source_identifier: str,
) -> RuntimeStateArtifact:
    return next(
        artifact
        for artifact in report.artifacts
        if artifact.source_identifier == source_identifier
    )


def test_hash_and_size_are_stable_for_unchanged_original_bytes(
    legacy_source_root: Path,
) -> None:
    payload = b'[{"goal_id":1},{"goal_id":2}]\n'
    source_path = _write_bytes(
        legacy_source_root,
        "data/goals/goals.json",
        payload,
    )
    inventory = LegacyRuntimeStateInventory(legacy_source_root)

    first = _find_artifact(
        inventory.collect(),
        "data/goals/goals.json",
    )
    second = _find_artifact(
        inventory.collect(),
        "data/goals/goals.json",
    )

    assert first.sha256 == hashlib.sha256(payload).hexdigest()
    assert second.sha256 == first.sha256
    assert first.byte_size == len(payload)
    assert source_path.read_bytes() == payload


def test_json_array_reports_top_level_record_count(
    legacy_source_root: Path,
) -> None:
    _write_bytes(
        legacy_source_root,
        "exports/memory_export_20260821.json",
        b'[{"id":1},{"id":2},{"id":3}]',
    )

    artifact = _find_artifact(
        LegacyRuntimeStateInventory(legacy_source_root).collect(),
        "exports/memory_export_20260821.json",
    )

    assert artifact.detected_format is ArtifactFormat.JSON_ARRAY
    assert artifact.schema_shape is ArtifactSchemaShape.TOP_LEVEL_ARRAY
    assert artifact.record_count == 3
    assert artifact.classification is ArtifactClassification.GENERATED_EXPORT


def test_json_object_reports_known_collection_and_schema_version(
    legacy_source_root: Path,
) -> None:
    _write_bytes(
        legacy_source_root,
        "data/goals/goals.json",
        b'{"schema_version":2,"goals":[{"id":1},{"id":2}]}',
    )

    artifact = _find_artifact(
        LegacyRuntimeStateInventory(legacy_source_root).collect(),
        "data/goals/goals.json",
    )

    assert artifact.validation_status is ArtifactValidationStatus.VALID
    assert artifact.detected_format is ArtifactFormat.JSON_OBJECT
    assert artifact.schema_shape is (
        ArtifactSchemaShape.OBJECT_WITH_RECORD_COLLECTION
    )
    assert artifact.schema_version == 2
    assert artifact.record_count == 2


def test_malformed_json_is_reported_without_payload_disclosure(
    legacy_source_root: Path,
) -> None:
    sensitive_marker = "private-goal-value-must-not-appear"
    _write_bytes(
        legacy_source_root,
        "data/goals/goals.json",
        f'{{"goal":"{sensitive_marker}"'.encode(),
    )

    artifact = _find_artifact(
        LegacyRuntimeStateInventory(legacy_source_root).collect(),
        "data/goals/goals.json",
    )
    serialized = json.dumps(artifact.to_dict())

    assert artifact.validation_status is ArtifactValidationStatus.INVALID
    assert artifact.detected_format is ArtifactFormat.MALFORMED_JSON
    assert artifact.validation_detail == "MALFORMED_JSON"
    assert sensitive_marker not in repr(artifact)
    assert sensitive_marker not in serialized


def test_missing_exact_and_glob_artifacts_are_truthful(
    legacy_source_root: Path,
) -> None:
    report = LegacyRuntimeStateInventory(legacy_source_root).collect()
    missing_goal = _find_artifact(report, "data/goals/goals.json")
    missing_snapshots = _find_artifact(report, "data/snapshots/*.json")

    assert missing_goal.exists is False
    assert missing_goal.validation_status is ArtifactValidationStatus.MISSING
    assert missing_goal.sha256 is None
    assert missing_snapshots.exists is False
    assert missing_snapshots.source_path is None


def test_snapshot_glob_discovers_only_matching_json_files(
    legacy_source_root: Path,
) -> None:
    _write_bytes(
        legacy_source_root,
        "data/snapshots/first.json",
        b"[]",
    )
    _write_bytes(
        legacy_source_root,
        "data/snapshots/second.json",
        b"{}",
    )
    _write_bytes(
        legacy_source_root,
        "data/snapshots/ignored.txt",
        b"not an inventory source",
    )

    snapshots = tuple(
        artifact
        for artifact in LegacyRuntimeStateInventory(
            legacy_source_root
        ).collect().artifacts
        if artifact.family is ArtifactFamily.SNAPSHOT
    )

    assert tuple(item.source_identifier for item in snapshots) == (
        "data/snapshots/first.json",
        "data/snapshots/second.json",
    )


def test_backup_family_discovers_nested_action_files(
    legacy_source_root: Path,
) -> None:
    _write_bytes(
        legacy_source_root,
        "data/backups/backup-a/actions.json",
        b'{"actions":[{"id":1}]}',
    )
    _write_bytes(
        legacy_source_root,
        "data/backups/backup-b/actions.json",
        b'{"actions":[]}',
    )

    backups = tuple(
        artifact
        for artifact in LegacyRuntimeStateInventory(
            legacy_source_root
        ).collect().artifacts
        if artifact.family is ArtifactFamily.BACKUP_ACTIONS
    )

    assert tuple(item.source_identifier for item in backups) == (
        "data/backups/backup-a/actions.json",
        "data/backups/backup-b/actions.json",
    )
    assert tuple(item.record_count for item in backups) == (1, 0)


def test_sensitive_payload_is_absent_from_repr_and_serialization(
    legacy_source_root: Path,
) -> None:
    sensitive_marker = "private-memory-content-4f9d73"
    _write_bytes(
        legacy_source_root,
        "data/memory/long_term_memory.json",
        json.dumps({"memories": [{"content": sensitive_marker}]}).encode(),
    )

    report = LegacyRuntimeStateInventory(legacy_source_root).collect()
    artifact = _find_artifact(
        report,
        "data/memory/long_term_memory.json",
    )
    serialized_report = json.dumps(report.to_dict())

    assert artifact.sensitivity is SensitivityClassification.HIGHLY_SENSITIVE
    assert sensitive_marker not in repr(artifact)
    assert sensitive_marker not in repr(report)
    assert sensitive_marker not in serialized_report
    assert "source_path" not in artifact.to_dict()


def test_repeated_runs_preserve_bytes_timestamp_and_tree(
    legacy_source_root: Path,
) -> None:
    source_path = _write_bytes(
        legacy_source_root,
        "data/history/actions.json",
        b'{\n  "actions": []\n}\n',
    )
    original_bytes = source_path.read_bytes()
    original_modified_ns = source_path.stat().st_mtime_ns
    original_tree = {
        path.relative_to(legacy_source_root).as_posix()
        for path in legacy_source_root.rglob("*")
    }
    inventory = LegacyRuntimeStateInventory(legacy_source_root)

    inventory.collect()
    inventory.collect()

    assert source_path.read_bytes() == original_bytes
    assert source_path.stat().st_mtime_ns == original_modified_ns
    assert {
        path.relative_to(legacy_source_root).as_posix()
        for path in legacy_source_root.rglob("*")
    } == original_tree


def test_source_root_is_mandatory_absolute_and_existing(
    tmp_path: Path,
) -> None:
    with pytest.raises(TypeError):
        LegacyRuntimeStateInventory()  # type: ignore[call-arg]

    with pytest.raises(
        RuntimeStateInventoryConfigurationError,
        match="source_root must be an absolute path",
    ):
        LegacyRuntimeStateInventory("relative-source")

    with pytest.raises(
        RuntimeStateInventoryConfigurationError,
        match="source_root must identify an existing directory",
    ):
        LegacyRuntimeStateInventory(tmp_path / "missing")


def test_inventory_does_not_consult_current_working_directory(
    tmp_path: Path,
    legacy_source_root: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    unrelated_cwd = tmp_path / "unrelated-cwd"
    unrelated_cwd.mkdir()
    cwd_marker = "cwd-content-must-not-be-inventoried"
    _write_bytes(
        unrelated_cwd,
        "data/goals/goals.json",
        json.dumps({"goal": cwd_marker}).encode(),
    )
    monkeypatch.chdir(unrelated_cwd)

    report = LegacyRuntimeStateInventory(legacy_source_root).collect()
    missing_goal = _find_artifact(report, "data/goals/goals.json")

    assert missing_goal.validation_status is ArtifactValidationStatus.MISSING
    assert cwd_marker not in json.dumps(report.to_dict())


def test_dry_run_dispositions_create_no_target_or_manifest(
    tmp_path: Path,
    legacy_source_root: Path,
) -> None:
    _write_bytes(
        legacy_source_root,
        "config/providers.json",
        b'{"providers":[]}',
    )
    migration_target = tmp_path / "canonical-runtime" / "migrations"
    inventory_manifest = legacy_source_root / "inventory.json"

    report = LegacyRuntimeStateInventory(legacy_source_root).collect()
    dispositions = {
        artifact.migration_disposition for artifact in report.artifacts
    }

    assert dispositions == set(MigrationDisposition)
    assert not migration_target.exists()
    assert not inventory_manifest.exists()


def test_supported_families_and_models_are_immutable(
    legacy_source_root: Path,
) -> None:
    report = LegacyRuntimeStateInventory(legacy_source_root).collect()

    assert {artifact.family for artifact in report.artifacts} == set(
        ArtifactFamily
    )
    with pytest.raises((AttributeError, TypeError)):
        report.artifacts = ()  # type: ignore[misc]
    with pytest.raises((AttributeError, TypeError)):
        report.artifacts[0].exists = True  # type: ignore[misc]


def test_classification_and_sensitivity_are_explicit(
    legacy_source_root: Path,
) -> None:
    report = LegacyRuntimeStateInventory(legacy_source_root).collect()
    provider_config = _find_artifact(report, "config/providers.json")
    system_log = _find_artifact(report, "logs/system.log")

    assert provider_config.classification is (
        ArtifactClassification.MUTABLE_CONFIGURATION
    )
    assert provider_config.sensitivity is (
        SensitivityClassification.SECRET_ADJACENT
    )
    assert provider_config.migration_disposition is (
        MigrationDisposition.CONFIGURATION_SPLIT_REQUIRED
    )
    assert system_log.classification is ArtifactClassification.LEGACY_LOG


def test_serialization_contains_structural_metadata_only(
    legacy_source_root: Path,
) -> None:
    private_value = "provider-response-private-value"
    source_path = _write_bytes(
        legacy_source_root,
        "data/providers/provider_memory.json",
        json.dumps({"provider_memory": [{"response": private_value}]}).encode(),
    )

    report = LegacyRuntimeStateInventory(legacy_source_root).collect()
    serialized = report.to_dict()
    serialized_text = json.dumps(serialized)
    artifact = _find_artifact(
        report,
        "data/providers/provider_memory.json",
    )

    assert private_value not in serialized_text
    assert str(source_path) not in serialized_text
    assert artifact.sha256 in serialized_text
    assert artifact.byte_size is not None
    assert artifact.modified_timestamp_ns is not None


def test_focused_inventory_preserves_real_protected_trees(
    legacy_source_root: Path,
    protected_repository_state: None,
) -> None:
    _write_bytes(
        legacy_source_root,
        "data/profile/user_profile.json",
        b'{"profile":"synthetic-only"}',
    )

    report = LegacyRuntimeStateInventory(legacy_source_root).collect()

    assert report.source_root == legacy_source_root.resolve()
