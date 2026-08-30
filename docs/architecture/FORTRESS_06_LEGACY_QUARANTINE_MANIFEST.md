# FORTRESS-06 Legacy and Quarantine Manifest

Document ID: ARCH-FORTRESS-06

Document Version: 1.7

Certified Repository Baseline: v0.9.0-alpha

Development Target: v0.10.0-alpha

Status: In Progress — F06D1, F06D2A, and F06D2B committed and pushed;
F06D2C IMPLEMENTED AND VERIFIED; F06D2D+ not started

Owner and Approval Authority: Founder Vinay B

Maintainer: JAOS Engineering

Last Updated: 2026-08-30

Related Documents:

- `docs/architecture/FORTRESS_PROGRAM.md`
- `docs/architecture/ARCHITECTURE_DECISIONS.md`
- `docs/engineering/RUNTIME_ARCHITECTURE_AUDIT.md`

Evidence Sources:

- `jaos_platform/runtime_state_inventory.py`
- `pytest.ini`
- `tests/tests/platform/test_collection_containment.py`
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

F06B preserves two unsupported root test-shaped scripts as byte-identical,
non-Python `.py.legacy` artifacts, then adopts pytest importlib mode through
the single existing pytest configuration. It moves no other legacy source.

F06C removes hidden CLI self-composition and lifecycle ownership. Its
injected-adapter implementation is committed and pushed at checkpoint
`0a2ea60` and resolves RAA-007 with evidence without completing the
FORTRESS-06 workstream.

F06D1 quarantines eight duplicate AI and Core configured test files to
`legacy_quarantine/tests/` as byte-identical, non-Python `.py.legacy` artifacts
without deleting them. Configured legacy-importing test files reduce from 67
to 59, and 50 source test definitions are retired from configured execution.
It is committed and pushed at checkpoint `51818d2`.

F06D2A archives the seven `executive_brain` filesystem-tool configured test
files to `legacy_quarantine/tests/tools/filesystem/` as byte-identical,
non-Python `.py.legacy` artifacts and replaces the seven configured paths with
canonical `jaos.tools.filesystem` tests. Configured legacy-importing test files
reduce from 59 to 52, 56 source test definitions are retired from configured
execution, and 100 canonical configured tests take their place. No production
code changed. It is committed and pushed at checkpoint `95adce4`.

F06D2B archives the four `executive_brain.tools.core` Tool Platform configured
test files to `legacy_quarantine/tests/tools/core/` as byte-identical,
non-Python `.py.legacy` artifacts and replaces the four configured paths with
canonical `jaos.tools` tests. Configured legacy-importing test files reduce from
52 to 48, 25 source test definitions are retired from configured execution, and
19 canonical configured tests take their place. No production code changed and
no FORTRESS-07 permission, approval, or audit policy was redesigned.

F06D2C archives four monolithic ExecutiveBrain/executive-pipeline configured
test files carrying 22 source tests to
`legacy_quarantine/tests/executive/` as byte-identical, non-Python
`.py.legacy` artifacts. Two canonical source tests, collected as three cases,
now prove deterministic `ExecutiveController` -> `ToolManager` execution and
safe blank/whitespace failure without Tool execution. Configured
legacy-importing files reduce from 48 to 44 and configured `executive_brain`
importers from 35 to 31. No production code or runtime data changed.

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
| `jaos.cli.command_dispatcher.CommandDispatcher injected adapter` | A — CANONICAL | Requires injected Tool, AI, and Executive collaborators and routes CLI requests without constructing or lifecycle-owning them. | Direct canonical closure through `run_jaos.py`. | Canonical CLI, composition, integration, and architecture-boundary tests. | None. | F06C boundary preservation. | PROHIBITED throughout F06. |
| `jaos.cli.shell.JAOSShell injected adapter` | A — CANONICAL | Requires an injected dispatcher and owns only the interactive input and EOF loop, not dispatcher composition or platform lifecycle. | Direct canonical closure through `run_jaos.py`. | Canonical shell, launcher, integration, and architecture-boundary tests. | None. | F06C boundary preservation. | PROHIBITED throughout F06. |
| `jaos.intelligence lazy facades` | B — COMPATIBILITY DEBT | Lazily preserve public exports and submodule compatibility without loading deferred capabilities. | Import-reachable in canonical Conversation composition. | F05 import-boundary and public-contract tests. | None. | F06G. | PROHIBITED until an approved public-API decision and F06G evidence. |
| `brain/` | D — QUARANTINE | Large legacy reasoning, provider, permission, approval, audit, and state-writer stack. | Unreachable from `run_jaos.py`. | Zero configured direct importers; 270 excluded flat-test importers. | Owns `BehaviorTracker`, `DecisionRecord`, `GoalTracker`, `ProviderMemory`, `ReasoningTraceLogger`, `CrashRecoverySystem`, `UserProfile`, and `ProviderRouter` legacy writers. | F06D, F06E, and F06F. | PROHIBITED until test adjudication, writer isolation, relocation plan, and rollback evidence pass. |
| `communication/` | D — QUARANTINE | Top-level satellite service stack using the legacy runtime-service bridge. | Unreachable from `run_jaos.py`. | One configured direct importer. | None in FORTRESS-02 inventory. | F06D and F06E. | PROHIBITED until configured-test adjudication and F06E relocation approval. |
| `core/` | D — QUARANTINE | Legacy engine, kernel, composition, permission, recovery, and repository-state path. | Unreachable from `run_jaos.py`; reachable from legacy `main.py`. | Two configured direct importers (F06D1 quarantined `tests/tests/core/test_kernel.py`). | Owns `ActionHistory`, `SnapshotManager`, `BackupManager`, and `ConfigManager` writers. | F06D, F06E, and F06F. | PROHIBITED until test adjudication, writer isolation, launcher decision, and rollback evidence pass. |
| `dashboard/` | D — QUARANTINE | Top-level satellite interface stack using the legacy runtime-service bridge. | Unreachable from `run_jaos.py`. | One configured direct importer. | None in FORTRESS-02 inventory. | F06D and F06E. | PROHIBITED until configured-test adjudication and F06E relocation approval. |
| `development/` | D — QUARANTINE | Top-level development-service prototypes using the legacy runtime-service bridge. | Unreachable from `run_jaos.py`. | One configured direct importer. | None in FORTRESS-02 inventory. | F06D and F06E. | PROHIBITED until configured-test adjudication and F06E relocation approval. |
| `engineering/` | D — QUARANTINE | Top-level engineering-service prototypes using the legacy runtime-service bridge. | Unreachable from `run_jaos.py`. | One configured direct importer. | None in FORTRESS-02 inventory. | F06D and F06E. | PROHIBITED until configured-test adjudication and F06E relocation approval. |
| `executive_brain/` | D — QUARANTINE | Parallel Executive, planning, registry, Memory, AI-provider, and Tool authority. | Unreachable from `run_jaos.py`. | Thirty-one configured direct importers (F06D1 quarantined six AI duplicate tests; F06D2A archived the seven filesystem-tool tests; F06D2B archived the four Tool Platform core tests; F06D2C archived four monolithic Executive/pipeline tests). | The legacy file tool owns no internal runtime-state artifact; the F06D2C tests mutate in-memory state only. | F06D and F06E. | PROHIBITED until configured-test migration, caller inventory, relocation plan, and rollback evidence pass. |
| `infrastructure/` | D — QUARANTINE | Top-level provider and infrastructure-service prototypes using the legacy runtime-service bridge. | Unreachable from `run_jaos.py`. | One configured direct importer. | None in FORTRESS-02 inventory. | F06D and F06E. | PROHIBITED until configured-test adjudication and F06E relocation approval. |
| `kernel/` | D — QUARANTINE | Parallel boot, kernel, lifecycle, registry, permission, and runtime-context authorities. | Unreachable from `run_jaos.py`. | One configured direct importer. | None in FORTRESS-02 inventory. | F06D and F06E. | PROHIBITED until configured-test adjudication, caller inventory, and rollback evidence pass. |
| `knowledge/` | D — QUARANTINE | Top-level knowledge-service prototypes using the legacy runtime-service bridge. | Unreachable from `run_jaos.py`. | One configured direct importer. | None in FORTRESS-02 inventory. | F06D and F06E. | PROHIBITED until configured-test adjudication and F06E relocation approval. |
| `memory/` | D — QUARANTINE | Root legacy Memory implementation distinct from canonical `jaos.memory`. | Unreachable from `run_jaos.py`. | Zero configured direct importers; nine excluded flat-test importers. | Owns `LongTermMemory`, `MemoryCleanup`, and `MemoryExport` writers. | F06D, F06E, and F06F. | PROHIBITED until writer isolation, data-preservation proof, relocation plan, and rollback evidence pass. |
| `pc_control/` | D — QUARANTINE | Top-level application, browser, filesystem, terminal, and device-control prototypes. | Unreachable from `run_jaos.py`. | One configured direct importer. | None in FORTRESS-02 inventory. | F06D and F06E. | PROHIBITED until configured-test adjudication and F06E relocation approval. |
| `security/` | D — QUARANTINE | Parallel permission, authorization, identity, and audit prototypes; F07 policy is separate. | Unreachable from `run_jaos.py`. | One configured direct importer. | None in FORTRESS-02 inventory. | F06D and F06E. | PROHIBITED until configured-test adjudication and F06E relocation approval; no F07 policy work in F06. |
| `system_services/` | D — QUARANTINE | Top-level startup, backup, configuration, cache, and cleanup prototypes. | Unreachable from `run_jaos.py`. | One configured direct importer. | None in FORTRESS-02 inventory. | F06D and F06E. | PROHIBITED until configured-test adjudication and F06E relocation approval. |
| `workflow/` | D — QUARANTINE | Parallel workflow, task, dependency, retry, and automation authority. | Unreachable from `run_jaos.py`. | One configured direct importer. | None in FORTRESS-02 inventory. | F06D and F06E. | PROHIBITED until configured-test adjudication and F06E relocation approval. |
| `main.py` | D — QUARANTINE | Alternate launcher for `core.engine.JarvisEngine`; manually executable despite canonical non-reachability. | Not reachable from `run_jaos.py`; independently invokable. | No configured importer. | Indirectly reaches the `core` action-history, snapshot, and configuration writers. | F06E and F06F. | PROHIBITED until the legacy-launcher compatibility decision, writer isolation, and rollback evidence pass. |
| `legacy_quarantine/tests/phase14_integration_test.py.legacy` | E — ARCHIVE-ONLY | Byte-identical preservation of the historical root module-body script under a suffix that is neither Python-importable nor pytest-discoverable. | Unreachable from `run_jaos.py`; archived payload is not a normal Python module. | None; removed from supported pytest collection by F06B. | None in FORTRESS-02 inventory. | F06B preservation; F06E final disposition. | MOVE COMPLETE in F06B; deletion or further movement PROHIBITED until F06E approval. |
| `kernel/jaos_kernel_backup.py` | E — ARCHIVE-ONLY | Unreferenced executable backup of a shadow kernel; this file-specific archive classification refines but does not remove the root `kernel` quarantine prohibition. | Unreachable from `run_jaos.py`. | No configured importer. | None in FORTRESS-02 inventory. | F06E. | PROHIBITED until archive relocation and rollback evidence are separately approved. |
| `legacy_quarantine/tests/test_logger.py.legacy` | E — ARCHIVE-ONLY | Byte-identical preservation of the root smoke script under a suffix that is neither Python-importable nor pytest-discoverable. | Unreachable from `run_jaos.py`; archived payload is not a normal Python module. | None; removed from supported pytest collection by F06B. | None; `logs/system.log` has no legacy writer. | F06B preservation; F06E final disposition. | MOVE COMPLETE in F06B; deletion or further movement PROHIBITED until F06E approval. |
| `plugins/` | F — SAFE-TO-DELETE-LATER | One sample plugin with no known production or test caller; top-level plugins are not canonical. | Unreachable from `run_jaos.py`. | No configured importer. | None in FORTRESS-02 inventory. | F06E. | DELETION PROHIBITED until caller recheck and explicit removal authorization. |
| `infrastructure_intelligence_core.py` | F — SAFE-TO-DELETE-LATER | Unreferenced root duplicate of the packaged infrastructure component. | Unreachable from `run_jaos.py`. | No configured importer. | None in FORTRESS-02 inventory. | F06E. | DELETION PROHIBITED until caller recheck and explicit removal authorization. |
| `reasoning_assumption.py` | F — SAFE-TO-DELETE-LATER | Empty root module with no known caller; distinct from canonical `jaos.intelligence.models.reasoning_assumption`. | Unreachable from `run_jaos.py`. | No configured importer. | None in FORTRESS-02 inventory. | F06E. | DELETION PROHIBITED until caller recheck and explicit removal authorization. |
<!-- F06A-CLASSIFICATION-ENTRIES:END -->

Classification counts:

| Classification | Count |
|---|---:|
| A — CANONICAL | 10 |
| B — COMPATIBILITY DEBT | 1 |
| C — MIGRATION INPUT | 0 source entries |
| D — QUARANTINE | 16 |
| E — ARCHIVE-ONLY | 3 |
| F — SAFE-TO-DELETE-LATER | 3 |
| G — UNKNOWN — NEEDS DECISION | 0 source entries |
| Total classified source entries | 33 |

---

## 4. Canonical Import Guard Contract

The quarantine namespace is the top-level module identity
`legacy_quarantine`. F06A reserved and forbade that identity before any source
moved. F06B creates only `legacy_quarantine/tests/` for two non-Python archive
payloads; F06D1 adds `tests/ai/` and `tests/core/`, F06D2A adds
`tests/tools/filesystem/`, and F06D2B adds `tests/tools/core/`, for further
non-Python archive payloads. No
directory under `legacy_quarantine` contains `__init__.py`, and no file under it
has a recognized Python import suffix. Because the repository root is on
`sys.path`, the directory can still be represented by Python as a PEP 420
namespace; it is not a regular package and contains no importable payload.
The F06A guard therefore remains the production non-reachability authority and
continues to forbid canonical dependency on `legacy_quarantine`.

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

## 6. F06A Closure State

F06A is limited to this manifest, the existing canonical import-boundary
infrastructure, focused tests, and minimum current-state documentation.

- At the F06A checkpoint, no legacy source had moved or been deleted.
- No compatibility fallback has changed.
- No runtime-state writer or preserved artifact has changed.
- At the F06A checkpoint, F06B and later F06 slices had not started.
- RAA-003 remains OPEN.
- RAA-007 remains PARTIALLY RESOLVED.
- FORTRESS-07 has not started.
- Step 7 remains IN PROGRESS.
- Step 8 and Fortress certification remain blocked or not started.
- Major Phase 8 expansion remains paused.

F06A is IMPLEMENTED AND VERIFIED — COMMITTED AND PUSHED at checkpoint
`92aa9d7`. The focused import-boundary suite passed 55 tests; the platform
suite passed 363 tests with one skip; the affected composition suite passed 45 tests; and
the full configured `tests/tests` regression suite passed 2,037 tests with one
skip. The skip is the known Windows directory-symlink privilege limitation.
This evidence did not complete the FORTRESS-06 workstream.

---

## 7. F06B State and Stop Boundary

F06B addresses pytest collection and test-package identity only:

- Root collection previously imported `phase14_integration_test.py`, which
  loaded the root `brain` package before pytest attempted to collect
  `tests/tests/brain/test_executive_brain.py` as
  `brain.test_executive_brain`; prepend mode then failed collection.
- `phase14_integration_test.py` and `test_logger.py` were not supported tests.
  F06B preserves them byte-for-byte at the two archive paths recorded above.
- The canonical `pytest.ini` selects `--import-mode=importlib`; no second pytest
  configuration, path manipulation, module-cache manipulation, or broad ignore
  rule was introduced.
- The 428 direct `tests/*.py` legacy scripts remain contained by the existing
  `tests/conftest.py` authority and remain later F06 debt.
- No other legacy source moved or was deleted, and no runtime data migrated.
- At the F06B checkpoint, F06C and later F06 slices had not started.
- RAA-003 remains OPEN.
- RAA-007 remains PARTIALLY RESOLVED.
- FORTRESS-07 has not started.
- Step 7 remains IN PROGRESS.
- Step 8 and Fortress certification remain blocked or not started.
- Major Phase 8 expansion remains paused.

F06B is IMPLEMENTED AND VERIFIED — COMMITTED AND PUSHED at checkpoint
`eea8190`.
Verification completed with all commands at exit code 0:

- focused collection/import/composition invariants: 80 passed;
- platform suite: 364 passed, 1 skipped;
- composition suite: 45 passed;
- integration suite: 58 passed;
- full configured `tests/tests`: 2,038 passed, 1 skipped;
- configured, `tests/`, and repository-root collection: 2,039 collected each;
- Ruff on both changed Python test files: all checks passed.

The skip remains the known Windows directory-symlink privilege limitation. No
importlib semantic regression was observed. This evidence does not complete
FORTRESS-06, Step 7, or any certification gate.

---

## 8. F06C Current State and Stop Boundary

F06C is IMPLEMENTED AND VERIFIED — COMMITTED AND PUSHED at checkpoint
`0a2ea60`.
The verified implementation establishes the following behavior:

- `CommandDispatcher` requires injected `ToolManager`, `AIManager`, and
  `ExecutiveController` collaborators. It does not construct or lifecycle-own
  those platform objects.
- `JAOSShell` requires an injected dispatcher. It does not construct a
  dispatcher or shut down platform-owned collaborators.
- `PlatformComposition` remains the owner of Tool, AI, and Executive
  composition and teardown, and `JAOSApplication` remains the canonical
  launcher and lifecycle coordinator.
- Missing constructor collaborators fail at the constructor boundary instead
  of falling through to deferred attribute errors.
- A standalone compatibility factory is unnecessary because repository
  evidence identifies no supported production or configured-test caller that
  requires a second composition or lifecycle owner.
- Configured tests use explicit collaborators or canonical
  composition evidence. The 428 direct `tests/*.py` legacy scripts, including
  excluded `tests/test_cli_ai_integration.py`, remain untouched and contained
  by the existing `tests/conftest.py` authority.

All verification commands exited 0 under Python 3.14.6 and pytest 9.1.1 with
bytecode and pytest cache disabled and a unique external base temporary
directory for each pytest gate:

- focused run across all seven changed test files: 125 passed in 9.05 seconds;
- affected CLI, AI, composition, integration, and platform ladder: 583 passed,
  1 skipped in 30.46 seconds;
- disposable launcher/lifecycle normal-exit, EOF, dispatch-exception, and
  shell-exception checks: 4 passed in 1.03 seconds;
- full configured `tests/tests`: 2,047 passed, 1 skipped in 42.46 seconds;
- repository-root collection: 2,048 collected in 3.73 seconds; and
- Ruff 0.16.1 on changed Python files: all checks passed.

The one skip is independently confirmed at
`tests/tests/platform/test_runtime_paths.py:312`: Windows denied the required
directory-symlink privilege with `WinError 1314`.
This evidence resolves RAA-007 while preserving all other finding states:

- RAA-007 is RESOLVED WITH EVIDENCE.
- RAA-002 remains PARTIALLY RESOLVED.
- RAA-003 remains OPEN.
- RAA-009 remains OPEN — DEFERRED.

No legacy root or file moved, no runtime data migrated, and no permission,
approval, audit, provider-resilience, Conversation routing, or Memory-context
behavior changed in F06C. F06D and later F06 slices have not started.
FORTRESS-07 has not started. Step 7 remains IN PROGRESS. Step 8 remains
NOT STARTED — BLOCKED BY STEP 7, Fortress certification remains NOT STARTED,
and major Phase 8 expansion remains PAUSED.

---

## 9. F06D2A Current State and Stop Boundary

F06D2A is IMPLEMENTED AND VERIFIED — COMMITTED AND PUSHED at checkpoint
`95adce4`. It addresses configured filesystem-tool test authority only:

- Seven configured files carrying 56 legacy `executive_brain` filesystem-tool
  tests were adjudicated. Each legacy payload is preserved byte-identically at
  `legacy_quarantine/tests/tools/filesystem/<name>.py.legacy`, verified by
  SHA-256 equality against the pre-change configured file.
- The same seven configured paths now hold 100 canonical tests that import only
  `jaos.tools` and `jaos.tools.filesystem`. Because the configured paths survive
  with new content, Git records seven modifications plus seven additions rather
  than renames.
- Nine legacy requirements were intentionally not preserved: seven per-tool
  `TypeError` request-type guards that the canonical result model replaces with
  `ToolResult(success=False)`; the search "pattern is mandatory" requirement,
  which `SearchFileTool.DEFAULT_PATTERN` supersedes; and the legacy rename's
  ability to create a destination directory, which the canonical `new_name`
  containment rule deliberately forbids.
- No production code changed. Two production observations were recorded for a
  later authorized slice: only `DeleteFileTool` carries an approval policy, and
  `RenameFileTool`'s `..` rejection comes from its destination-exists check
  rather than its name-containment check.
- Configured legacy-importing test files reduce from 59 to 52, recomputed
  mechanically by AST inspection.
- `tests/tests/platform/test_collection_containment.py` gained two checks
  proving the seven archives are non-Python, non-importable, still carry the
  original `executive_brain` source, and that the seven configured replacements
  import `jaos` and no legacy root. No second quarantine-test framework was
  created, and `legacy_quarantine` still contains no `__init__.py`.
- The remaining 19 legacy `tests/tests/tools` files and the 428 direct
  `tests/*.py` legacy scripts are untouched and remain later F06 debt.

Verified F06D2A evidence, all exit code 0 under Python 3.14.6 and pytest 9.1.1
with `PYTHONDONTWRITEBYTECODE=1`, `-B`, `-p no:cacheprovider`, and a unique
external `--basetemp` per gate:

- focused filesystem tests: 100 passed;
- focused filesystem plus containment and import boundary: 171 passed;
- tools suite: 226 passed;
- platform suite: 367 passed, 1 skipped;
- composition suite: 49 passed;
- integration suite: 64 passed;
- full configured `tests/tests`: 2,044 passed, 1 skipped;
- configured, `tests/`, and repository-root collection: 2,045 collected each;
- Ruff 0.16.1 `check` on all eight changed Python files: all checks passed.

The one skip remains the Windows directory-symlink privilege limitation at
`tests/tests/platform/test_runtime_paths.py:312` (`WinError 1314`).

F06D2A does not complete F06D. RAA-003 remains OPEN, RAA-007 remains RESOLVED
WITH EVIDENCE, FORTRESS-07 has not started, Step 7 remains IN PROGRESS, Step 8
remains NOT STARTED — BLOCKED BY STEP 7, Fortress certification remains NOT
STARTED, and major Phase 8 expansion remains PAUSED.


---

## 10. F06D2B Current State and Stop Boundary

F06D2B is IMPLEMENTED AND VERIFIED. It addresses configured Tool Platform core
test authority only:

- Four configured files carrying 25 legacy `executive_brain.tools.core` tests
  were adjudicated. The 4-file / 25-test baseline was reconciled mechanically by
  AST inspection before any edit. Each legacy payload is preserved
  byte-identically at `legacy_quarantine/tests/tools/core/<name>.py.legacy`,
  verified by SHA-256 and Git blob equality against the pre-change configured
  file.

| Archived payload | SHA-256 | Git blob |
|---|---|---|
| `test_tool_interface.py.legacy` | `c201731050a6afb19a964a873abb7710a3a244758f3fa04564cfabe3a0bba361` | `3ec3b28c9eeaa0dfe2fa6cda5beca99074861f87` |
| `test_tool_manager.py.legacy` | `f7757e71404660ccc5b256ebfc426fb950702f7485cb5d8162ebad0c47461a47` | `bfd477787547cc9edfc6410af13f4066441fc7f7` |
| `test_tool_models.py.legacy` | `7a5472ee250a0e896e7e11c7027e877be07e027db4c98c9c0bd82192740a76a3` | `e93aecbb44893bffb8ca14afe24568f1caa9a9ab` |
| `test_tool_registry.py.legacy` | `eff479fa3cdab6a3162067f0091e94f86e5ba5615aa194cc123e6e095d057589` | `08bc593865dc35fefaea69a3ad4c35c28d168d37` |

- The same four configured paths now hold 19 canonical tests that import only
  `jaos.tools`. Because the configured paths survive with new content, Git
  records four modifications plus four additions rather than renames.
- Ten legacy requirements were intentionally not preserved: the legacy
  `ToolStatus.SUCCESS`/`FAILURE` value assertions, whose concept moved to
  `ToolResult.success`; the `ToolManager.registry` accessor, whose preservation
  would have documented an escape hatch around the canonical permission,
  approval, and audit chain; two runtime `TypeError` input guards that canonical
  ABC typing replaces; four registry and manager deregistration or bulk-clear
  requirements with no canonical owner; and `count()`, which survives as the
  length of `list_tools()`.
- No production code changed. Three observations were recorded for a later
  authorized slice: `ToolRegistry.register` and `ToolManager.execute` raise
  `AttributeError` rather than typed errors for non-tool and non-request input;
  canonical tool deregistration and registry reset have no owner; and the frozen
  canonical Tool Platform models have no configured immutability assertion.
  None of these is a permission, approval, or audit policy gap, so none belongs
  to FORTRESS-07.
- Configured legacy-importing test files reduce from 52 to 48 and configured
  `executive_brain` importers from 39 to 35, both recomputed mechanically by AST
  inspection.
- `tests/tests/platform/test_collection_containment.py` gained three checks
  proving the four archives are non-Python, non-importable, and still carry the
  original `executive_brain.tools.core` source; that the four configured
  replacements import `jaos` and no legacy root; and that no configured test at
  the four adjudicated paths imports `executive_brain.tools.core`, with the
  sixteen remaining configured importers pinned by name as F06D2E
  prototype-tool test debt.
  No second quarantine-test framework was created, and `legacy_quarantine` still
  contains no `__init__.py`.
- The sixteen remaining legacy `tests/tests/tools` files and the 428 direct
  `tests/*.py` legacy scripts are untouched and remain later F06 debt.

Verified F06D2B evidence, all exit code 0 under Python 3.14.6 and pytest 9.1.1
with `PYTHONDONTWRITEBYTECODE=1`, `-B`, `-p no:cacheprovider`, and a unique
external `--basetemp` per gate:

- focused Tool Platform tests: 19 passed;
- containment and canonical import boundary: 74 passed;
- tools suite: 220 passed;
- platform suite: 370 passed, 1 skipped;
- composition suite: 49 passed;
- integration suite: 64 passed;
- full configured `tests/tests`: 2,041 passed, 1 skipped;
- configured, `tests/`, and repository-root collection: 2,042 collected each;
- Ruff 0.16.1 `check` on all five changed Python files: all checks passed.

The one skip remains the Windows directory-symlink privilege limitation at
`tests/tests/platform/test_runtime_paths.py:312` (`WinError 1314`).

F06D2B does not complete F06D. RAA-003 remains OPEN, RAA-007 remains RESOLVED
WITH EVIDENCE, F06D2C and later slices have not started, FORTRESS-07 has not
started, Step 7 remains IN PROGRESS, Step 8 remains NOT STARTED — BLOCKED BY
STEP 7, Fortress certification remains NOT STARTED, and major Phase 8 expansion
remains PAUSED.

---

## 11. F06D2C Current State and Stop Boundary

FORTRESS-06D2C — IMPLEMENTED AND VERIFIED.
It retires only the four Founder-authorized monolithic ExecutiveBrain and
executive-pipeline configured files. The 4-file / 22-source-test baseline was
reconciled mechanically before any edit:

| Retired configured file | Source tests | Non-Python archive |
|---|---:|---|
| `tests/tests/brain/test_executive_brain.py` | 9 | `legacy_quarantine/tests/executive/brain/test_executive_brain.py.legacy` |
| `tests/tests/integration/test_executive_pipeline.py` | 5 | `legacy_quarantine/tests/executive/pipeline/test_executive_pipeline.py.legacy` |
| `tests/tests/integration/test_executive_pipeline_v2.py` | 4 | `legacy_quarantine/tests/executive/pipeline/test_executive_pipeline_v2.py.legacy` |
| `tests/tests/integration/test_executive_runtime.py` | 4 | `legacy_quarantine/tests/executive/runtime/test_executive_runtime.py.legacy` |
| Total | 22 | 4 archives |

Each payload was copied before its configured source was retired and verified
byte-identical by both SHA-256 and Git blob identity:

| Archived payload | SHA-256 | Git blob |
|---|---|---|
| `test_executive_brain.py.legacy` | `d422566f036ba637241e03f66f75aa80238aead422a30b54fd18d900126060cb` | `567f49e9b5e9bea8bef14bb8f518906025f553c7` |
| `test_executive_pipeline.py.legacy` | `8be05bbee311ec57f528cb6fe3da2120a54e66f70a8ba5f7949ec59cc5aebe8c` | `49f54713dc47419abbe7a9132e2312ab7e6276f3` |
| `test_executive_pipeline_v2.py.legacy` | `31430e092c95a4b48e0c1a05a03ecce6a30b58ce008a7adb8b04efc442016e23` | `5cecb19fcad192c4bcf67d6d1f1c337b2ea83b3a` |
| `test_executive_runtime.py.legacy` | `945a3d4104883f62382a79f6a9c311f6102cfad67fa864c315e4e09c509558b7` | `1be134b533b051be672fb13ccc05b6a46849a9a1` |

`tests/tests/executive/test_canonical_executive_controller.py` adds exactly two
canonical source tests:

- a real deterministic read request traverses `ExecutiveController.process`,
  `ExecutionCoordinator`, `ToolManager`, and canonical `ReadFileTool`, returning
  a truthful `ExecutiveResponse` whose output matches the test-owned file and
  whose Tool audit record reports the actual successful execution; and
- empty and whitespace-only inputs return the existing controlled canonical
  failure, do not claim success, invoke no `ToolManager.execute`, execute no
  tool, and create no audit record. The legacy `ValueError` contract is not
  preserved.

The following shadow requirements were intentionally not ported: monolithic
ExecutiveBrain initialization/readiness; ownership of RegistryManager,
MemoryManager, and hard-coded managers/registries; legacy WorkingMemory layout;
mission/decision/result identifiers and counts; automatic approval; the
`executive_brain` service key and `executive_brain_status`; literal
`PIPELINE_EXECUTED`; and hard-coded WorkflowEngine readiness.

The existing containment authority gained three checks proving that the four
configured paths are absent, the four archives are non-Python,
non-importable, and non-collectable, the canonical replacement imports only
canonical JAOS plus standard test dependencies, and the adjacent
`test_memory_runtime_integration.py` remains executable and deferred. The
existing F06D2E guard continues to pin all sixteen prototype browser, Windows,
and development `executive_brain.tools.core` importers by name. No second
quarantine framework or `legacy_quarantine/__init__.py` was created.

AST inspection of every configured test file against the F06 guarded roots
recomputed the exact progression:

- configured legacy-facing files: 48 -> 44;
- configured `executive_brain` importers: 35 -> 31; and
- configured `executive_brain.tools.core` prototype importers: 16 unchanged,
  owned by F06D2E.

The earlier F06D writer observation is corrected for these four files. Their
execution mutates only legacy in-memory registries, WorkingMemory fields,
ServiceContainer entries, RuntimeContext keys, and transient EventBus state.
It calls no persistent runtime-state writer, no file API, and no runtime
logging configuration, so these are not repository-data writer tests. The
FORTRESS-02 protected-state guard remains defense in depth; no protected JSON
artifact was changed or migrated.

Verified F06D2C evidence, all recorded successful gates exit code 0 under
Python 3.14.6, pytest 9.1.1, `PYTHONDONTWRITEBYTECODE=1`, `-B`,
`-p no:cacheprovider`, and a unique external `--basetemp` per gate:

| Gate | Result |
|---|---|
| Canonical ExecutiveController | 3 passed from 2 source tests |
| Focused Executive/Tool/composition/lifecycle/containment/import boundary | 122 passed |
| Containment and canonical import boundary | 77 passed |
| Executive suite | 6 passed |
| Tools suite | 220 passed |
| Composition suite | 49 passed |
| Platform suite | 373 passed, 1 skipped |
| Integration suite | 51 passed |
| Full configured `tests/tests` | 2,025 passed, 1 skipped |
| Repository-root collection | 2,026 collected |
| Ruff 0.16.1 on both changed Python files | All checks passed |

Python 3.14's Windows `0o700` ACL handling denied pytest access to its own
basetemp under the managed sandbox. Test commands therefore loaded a temporary,
Windows-only runner shim that changed only pytest's basetemp directory mode to
inherit the parent ACL. It did not change JAOS code, fixtures, test behavior, or
the final repository diff and was removed after verification. The one skip
remains the Windows directory-symlink privilege limitation at
`tests/tests/platform/test_runtime_paths.py:312` (`WinError 1314`).

F07 continues to own permission, approval, audit, and risk policy; F08 durable
mission/decision/result persistence and recovery/replay; F09 provider
resilience; F10 aggregate health/degradation/readiness semantics; F11
abuse/security/chaos/CI; and resumed Phase 8 intelligence routing,
conversation-memory context, multi-turn continuity, and expanded
reasoning/planning. None was implemented in F06D2C.

F06D2C does not complete F06D or FORTRESS-06. RAA-003 remains OPEN, RAA-007
remains RESOLVED WITH EVIDENCE, F06D2D+ and FORTRESS-07 remain NOT STARTED,
Step 7 remains IN PROGRESS, Step 8 remains NOT STARTED — BLOCKED BY STEP 7,
Fortress certification remains NOT STARTED, and major Phase 8 expansion remains
PAUSED. F06D2C is IMPLEMENTED AND VERIFIED.

---

## 12. Update History

| Date | Version | Change |
|---|---|---|
| 2026-08-30 | 1.7 | Recorded F06D2C's exact 4-file / 22-source-test ExecutiveBrain and pipeline retirement, four byte/blob-identical `.py.legacy` archives, two canonical source tests, three containment checks, corrected in-memory writer finding, 48 -> 44 legacy-facing reduction, and 35 -> 31 `executive_brain` importer reduction. Full configured suite 2,025 passed, 1 skipped; repository-root collection found 2,026 tests; Ruff passed. F06D2C is IMPLEMENTED AND VERIFIED; F06D and FORTRESS-06 remain in progress. |
| 2026-08-30 | 1.6 | Recorded F06D2B's four-file Tool Platform core test adjudication, byte-identical archives under `legacy_quarantine/tests/tools/core/` with SHA-256 and Git blob evidence, 19 canonical `jaos.tools` replacement tests, 10 dropped legacy requirements, 3 recorded non-FORTRESS-07 observations, and the 52 -> 48 legacy-facing reduction (39 -> 35 `executive_brain` importers). Synchronized F06D2A to its committed checkpoint `95adce4`. FORTRESS-06 remains in progress, F06D is not complete, and F06D2C+ remains not started. |
| 2026-08-25 | 1.5 | Recorded F06D2A's seven-file filesystem-tool test migration, byte-identical archives, 59 -> 52 legacy-facing reduction, and verification evidence; synchronized F06D1 to its committed checkpoint `51818d2`. FORTRESS-06 remains in progress, F06D is not complete, and F06D2B+ remains not started. |
| 2026-08-25 | 1.3 | Synchronized F06C current-state wording with committed and pushed checkpoint `0a2ea60`; FORTRESS-06 remains in progress, F06D+ remains not started, and certification gates remain unchanged. |
| 2026-08-25 | 1.2 | Recorded F06C's verified injected CLI adapters, canonical lifecycle ownership, exact verification evidence, and RAA-007 resolution. FORTRESS-06 remains in progress and F06D+ remains not started. |
| 2026-08-25 | 1.1 | Recorded F06B's exact two-artifact non-Python archive move, importlib pytest configuration, collection-collision remediation, and unchanged stop boundary. |
| 2026-08-25 | 1.0 | Created the authoritative F06 classification and canonical import-guard contract. No legacy source or runtime data moved. |
