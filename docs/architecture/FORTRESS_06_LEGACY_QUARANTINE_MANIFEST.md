# FORTRESS-06 Legacy and Quarantine Manifest

Document ID: ARCH-FORTRESS-06

Document Version: 1.0

Certified Repository Baseline: v0.9.0-alpha

Development Target: v0.10.0-alpha

Status: In Progress — F06A implemented and verified candidate (uncommitted working tree)

Owner and Approval Authority: Founder Vinay B

Maintainer: JAOS Engineering

Last Updated: 2026-08-25

Related Documents:

- `docs/architecture/FORTRESS_PROGRAM.md`
- `docs/architecture/ARCHITECTURE_DECISIONS.md`
- `docs/engineering/RUNTIME_ARCHITECTURE_AUDIT.md`

Evidence Sources:

- `jaos_platform/runtime_state_inventory.py`
- `tests/tests/platform/test_canonical_import_boundary.py`

---

## 1. Purpose and Authority

This document is the authoritative FORTRESS-06 classification manifest for
canonical production systems, temporary compatibility debt, quarantine
candidates, archive-only sources, and sources that may be safe to delete only
after their owning F06 slice is separately authorized and verified.

F06A records classifications and strengthens the existing canonical import
boundary. It does not move, delete, rewrite, import-enable, or execute any
legacy source. It does not migrate or reclassify preserved runtime data.

The authoritative runtime-state artifact and writer metadata remains in
`jaos_platform/runtime_state_inventory.py`. This manifest records which source
groups own those writers without becoming a second runtime-state inventory.

---

## 2. Classification Vocabulary

| Code | Classification | Meaning |
|---|---|---|
| A | CANONICAL | Approved production owner or completed production scope that must be preserved. |
| B | COMPATIBILITY DEBT | Temporary compatibility behavior with an explicit later F06 owner. It must not become a second production authority. |
| C | MIGRATION INPUT | Preserved input governed by a migration decision; never implicitly deleted or rewritten. |
| D | QUARANTINE | Noncanonical or shadow implementation that must remain unreachable from canonical production pending controlled relocation. |
| E | ARCHIVE-ONLY | Historical source retained outside supported execution after its owning slice. |
| F | SAFE-TO-DELETE-LATER | No known caller at audit time; deletion remains prohibited until separately authorized and reverified. |
| G | UNKNOWN — NEEDS DECISION | Ownership or disposition requires a recorded decision before change. |

The absence of C and G entries from the source classification table does not
reclassify runtime data. Preserved artifacts, configuration, and unowned
runtime-state locations retain their FORTRESS-02 inventory dispositions.

---

## 3. Authoritative Source Classification

Configured-test dependency counts are direct importing modules observed by the
2026-08-25 F06 read-only audit. Counts may change only through an authorized
slice that updates this manifest and its evidence together.

<!-- F06A-CLASSIFICATION-ENTRIES:START -->
| Path or surface | Classification | Reason | Production reachability | Configured-test dependency | Runtime-state-writer ownership | Intended owner | Move/delete gate |
|---|---|---|---|---|---|---|---|
| `run_jaos.py` | A — CANONICAL | Sole supported production launcher. | Direct entry point. | Canonical launcher and composition tests. | None. | F06A boundary preservation. | PROHIBITED throughout F06. |
| `jaos_platform` | A — CANONICAL | Runtime, boot, lifecycle, service-container, and runtime-path authority; shadow consumers of `BasePlatformService` do not thereby become canonical. | Direct canonical closure. | Canonical platform suite. | Read-only inventory owner; not a legacy writer. | F06A boundary preservation. | PROHIBITED throughout F06. |
| `jaos.composition` | A — CANONICAL | Owns the composed Tool, AI, Executive, Memory, and Conversation graph. | Direct canonical closure. | Canonical composition suite. | None. | F06A boundary preservation. | PROHIBITED throughout F06. |
| `jaos.ai` | A — CANONICAL | Provider-independent AI authority. | Direct canonical closure. | Canonical AI and composition suites. | None. | F06A boundary preservation. | PROHIBITED throughout F06. |
| `jaos.memory` | A — CANONICAL | Persistent-memory contracts and provider authority. | Direct canonical closure. | Canonical Memory and composition suites. | None; distinct from root `memory`. | F06A boundary preservation. | PROHIBITED throughout F06. |
| `jaos.executive` | A — CANONICAL | System-action authority. | Direct canonical closure. | Canonical Executive and composition suites. | None. | F06A boundary preservation. | PROHIBITED throughout F06. |
| `jaos.tools` | A — CANONICAL | Controlled execution, permission, approval, and audit boundary. | Direct canonical closure. | Canonical Tool and composition suites. | Caller-supplied filesystem paths are excluded from the internal writer inventory. | F06A boundary preservation. | PROHIBITED throughout F06. |
| `jaos.intelligence.conversation` | A — CANONICAL | Completed Conversation Intelligence scope only; proposal/response authority without execution authority. | Composed in the canonical closure but not request-routed. | Conversation and composition suites. | None. | F06A boundary preservation. | PROHIBITED throughout F06. |
| `jaos.cli.command_dispatcher.CommandDispatcher self-construction fallback` | B — COMPATIBILITY DEBT | Zero-argument construction can still build Tool, AI, provider, and Executive collaborators. | Code is import-reachable; fallback is not called by `run_jaos.py`. | Two configured test modules plus excluded legacy CLI tests. | None. | F06C. | PROHIBITED until F06C caller and compatibility evidence is approved. |
| `jaos.cli.shell.JAOSShell dispatcher fallback` | B — COMPATIBILITY DEBT | Zero-argument shell construction creates a dispatcher and therefore a hidden composition path. | Code is import-reachable; fallback is not called by `run_jaos.py`. | One configured integration test module. | None. | F06C. | PROHIBITED until F06C caller and compatibility evidence is approved. |
| `jaos.intelligence lazy facades` | B — COMPATIBILITY DEBT | Lazily preserve public exports and submodule compatibility without loading deferred capabilities. | Import-reachable in canonical Conversation composition. | F05 import-boundary and public-contract tests. | None. | F06G. | PROHIBITED until an approved public-API decision and F06G evidence. |
| `brain/` | D — QUARANTINE | Large legacy reasoning, provider, permission, approval, audit, and state-writer stack. | Unreachable from `run_jaos.py`. | Zero configured direct importers; 270 excluded flat-test importers. | Owns `BehaviorTracker`, `DecisionRecord`, `GoalTracker`, `ProviderMemory`, `ReasoningTraceLogger`, `CrashRecoverySystem`, `UserProfile`, and `ProviderRouter` legacy writers. | F06D, F06E, and F06F. | PROHIBITED until test adjudication, writer isolation, relocation plan, and rollback evidence pass. |
| `communication/` | D — QUARANTINE | Top-level satellite service stack using the legacy runtime-service bridge. | Unreachable from `run_jaos.py`. | One configured direct importer. | None in FORTRESS-02 inventory. | F06D and F06E. | PROHIBITED until configured-test adjudication and F06E relocation approval. |
| `core/` | D — QUARANTINE | Legacy engine, kernel, composition, permission, recovery, and repository-state path. | Unreachable from `run_jaos.py`; reachable from legacy `main.py`. | Three configured direct importers. | Owns `ActionHistory`, `SnapshotManager`, `BackupManager`, and `ConfigManager` writers. | F06D, F06E, and F06F. | PROHIBITED until test adjudication, writer isolation, launcher decision, and rollback evidence pass. |
| `dashboard/` | D — QUARANTINE | Top-level satellite interface stack using the legacy runtime-service bridge. | Unreachable from `run_jaos.py`. | One configured direct importer. | None in FORTRESS-02 inventory. | F06D and F06E. | PROHIBITED until configured-test adjudication and F06E relocation approval. |
| `development/` | D — QUARANTINE | Top-level development-service prototypes using the legacy runtime-service bridge. | Unreachable from `run_jaos.py`. | One configured direct importer. | None in FORTRESS-02 inventory. | F06D and F06E. | PROHIBITED until configured-test adjudication and F06E relocation approval. |
| `engineering/` | D — QUARANTINE | Top-level engineering-service prototypes using the legacy runtime-service bridge. | Unreachable from `run_jaos.py`. | One configured direct importer. | None in FORTRESS-02 inventory. | F06D and F06E. | PROHIBITED until configured-test adjudication and F06E relocation approval. |
| `executive_brain/` | D — QUARANTINE | Parallel Executive, planning, registry, Memory, AI-provider, and Tool authority. | Unreachable from `run_jaos.py`. | Fifty-two configured direct importers. | The legacy file tool owns no internal runtime-state artifact. | F06D and F06E. | PROHIBITED until configured-test migration, caller inventory, relocation plan, and rollback evidence pass. |
| `infrastructure/` | D — QUARANTINE | Top-level provider and infrastructure-service prototypes using the legacy runtime-service bridge. | Unreachable from `run_jaos.py`. | One configured direct importer. | None in FORTRESS-02 inventory. | F06D and F06E. | PROHIBITED until configured-test adjudication and F06E relocation approval. |
| `kernel/` | D — QUARANTINE | Parallel boot, kernel, lifecycle, registry, permission, and runtime-context authorities. | Unreachable from `run_jaos.py`. | One configured direct importer. | None in FORTRESS-02 inventory. | F06D and F06E. | PROHIBITED until configured-test adjudication, caller inventory, and rollback evidence pass. |
| `knowledge/` | D — QUARANTINE | Top-level knowledge-service prototypes using the legacy runtime-service bridge. | Unreachable from `run_jaos.py`. | One configured direct importer. | None in FORTRESS-02 inventory. | F06D and F06E. | PROHIBITED until configured-test adjudication and F06E relocation approval. |
| `memory/` | D — QUARANTINE | Root legacy Memory implementation distinct from canonical `jaos.memory`. | Unreachable from `run_jaos.py`. | Zero configured direct importers; nine excluded flat-test importers. | Owns `LongTermMemory`, `MemoryCleanup`, and `MemoryExport` writers. | F06D, F06E, and F06F. | PROHIBITED until writer isolation, data-preservation proof, relocation plan, and rollback evidence pass. |
| `pc_control/` | D — QUARANTINE | Top-level application, browser, filesystem, terminal, and device-control prototypes. | Unreachable from `run_jaos.py`. | One configured direct importer. | None in FORTRESS-02 inventory. | F06D and F06E. | PROHIBITED until configured-test adjudication and F06E relocation approval. |
| `security/` | D — QUARANTINE | Parallel permission, authorization, identity, and audit prototypes; F07 policy is separate. | Unreachable from `run_jaos.py`. | One configured direct importer. | None in FORTRESS-02 inventory. | F06D and F06E. | PROHIBITED until configured-test adjudication and F06E relocation approval; no F07 policy work in F06. |
| `system_services/` | D — QUARANTINE | Top-level startup, backup, configuration, cache, and cleanup prototypes. | Unreachable from `run_jaos.py`. | One configured direct importer. | None in FORTRESS-02 inventory. | F06D and F06E. | PROHIBITED until configured-test adjudication and F06E relocation approval. |
| `workflow/` | D — QUARANTINE | Parallel workflow, task, dependency, retry, and automation authority. | Unreachable from `run_jaos.py`. | One configured direct importer. | None in FORTRESS-02 inventory. | F06D and F06E. | PROHIBITED until configured-test adjudication and F06E relocation approval. |
| `main.py` | D — QUARANTINE | Alternate launcher for `core.engine.JarvisEngine`; manually executable despite canonical non-reachability. | Not reachable from `run_jaos.py`; independently invokable. | No configured importer. | Indirectly reaches the `core` action-history, snapshot, and configuration writers. | F06E and F06F. | PROHIBITED until the legacy-launcher compatibility decision, writer isolation, and rollback evidence pass. |
| `phase14_integration_test.py` | E — ARCHIVE-ONLY | Historical root module-body script matching pytest's legacy filename pattern. | Unreachable from `run_jaos.py`; importable during repository-root collection. | Outside configured testpaths. | None in FORTRESS-02 inventory. | F06B and F06E. | PROHIBITED until collection remediation and archive relocation are separately approved. |
| `kernel/jaos_kernel_backup.py` | E — ARCHIVE-ONLY | Unreferenced executable backup of a shadow kernel; this file-specific archive classification refines but does not remove the root `kernel` quarantine prohibition. | Unreachable from `run_jaos.py`. | No configured importer. | None in FORTRESS-02 inventory. | F06E. | PROHIBITED until archive relocation and rollback evidence are separately approved. |
| `plugins/` | F — SAFE-TO-DELETE-LATER | One sample plugin with no known production or test caller; top-level plugins are not canonical. | Unreachable from `run_jaos.py`. | No configured importer. | None in FORTRESS-02 inventory. | F06E. | DELETION PROHIBITED until caller recheck and explicit removal authorization. |
| `test_logger.py` | F — SAFE-TO-DELETE-LATER | Root smoke script with no known caller; its module body emits one unconfigured log record. | Unreachable from `run_jaos.py`; importable during repository-root collection. | Outside configured testpaths. | None; `logs/system.log` has no legacy writer. | F06B and F06E. | DELETION PROHIBITED until collection handling and explicit removal authorization. |
| `infrastructure_intelligence_core.py` | F — SAFE-TO-DELETE-LATER | Unreferenced root duplicate of the packaged infrastructure component. | Unreachable from `run_jaos.py`. | No configured importer. | None in FORTRESS-02 inventory. | F06E. | DELETION PROHIBITED until caller recheck and explicit removal authorization. |
| `reasoning_assumption.py` | F — SAFE-TO-DELETE-LATER | Empty root module with no known caller; distinct from canonical `jaos.intelligence.models.reasoning_assumption`. | Unreachable from `run_jaos.py`. | No configured importer. | None in FORTRESS-02 inventory. | F06E. | DELETION PROHIBITED until caller recheck and explicit removal authorization. |
<!-- F06A-CLASSIFICATION-ENTRIES:END -->

Classification counts:

| Classification | Count |
|---|---:|
| A — CANONICAL | 8 |
| B — COMPATIBILITY DEBT | 3 |
| C — MIGRATION INPUT | 0 source entries |
| D — QUARANTINE | 16 |
| E — ARCHIVE-ONLY | 2 |
| F — SAFE-TO-DELETE-LATER | 4 |
| G — UNKNOWN — NEEDS DECISION | 0 source entries |
| Total classified source entries | 33 |

---

## 4. Canonical Import Guard Contract

The future quarantine namespace is the top-level module identity
`legacy_quarantine`. F06A reserves and forbids that identity before any source
is moved. F06A does not create the namespace or authorize relocation into it.

The following top-level identities must never enter the static production
import closure of `run_jaos.py`. This block is parsed by the existing canonical
import-boundary tests and must change atomically with the guard.

<!-- F06A-GUARDED-TOP-LEVEL-MODULES:START -->
- `brain`
- `communication`
- `core`
- `dashboard`
- `development`
- `engineering`
- `executive_brain`
- `infrastructure`
- `infrastructure_intelligence_core`
- `kernel`
- `knowledge`
- `legacy_quarantine`
- `main`
- `memory`
- `pc_control`
- `phase14_integration_test`
- `plugins`
- `reasoning_assumption`
- `security`
- `system_services`
- `test_logger`
- `workflow`
<!-- F06A-GUARDED-TOP-LEVEL-MODULES:END -->

The guard is based on the first dotted-name component. Therefore top-level
`memory`, `executive_brain`, or `plugins` is forbidden while canonical
`jaos.memory`, `jaos.executive`, `jaos.tools`, and `jaos.ai` remain allowed.

The pre-existing deferred capability guards for planning, reasoning, agents,
execution proposals, and Memory-context integration remain unchanged and are
not reclassified by F06A.

The analyzer follows repository-local static imports and also rejects literal
dynamic imports made with `import_module("...")`,
`importlib.import_module("...")`, or `__import__("...")`. Dynamic imports
whose module identity is computed at runtime remain outside static proof and
require complementary clean-import or runtime evidence.

---

## 5. Runtime-State Preservation

No preserved data or configuration path is classified as safe to delete by
this manifest. In particular, the seven currently modified runtime JSON files
remain protected migration or archive inputs, and F06A does not read their
payloads, rewrite them, migrate them, stage them, or change their inventory
dispositions.

All `brain`, `core`, and root `memory` writers recorded above must remain
unreachable from canonical production. Their code and associated artifacts may
move or change only in F06D, F06E, or F06F after the required caller, test,
data-preservation, and rollback evidence exists.

---

## 6. F06A State and Stop Boundary

F06A is limited to this manifest, the existing canonical import-boundary
infrastructure, focused tests, and minimum current-state documentation.

- No legacy source has moved or been deleted.
- No compatibility fallback has changed.
- No runtime-state writer or preserved artifact has changed.
- F06B and later F06 slices have not started.
- RAA-003 remains OPEN.
- RAA-007 remains PARTIALLY RESOLVED.
- FORTRESS-07 has not started.
- Step 7 remains IN PROGRESS.
- Step 8 and Fortress certification remain blocked or not started.
- Major Phase 8 expansion remains paused.

F06A is an IMPLEMENTED AND VERIFIED CANDIDATE in the uncommitted working tree.
The focused import-boundary suite passed 55 tests; the platform suite passed
363 tests with one skip; the affected composition suite passed 45 tests; and
the full configured `tests/tests` regression suite passed 2,037 tests with one
skip. The skip is the known Windows directory-symlink privilege limitation.
This evidence does not make F06A accepted, committed, certified, or complete the
FORTRESS-06 workstream.

---

## 7. Update History

| Date | Version | Change |
|---|---|---|
| 2026-08-25 | 1.0 | Created the authoritative F06 classification and canonical import-guard contract. No legacy source or runtime data moved. |
