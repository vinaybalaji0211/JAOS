"""Read-only inventory for preserved legacy JAOS runtime-state artifacts."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Final


class RuntimeStateInventoryConfigurationError(ValueError):
    """Raised when a legacy inventory source root is invalid."""


class ArtifactFamily(str, Enum):
    BEHAVIOR_PATTERNS = "BEHAVIOR_PATTERNS"
    DECISION_RECORDS = "DECISION_RECORDS"
    GOALS = "GOALS"
    LONG_TERM_MEMORY = "LONG_TERM_MEMORY"
    PROVIDER_MEMORY = "PROVIDER_MEMORY"
    REASONING_TRACES = "REASONING_TRACES"
    CRASH_CHECKPOINT = "CRASH_CHECKPOINT"
    USER_PROFILE = "USER_PROFILE"
    ACTION_HISTORY = "ACTION_HISTORY"
    SNAPSHOT = "SNAPSHOT"
    BACKUP_ACTIONS = "BACKUP_ACTIONS"
    SETTINGS = "SETTINGS"
    PROVIDER_CONFIGURATION = "PROVIDER_CONFIGURATION"
    MEMORY_EXPORT = "MEMORY_EXPORT"
    SYSTEM_LOG = "SYSTEM_LOG"


class ArtifactClassification(str, Enum):
    RUNTIME_STATE = "RUNTIME_STATE"
    HISTORICAL_RUNTIME_ARTIFACT = "HISTORICAL_RUNTIME_ARTIFACT"
    MUTABLE_CONFIGURATION = "MUTABLE_CONFIGURATION"
    GENERATED_EXPORT = "GENERATED_EXPORT"
    LEGACY_LOG = "LEGACY_LOG"
    UNKNOWN = "UNKNOWN"


class SensitivityClassification(str, Enum):
    NORMAL = "NORMAL"
    USER_SENSITIVE = "USER_SENSITIVE"
    HIGHLY_SENSITIVE = "HIGHLY_SENSITIVE"
    SECRET_ADJACENT = "SECRET_ADJACENT"


class MigrationDisposition(str, Enum):
    MIGRATION_CANDIDATE = "MIGRATION_CANDIDATE"
    ARCHIVE_ONLY = "ARCHIVE_ONLY"
    CONFIGURATION_SPLIT_REQUIRED = "CONFIGURATION_SPLIT_REQUIRED"
    REQUIRES_FOUNDER_OR_USER_APPROVAL = (
        "REQUIRES_FOUNDER_OR_USER_APPROVAL"
    )
    UNKNOWN_MANUAL_REVIEW_REQUIRED = "UNKNOWN_MANUAL_REVIEW_REQUIRED"


class WriterReachability(str, Enum):
    """Topology that can reach a legacy runtime-state writer."""

    RUN_JAOS = "RUN_JAOS"
    MAIN = "MAIN"
    CONFIGURED_TEST = "CONFIGURED_TEST"
    EXCLUDED_TEST = "EXCLUDED_TEST"
    DEVELOPER_TOOL = "DEVELOPER_TOOL"
    NO_KNOWN_CALLER = "NO_KNOWN_CALLER"


class FortressDisposition(str, Enum):
    """Fortress containment decision recorded by the FORTRESS-02G audit."""

    CANONICAL_EXTERNALIZED = "CANONICAL_EXTERNALIZED"
    PRESERVE_FOR_MIGRATION = "PRESERVE_FOR_MIGRATION"
    QUARANTINE_FORTRESS_06 = "QUARANTINE_FORTRESS_06"
    ARCHIVE_ONLY = "ARCHIVE_ONLY"
    CONFIG_SPLIT = "CONFIG_SPLIT"
    DEFERRED_ARCHITECTURE_DECISION = "DEFERRED_ARCHITECTURE_DECISION"


@dataclass(frozen=True, slots=True)
class RuntimeStateWriter:
    """Metadata identity of one writer. This module never imports writers."""

    module: str
    symbol: str
    reachability: tuple[WriterReachability, ...]
    fortress_disposition: FortressDisposition
    path_constant: str | None = None
    declared_path_literal: str | None = None
    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.reachability:
            raise RuntimeStateInventoryConfigurationError(
                "a writer must declare at least one reachability value"
            )

    @property
    def identifier(self) -> str:
        """Return the stable dotted identity of this writer."""

        return f"{self.module}.{self.symbol}"

    @property
    def statically_verifiable_path(self) -> bool:
        """Whether a class-level literal path constant is declared."""

        return (
            self.path_constant is not None
            and self.declared_path_literal is not None
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "module": self.module,
            "symbol": self.symbol,
            "reachability": [value.value for value in self.reachability],
            "fortress_disposition": self.fortress_disposition.value,
            "path_constant": self.path_constant,
            "declared_path_literal": self.declared_path_literal,
            "notes": self.notes,
        }


@dataclass(frozen=True, slots=True)
class UnownedRuntimeStateLocation:
    """A runtime-state location that exists but has no declared writer.

    These are directories rather than artifacts, so they are recorded
    separately instead of being forced into the artifact model.
    """

    location: str
    reachability: tuple[WriterReachability, ...]
    fortress_disposition: FortressDisposition
    notes: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "location": self.location,
            "reachability": [value.value for value in self.reachability],
            "fortress_disposition": self.fortress_disposition.value,
            "notes": self.notes,
        }


class ArtifactValidationStatus(str, Enum):
    VALID = "VALID"
    INVALID = "INVALID"
    MISSING = "MISSING"


class ArtifactFormat(str, Enum):
    JSON_ARRAY = "JSON_ARRAY"
    JSON_OBJECT = "JSON_OBJECT"
    JSON_SCALAR = "JSON_SCALAR"
    MALFORMED_JSON = "MALFORMED_JSON"
    TEXT = "TEXT"
    BINARY = "BINARY"
    UNKNOWN = "UNKNOWN"


class ArtifactSchemaShape(str, Enum):
    TOP_LEVEL_ARRAY = "TOP_LEVEL_ARRAY"
    TOP_LEVEL_OBJECT = "TOP_LEVEL_OBJECT"
    OBJECT_WITH_RECORD_COLLECTION = "OBJECT_WITH_RECORD_COLLECTION"
    SCALAR = "SCALAR"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True, slots=True)
class RuntimeStateArtifact:
    """Safe structural metadata for one legacy source artifact."""

    source_identifier: str
    family: ArtifactFamily
    classification: ArtifactClassification
    sensitivity: SensitivityClassification
    migration_disposition: MigrationDisposition
    validation_status: ArtifactValidationStatus
    detected_format: ArtifactFormat
    schema_shape: ArtifactSchemaShape
    exists: bool
    byte_size: int | None = None
    sha256: str | None = None
    modified_timestamp_ns: int | None = None
    schema_version: str | int | None = None
    record_count: int | None = None
    validation_detail: str | None = None
    fortress_disposition: FortressDisposition = (
        FortressDisposition.PRESERVE_FOR_MIGRATION
    )
    writers: tuple[RuntimeStateWriter, ...] = ()
    source_path: Path | None = field(default=None, repr=False)

    @property
    def reachability(self) -> tuple[WriterReachability, ...]:
        """Return the deduplicated, deterministically ordered reachability."""

        observed = {
            value
            for writer in self.writers
            for value in writer.reachability
        }
        if not observed:
            return (WriterReachability.NO_KNOWN_CALLER,)

        return tuple(
            value for value in WriterReachability if value in observed
        )

    @property
    def reachable_from_run_jaos(self) -> bool:
        """Whether any declared writer is reachable from run_jaos.py.

        Derived from recorded FORTRESS-02G evidence and enforced by the
        FORTRESS-02I canonical import guard. It is never established by
        executing JAOS.
        """

        return WriterReachability.RUN_JAOS in self.reachability

    def to_dict(self) -> dict[str, object]:
        """Return metadata only; source payloads are never serialized."""

        return {
            "source_identifier": self.source_identifier,
            "family": self.family.value,
            "classification": self.classification.value,
            "sensitivity": self.sensitivity.value,
            "migration_disposition": self.migration_disposition.value,
            "fortress_disposition": self.fortress_disposition.value,
            "validation_status": self.validation_status.value,
            "detected_format": self.detected_format.value,
            "schema_shape": self.schema_shape.value,
            "exists": self.exists,
            "byte_size": self.byte_size,
            "sha256": self.sha256,
            "modified_timestamp_ns": self.modified_timestamp_ns,
            "schema_version": self.schema_version,
            "record_count": self.record_count,
            "validation_detail": self.validation_detail,
            "reachability": [value.value for value in self.reachability],
            "reachable_from_run_jaos": self.reachable_from_run_jaos,
            "writers": [writer.to_dict() for writer in self.writers],
        }


@dataclass(frozen=True, slots=True)
class RuntimeStateInventoryReport:
    """Immutable result of one read-only legacy inventory run."""

    source_root: Path = field(repr=False)
    artifacts: tuple[RuntimeStateArtifact, ...]
    unowned_locations: tuple[UnownedRuntimeStateLocation, ...] = ()
    excluded_developer_writers: tuple[RuntimeStateWriter, ...] = ()
    documented_exclusions: tuple[str, ...] = ()

    @property
    def artifacts_reachable_from_run_jaos(
        self,
    ) -> tuple[RuntimeStateArtifact, ...]:
        """Return artifacts whose writers are canonically reachable."""

        return tuple(
            artifact
            for artifact in self.artifacts
            if artifact.reachable_from_run_jaos
        )

    def to_dict(self) -> dict[str, object]:
        """Return a pure metadata representation without writing a manifest."""

        return {
            "source_root": str(self.source_root),
            "artifacts": [artifact.to_dict() for artifact in self.artifacts],
            "unowned_locations": [
                location.to_dict() for location in self.unowned_locations
            ],
            "excluded_developer_writers": [
                writer.to_dict()
                for writer in self.excluded_developer_writers
            ],
            "documented_exclusions": list(self.documented_exclusions),
        }


@dataclass(frozen=True, slots=True)
class _ArtifactSpecification:
    source_pattern: str
    family: ArtifactFamily
    classification: ArtifactClassification
    sensitivity: SensitivityClassification
    migration_disposition: MigrationDisposition
    fortress_disposition: FortressDisposition
    writers: tuple[RuntimeStateWriter, ...] = ()
    record_keys: tuple[str, ...] = ()

    @property
    def uses_glob(self) -> bool:
        return "*" in self.source_pattern


_SCHEMA_VERSION_PATTERN: Final = re.compile(r"^[A-Za-z0-9_.-]{1,32}$")
_READ_CHUNK_SIZE: Final = 1024 * 1024

_ARTIFACT_SPECIFICATIONS: Final = (
    _ArtifactSpecification(
        source_pattern="data/behavior/behavior_patterns.json",
        family=ArtifactFamily.BEHAVIOR_PATTERNS,
        classification=ArtifactClassification.RUNTIME_STATE,
        sensitivity=SensitivityClassification.USER_SENSITIVE,
        migration_disposition=MigrationDisposition.MIGRATION_CANDIDATE,
        fortress_disposition=FortressDisposition.PRESERVE_FOR_MIGRATION,
        writers=(
            RuntimeStateWriter(
                module="brain.behavior_tracker",
                symbol="BehaviorTracker",
                reachability=(WriterReachability.EXCLUDED_TEST,),
                fortress_disposition=(
                    FortressDisposition.QUARANTINE_FORTRESS_06
                ),
                path_constant="FILE_PATH",
                declared_path_literal="data/behavior/behavior_patterns.json",
            ),
        ),
        record_keys=("behavior_patterns", "patterns"),
    ),
    _ArtifactSpecification(
        source_pattern="data/decisions/decision_records.json",
        family=ArtifactFamily.DECISION_RECORDS,
        classification=ArtifactClassification.RUNTIME_STATE,
        sensitivity=SensitivityClassification.USER_SENSITIVE,
        migration_disposition=MigrationDisposition.MIGRATION_CANDIDATE,
        fortress_disposition=FortressDisposition.PRESERVE_FOR_MIGRATION,
        writers=(
            RuntimeStateWriter(
                module="brain.decision_record",
                symbol="DecisionRecord",
                reachability=(WriterReachability.EXCLUDED_TEST,),
                fortress_disposition=(
                    FortressDisposition.QUARANTINE_FORTRESS_06
                ),
                path_constant="FILE_PATH",
                declared_path_literal="data/decisions/decision_records.json",
            ),
        ),
        record_keys=("decision_records", "decisions"),
    ),
    _ArtifactSpecification(
        source_pattern="data/goals/goals.json",
        family=ArtifactFamily.GOALS,
        classification=ArtifactClassification.RUNTIME_STATE,
        sensitivity=SensitivityClassification.USER_SENSITIVE,
        migration_disposition=(
            MigrationDisposition.REQUIRES_FOUNDER_OR_USER_APPROVAL
        ),
        fortress_disposition=FortressDisposition.PRESERVE_FOR_MIGRATION,
        writers=(
            RuntimeStateWriter(
                module="brain.goal_tracker",
                symbol="GoalTracker",
                reachability=(WriterReachability.EXCLUDED_TEST,),
                fortress_disposition=(
                    FortressDisposition.QUARANTINE_FORTRESS_06
                ),
                path_constant="FILE_PATH",
                declared_path_literal="data/goals/goals.json",
            ),
        ),
        record_keys=("goals",),
    ),
    _ArtifactSpecification(
        source_pattern="data/memory/long_term_memory.json",
        family=ArtifactFamily.LONG_TERM_MEMORY,
        classification=ArtifactClassification.RUNTIME_STATE,
        sensitivity=SensitivityClassification.HIGHLY_SENSITIVE,
        migration_disposition=(
            MigrationDisposition.REQUIRES_FOUNDER_OR_USER_APPROVAL
        ),
        fortress_disposition=FortressDisposition.PRESERVE_FOR_MIGRATION,
        writers=(
            RuntimeStateWriter(
                module="memory.long_term_memory",
                symbol="LongTermMemory",
                reachability=(WriterReachability.EXCLUDED_TEST,),
                fortress_disposition=(
                    FortressDisposition.QUARANTINE_FORTRESS_06
                ),
                path_constant="FILE_PATH",
                declared_path_literal="data/memory/long_term_memory.json",
                notes=(
                    "root legacy memory package; distinct from canonical "
                    "jaos.memory"
                ),
            ),
            RuntimeStateWriter(
                module="memory.memory_cleanup",
                symbol="MemoryCleanup",
                reachability=(WriterReachability.EXCLUDED_TEST,),
                fortress_disposition=(
                    FortressDisposition.QUARANTINE_FORTRESS_06
                ),
                notes=(
                    "rewrites the same artifact; its directory literal is "
                    "method-local, so no class constant is statically "
                    "verifiable"
                ),
            ),
        ),
        record_keys=("memories", "records"),
    ),
    _ArtifactSpecification(
        source_pattern="data/providers/provider_memory.json",
        family=ArtifactFamily.PROVIDER_MEMORY,
        classification=ArtifactClassification.RUNTIME_STATE,
        sensitivity=SensitivityClassification.USER_SENSITIVE,
        migration_disposition=(
            MigrationDisposition.UNKNOWN_MANUAL_REVIEW_REQUIRED
        ),
        fortress_disposition=FortressDisposition.PRESERVE_FOR_MIGRATION,
        writers=(
            RuntimeStateWriter(
                module="brain.provider_memory",
                symbol="ProviderMemory",
                reachability=(WriterReachability.EXCLUDED_TEST,),
                fortress_disposition=(
                    FortressDisposition.QUARANTINE_FORTRESS_06
                ),
                path_constant="FILE_PATH",
                declared_path_literal="data/providers/provider_memory.json",
                notes=(
                    "its only non-test caller, brain.provider_benchmark, is "
                    "itself reachable solely from excluded tests"
                ),
            ),
        ),
        record_keys=("provider_memory", "providers", "records"),
    ),
    _ArtifactSpecification(
        source_pattern="data/reasoning/reasoning_traces.json",
        family=ArtifactFamily.REASONING_TRACES,
        classification=ArtifactClassification.RUNTIME_STATE,
        sensitivity=SensitivityClassification.HIGHLY_SENSITIVE,
        migration_disposition=MigrationDisposition.ARCHIVE_ONLY,
        fortress_disposition=FortressDisposition.ARCHIVE_ONLY,
        writers=(
            RuntimeStateWriter(
                module="brain.reasoning_trace_logger",
                symbol="ReasoningTraceLogger",
                reachability=(WriterReachability.EXCLUDED_TEST,),
                fortress_disposition=(
                    FortressDisposition.QUARANTINE_FORTRESS_06
                ),
                path_constant="FILE_PATH",
                declared_path_literal="data/reasoning/reasoning_traces.json",
            ),
        ),
        record_keys=("reasoning_traces", "traces"),
    ),
    _ArtifactSpecification(
        source_pattern="data/recovery/crash_checkpoint.json",
        family=ArtifactFamily.CRASH_CHECKPOINT,
        classification=ArtifactClassification.RUNTIME_STATE,
        sensitivity=SensitivityClassification.HIGHLY_SENSITIVE,
        migration_disposition=MigrationDisposition.ARCHIVE_ONLY,
        fortress_disposition=FortressDisposition.ARCHIVE_ONLY,
        writers=(
            RuntimeStateWriter(
                module="brain.crash_recovery_system",
                symbol="CrashRecoverySystem",
                reachability=(WriterReachability.EXCLUDED_TEST,),
                fortress_disposition=(
                    FortressDisposition.QUARANTINE_FORTRESS_06
                ),
                path_constant="FILE_PATH",
                declared_path_literal="data/recovery/crash_checkpoint.json",
            ),
        ),
    ),
    _ArtifactSpecification(
        source_pattern="data/profile/user_profile.json",
        family=ArtifactFamily.USER_PROFILE,
        classification=ArtifactClassification.RUNTIME_STATE,
        sensitivity=SensitivityClassification.HIGHLY_SENSITIVE,
        migration_disposition=(
            MigrationDisposition.REQUIRES_FOUNDER_OR_USER_APPROVAL
        ),
        fortress_disposition=FortressDisposition.PRESERVE_FOR_MIGRATION,
        writers=(
            RuntimeStateWriter(
                module="brain.user_profile",
                symbol="UserProfile",
                reachability=(WriterReachability.EXCLUDED_TEST,),
                fortress_disposition=(
                    FortressDisposition.QUARANTINE_FORTRESS_06
                ),
                path_constant="FILE_PATH",
                declared_path_literal="data/profile/user_profile.json",
            ),
        ),
    ),
    _ArtifactSpecification(
        source_pattern="data/history/actions.json",
        family=ArtifactFamily.ACTION_HISTORY,
        classification=ArtifactClassification.HISTORICAL_RUNTIME_ARTIFACT,
        sensitivity=SensitivityClassification.USER_SENSITIVE,
        migration_disposition=MigrationDisposition.MIGRATION_CANDIDATE,
        fortress_disposition=FortressDisposition.PRESERVE_FOR_MIGRATION,
        writers=(
            RuntimeStateWriter(
                module="core.action_history",
                symbol="ActionHistory",
                reachability=(WriterReachability.MAIN,),
                fortress_disposition=(
                    FortressDisposition.QUARANTINE_FORTRESS_06
                ),
                path_constant="FILE_PATH",
                declared_path_literal="data/history/actions.json",
                notes=(
                    "legacy main.py path only; retirement belongs to "
                    "FORTRESS-04 and FORTRESS-06"
                ),
            ),
        ),
        record_keys=("actions",),
    ),
    _ArtifactSpecification(
        source_pattern="data/snapshots/*.json",
        family=ArtifactFamily.SNAPSHOT,
        classification=ArtifactClassification.HISTORICAL_RUNTIME_ARTIFACT,
        sensitivity=SensitivityClassification.HIGHLY_SENSITIVE,
        migration_disposition=MigrationDisposition.ARCHIVE_ONLY,
        fortress_disposition=FortressDisposition.ARCHIVE_ONLY,
        writers=(
            RuntimeStateWriter(
                module="core.snapshot_manager",
                symbol="SnapshotManager",
                reachability=(WriterReachability.MAIN,),
                fortress_disposition=(
                    FortressDisposition.QUARANTINE_FORTRESS_06
                ),
                notes=(
                    "directory literal is method-local, so no class "
                    "constant is statically verifiable"
                ),
            ),
        ),
        record_keys=("records", "memories", "actions"),
    ),
    _ArtifactSpecification(
        source_pattern="data/backups/*/actions.json",
        family=ArtifactFamily.BACKUP_ACTIONS,
        classification=ArtifactClassification.HISTORICAL_RUNTIME_ARTIFACT,
        sensitivity=SensitivityClassification.HIGHLY_SENSITIVE,
        migration_disposition=MigrationDisposition.ARCHIVE_ONLY,
        fortress_disposition=FortressDisposition.ARCHIVE_ONLY,
        writers=(
            RuntimeStateWriter(
                module="core.backup_manager",
                symbol="BackupManager",
                reachability=(WriterReachability.NO_KNOWN_CALLER,),
                fortress_disposition=FortressDisposition.ARCHIVE_ONLY,
                notes=(
                    "no caller anywhere in the repository; distinct from "
                    "system_services.backup_manager"
                ),
            ),
        ),
        record_keys=("actions",),
    ),
    _ArtifactSpecification(
        source_pattern="config/settings.json",
        family=ArtifactFamily.SETTINGS,
        classification=ArtifactClassification.MUTABLE_CONFIGURATION,
        sensitivity=SensitivityClassification.USER_SENSITIVE,
        migration_disposition=(
            MigrationDisposition.CONFIGURATION_SPLIT_REQUIRED
        ),
        fortress_disposition=FortressDisposition.CONFIG_SPLIT,
        writers=(
            RuntimeStateWriter(
                module="core.config_manager",
                symbol="ConfigManager",
                reachability=(
                    WriterReachability.MAIN,
                    WriterReachability.CONFIGURED_TEST,
                ),
                fortress_disposition=(
                    FortressDisposition.CANONICAL_EXTERNALIZED
                ),
                path_constant="FILE_PATH",
                declared_path_literal="config/settings.json",
                notes=(
                    "FORTRESS-02H externalized mutable settings to the "
                    "injected profile config scope; this repository file is "
                    "now a read-only defaults source and is never written"
                ),
            ),
        ),
    ),
    _ArtifactSpecification(
        source_pattern="config/providers.json",
        family=ArtifactFamily.PROVIDER_CONFIGURATION,
        classification=ArtifactClassification.MUTABLE_CONFIGURATION,
        sensitivity=SensitivityClassification.SECRET_ADJACENT,
        migration_disposition=(
            MigrationDisposition.CONFIGURATION_SPLIT_REQUIRED
        ),
        fortress_disposition=(
            FortressDisposition.DEFERRED_ARCHITECTURE_DECISION
        ),
        writers=(
            RuntimeStateWriter(
                module="brain.provider_router",
                symbol="ProviderRouter",
                reachability=(WriterReachability.EXCLUDED_TEST,),
                fortress_disposition=(
                    FortressDisposition.QUARANTINE_FORTRESS_06
                ),
                path_constant="PROVIDER_FILE",
                declared_path_literal="config/providers.json",
                notes=(
                    "distinct from the canonical jaos.ai.routing "
                    "ProviderRouter; catalog ownership remains deferred"
                ),
            ),
        ),
        record_keys=("providers",),
    ),
    _ArtifactSpecification(
        source_pattern="exports/memory_export_*.json",
        family=ArtifactFamily.MEMORY_EXPORT,
        classification=ArtifactClassification.GENERATED_EXPORT,
        sensitivity=SensitivityClassification.HIGHLY_SENSITIVE,
        migration_disposition=MigrationDisposition.ARCHIVE_ONLY,
        fortress_disposition=FortressDisposition.ARCHIVE_ONLY,
        writers=(
            RuntimeStateWriter(
                module="memory.memory_export",
                symbol="MemoryExport",
                reachability=(WriterReachability.EXCLUDED_TEST,),
                fortress_disposition=(
                    FortressDisposition.QUARANTINE_FORTRESS_06
                ),
                path_constant="EXPORT_FOLDER",
                declared_path_literal="exports",
                notes=(
                    "emits a new timestamped file per call with no "
                    "retention cap"
                ),
            ),
        ),
        record_keys=("memories", "records"),
    ),
    _ArtifactSpecification(
        source_pattern="logs/system.log",
        family=ArtifactFamily.SYSTEM_LOG,
        classification=ArtifactClassification.LEGACY_LOG,
        sensitivity=SensitivityClassification.HIGHLY_SENSITIVE,
        migration_disposition=MigrationDisposition.ARCHIVE_ONLY,
        fortress_disposition=FortressDisposition.ARCHIVE_ONLY,
        writers=(),
    ),
)


UNOWNED_RUNTIME_STATE_LOCATIONS: Final = (
    UnownedRuntimeStateLocation(
        location="data/cache",
        reachability=(WriterReachability.NO_KNOWN_CALLER,),
        fortress_disposition=(
            FortressDisposition.DEFERRED_ARCHITECTURE_DECISION
        ),
        notes=(
            "empty directory present on disk with no writer and no path "
            "literal anywhere in the repository"
        ),
    ),
    UnownedRuntimeStateLocation(
        location="data/diagnostics",
        reachability=(WriterReachability.NO_KNOWN_CALLER,),
        fortress_disposition=(
            FortressDisposition.DEFERRED_ARCHITECTURE_DECISION
        ),
        notes=(
            "empty directory present on disk with no writer and no path "
            "literal anywhere in the repository"
        ),
    ),
)


EXCLUDED_DEVELOPER_WRITERS: Final = (
    RuntimeStateWriter(
        module="scripts.generate_dg1_docs",
        symbol="write_file",
        reachability=(WriterReachability.DEVELOPER_TOOL,),
        fortress_disposition=FortressDisposition.ARCHIVE_ONLY,
        notes=(
            "developer documentation tooling that backs up and regenerates "
            "tracked repository documentation; it is not JAOS internal "
            "runtime state and is deliberately outside the artifact model"
        ),
    ),
)


DOCUMENTED_INVENTORY_EXCLUSIONS: Final = (
    "jaos.tools.filesystem: user-directed filesystem tools operate on "
    "caller-supplied paths and are not internal runtime-state writers",
    "executive_brain.tools.file: duplicate legacy or shadow filesystem "
    "stack with no importer; it is a forbidden canonical dependency "
    "enforced by the FORTRESS-02I import guard and owns no runtime-state "
    "artifact",
)


class LegacyRuntimeStateInventory:
    """Inventory preserved artifacts beneath one explicit legacy source root."""

    def __init__(self, source_root: str | Path) -> None:
        try:
            candidate = Path(source_root)
        except (TypeError, ValueError, OSError) as error:
            raise RuntimeStateInventoryConfigurationError(
                "source_root must be a valid absolute directory path"
            ) from error

        if not candidate.is_absolute():
            raise RuntimeStateInventoryConfigurationError(
                "source_root must be an absolute path"
            )

        try:
            canonical_root = candidate.resolve(strict=True)
        except (OSError, RuntimeError) as error:
            raise RuntimeStateInventoryConfigurationError(
                "source_root must identify an existing directory"
            ) from error

        if not canonical_root.is_dir():
            raise RuntimeStateInventoryConfigurationError(
                "source_root must identify an existing directory"
            )

        self._source_root = canonical_root

    @property
    def source_root(self) -> Path:
        return self._source_root

    def collect(self) -> RuntimeStateInventoryReport:
        """Collect safe metadata without modifying sources or writing output."""

        artifacts: list[RuntimeStateArtifact] = []
        for specification in _ARTIFACT_SPECIFICATIONS:
            artifacts.extend(self._collect_specification(specification))

        artifacts.sort(key=lambda artifact: artifact.source_identifier)
        return RuntimeStateInventoryReport(
            source_root=self._source_root,
            artifacts=tuple(artifacts),
            unowned_locations=UNOWNED_RUNTIME_STATE_LOCATIONS,
            excluded_developer_writers=EXCLUDED_DEVELOPER_WRITERS,
            documented_exclusions=DOCUMENTED_INVENTORY_EXCLUSIONS,
        )

    def _collect_specification(
        self,
        specification: _ArtifactSpecification,
    ) -> list[RuntimeStateArtifact]:
        if not specification.uses_glob:
            source_path = self._source_root / specification.source_pattern
            return [self._inspect(source_path, specification)]

        matches = sorted(
            self._source_root.glob(specification.source_pattern),
            key=lambda path: path.as_posix(),
        )
        if not matches:
            return [self._missing_glob(specification)]

        return [
            self._inspect(source_path, specification)
            for source_path in matches
        ]

    def _inspect(
        self,
        source_path: Path,
        specification: _ArtifactSpecification,
    ) -> RuntimeStateArtifact:
        source_identifier = source_path.relative_to(
            self._source_root
        ).as_posix()

        if not source_path.exists():
            if source_path.is_symlink():
                return self._invalid(
                    source_identifier,
                    source_path,
                    specification,
                    "UNSAFE_SOURCE_PATH",
                )
            return self._missing(
                source_identifier,
                source_path,
                specification,
            )

        try:
            canonical_source = source_path.resolve(strict=True)
            canonical_source.relative_to(self._source_root)
        except (OSError, RuntimeError, ValueError):
            return self._invalid(
                source_identifier,
                source_path,
                specification,
                "UNSAFE_SOURCE_PATH",
            )

        if not canonical_source.is_file():
            return self._invalid(
                source_identifier,
                source_path,
                specification,
                "SOURCE_IS_NOT_A_FILE",
            )

        return self._read_source(
            source_identifier,
            source_path,
            specification,
        )

    def _read_source(
        self,
        source_identifier: str,
        source_path: Path,
        specification: _ArtifactSpecification,
    ) -> RuntimeStateArtifact:
        digest = hashlib.sha256()
        payload = bytearray()
        byte_size = 0

        try:
            before = source_path.stat()
            with source_path.open("rb") as stream:
                for chunk in iter(
                    lambda: stream.read(_READ_CHUNK_SIZE),
                    b"",
                ):
                    digest.update(chunk)
                    payload.extend(chunk)
                    byte_size += len(chunk)
            after = source_path.stat()
        except OSError:
            return self._invalid(
                source_identifier,
                source_path,
                specification,
                "SOURCE_READ_ERROR",
            )

        if (
            before.st_size != after.st_size
            or before.st_mtime_ns != after.st_mtime_ns
            or byte_size != after.st_size
        ):
            return RuntimeStateArtifact(
                source_identifier=source_identifier,
                source_path=source_path,
                family=specification.family,
                classification=specification.classification,
                sensitivity=specification.sensitivity,
                migration_disposition=(
                    specification.migration_disposition
                ),
                fortress_disposition=specification.fortress_disposition,
                writers=specification.writers,
                validation_status=ArtifactValidationStatus.INVALID,
                validation_detail="SOURCE_CHANGED_DURING_READ",
                detected_format=ArtifactFormat.UNKNOWN,
                schema_shape=ArtifactSchemaShape.UNKNOWN,
                exists=True,
                byte_size=byte_size,
                sha256=digest.hexdigest(),
                modified_timestamp_ns=after.st_mtime_ns,
            )

        inspection = self._inspect_payload(
            source_path=source_path,
            payload=bytes(payload),
            record_keys=specification.record_keys,
        )
        return RuntimeStateArtifact(
            source_identifier=source_identifier,
            source_path=source_path,
            family=specification.family,
            classification=specification.classification,
            sensitivity=specification.sensitivity,
            migration_disposition=specification.migration_disposition,
            fortress_disposition=specification.fortress_disposition,
            writers=specification.writers,
            validation_status=inspection.validation_status,
            validation_detail=inspection.validation_detail,
            detected_format=inspection.detected_format,
            schema_shape=inspection.schema_shape,
            exists=True,
            byte_size=byte_size,
            sha256=digest.hexdigest(),
            modified_timestamp_ns=after.st_mtime_ns,
            schema_version=inspection.schema_version,
            record_count=inspection.record_count,
        )

    @staticmethod
    def _inspect_payload(
        *,
        source_path: Path,
        payload: bytes,
        record_keys: tuple[str, ...],
    ) -> _PayloadInspection:
        if source_path.suffix.lower() == ".json":
            return LegacyRuntimeStateInventory._inspect_json(
                payload,
                record_keys,
            )

        if source_path.suffix.lower() == ".log":
            try:
                payload.decode("utf-8")
            except UnicodeDecodeError:
                detected_format = ArtifactFormat.BINARY
            else:
                detected_format = ArtifactFormat.TEXT
            return _PayloadInspection(
                validation_status=ArtifactValidationStatus.VALID,
                detected_format=detected_format,
                schema_shape=ArtifactSchemaShape.UNKNOWN,
            )

        return _PayloadInspection(
            validation_status=ArtifactValidationStatus.VALID,
            detected_format=ArtifactFormat.UNKNOWN,
            schema_shape=ArtifactSchemaShape.UNKNOWN,
        )

    @staticmethod
    def _inspect_json(
        payload: bytes,
        record_keys: tuple[str, ...],
    ) -> _PayloadInspection:
        try:
            parsed = json.loads(payload)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return _PayloadInspection(
                validation_status=ArtifactValidationStatus.INVALID,
                validation_detail="MALFORMED_JSON",
                detected_format=ArtifactFormat.MALFORMED_JSON,
                schema_shape=ArtifactSchemaShape.UNKNOWN,
            )

        if isinstance(parsed, list):
            return _PayloadInspection(
                validation_status=ArtifactValidationStatus.VALID,
                detected_format=ArtifactFormat.JSON_ARRAY,
                schema_shape=ArtifactSchemaShape.TOP_LEVEL_ARRAY,
                record_count=len(parsed),
            )

        if isinstance(parsed, dict):
            record_count = len(parsed)
            schema_shape = ArtifactSchemaShape.TOP_LEVEL_OBJECT
            for record_key in record_keys:
                records = parsed.get(record_key)
                if isinstance(records, list):
                    record_count = len(records)
                    schema_shape = (
                        ArtifactSchemaShape.OBJECT_WITH_RECORD_COLLECTION
                    )
                    break

            return _PayloadInspection(
                validation_status=ArtifactValidationStatus.VALID,
                detected_format=ArtifactFormat.JSON_OBJECT,
                schema_shape=schema_shape,
                schema_version=(
                    LegacyRuntimeStateInventory._schema_version(parsed)
                ),
                record_count=record_count,
            )

        return _PayloadInspection(
            validation_status=ArtifactValidationStatus.VALID,
            detected_format=ArtifactFormat.JSON_SCALAR,
            schema_shape=ArtifactSchemaShape.SCALAR,
        )

    @staticmethod
    def _schema_version(parsed: dict[object, object]) -> str | int | None:
        for key in ("schema_version", "version"):
            value = parsed.get(key)
            if isinstance(value, bool):
                continue
            if isinstance(value, int):
                return value
            if (
                isinstance(value, str)
                and _SCHEMA_VERSION_PATTERN.fullmatch(value) is not None
            ):
                return value
        return None

    def _missing_glob(
        self,
        specification: _ArtifactSpecification,
    ) -> RuntimeStateArtifact:
        return self._missing(
            specification.source_pattern,
            None,
            specification,
        )

    @staticmethod
    def _missing(
        source_identifier: str,
        source_path: Path | None,
        specification: _ArtifactSpecification,
    ) -> RuntimeStateArtifact:
        return RuntimeStateArtifact(
            source_identifier=source_identifier,
            source_path=source_path,
            family=specification.family,
            classification=specification.classification,
            sensitivity=specification.sensitivity,
            migration_disposition=specification.migration_disposition,
            fortress_disposition=specification.fortress_disposition,
            writers=specification.writers,
            validation_status=ArtifactValidationStatus.MISSING,
            validation_detail="SOURCE_NOT_FOUND",
            detected_format=ArtifactFormat.UNKNOWN,
            schema_shape=ArtifactSchemaShape.UNKNOWN,
            exists=False,
        )

    @staticmethod
    def _invalid(
        source_identifier: str,
        source_path: Path,
        specification: _ArtifactSpecification,
        validation_detail: str,
    ) -> RuntimeStateArtifact:
        return RuntimeStateArtifact(
            source_identifier=source_identifier,
            source_path=source_path,
            family=specification.family,
            classification=specification.classification,
            sensitivity=specification.sensitivity,
            migration_disposition=specification.migration_disposition,
            fortress_disposition=specification.fortress_disposition,
            writers=specification.writers,
            validation_status=ArtifactValidationStatus.INVALID,
            validation_detail=validation_detail,
            detected_format=ArtifactFormat.UNKNOWN,
            schema_shape=ArtifactSchemaShape.UNKNOWN,
            exists=True,
        )


@dataclass(frozen=True, slots=True)
class _PayloadInspection:
    validation_status: ArtifactValidationStatus
    detected_format: ArtifactFormat
    schema_shape: ArtifactSchemaShape
    schema_version: str | int | None = None
    record_count: int | None = None
    validation_detail: str | None = None


__all__ = [
    "ArtifactClassification",
    "ArtifactFamily",
    "ArtifactFormat",
    "ArtifactSchemaShape",
    "ArtifactValidationStatus",
    "DOCUMENTED_INVENTORY_EXCLUSIONS",
    "EXCLUDED_DEVELOPER_WRITERS",
    "FortressDisposition",
    "LegacyRuntimeStateInventory",
    "MigrationDisposition",
    "RuntimeStateArtifact",
    "RuntimeStateInventoryConfigurationError",
    "RuntimeStateInventoryReport",
    "RuntimeStateWriter",
    "SensitivityClassification",
    "UNOWNED_RUNTIME_STATE_LOCATIONS",
    "UnownedRuntimeStateLocation",
    "WriterReachability",
]
