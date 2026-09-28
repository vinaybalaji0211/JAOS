# FORTRESS-06 Legacy and Quarantine Manifest

Document ID: ARCH-FORTRESS-06

Document Version: 1.27

Certified Repository Baseline: v0.9.0-alpha

Development Target: v0.10.0-alpha

Status: In Progress — F06D1, F06D2A, F06D2B, and F06D2C committed and pushed;
F06D2D IMPLEMENTED AND VERIFIED; F06D2E IMPLEMENTED AND VERIFIED;
FORTRESS-06D Memory retirement — IMPLEMENTED AND VERIFIED under ADR-0013;
provider retirement — IMPLEMENTED AND VERIFIED under ADR-0014;
satellite/runtime shadow-test retirement — IMPLEMENTED AND VERIFIED;
core/kernel shadow-runtime test retirement — IMPLEMENTED AND VERIFIED;
FORTRESS-06E communication production-root quarantine pilot — IMPLEMENTED AND
VERIFIED; development/infrastructure/pc_control production quarantine —
IMPLEMENTED AND VERIFIED; dashboard/knowledge/security/system_services
production quarantine — IMPLEMENTED AND VERIFIED; engineering production-root
quarantine — IMPLEMENTED AND VERIFIED; kernel production-root quarantine —
IMPLEMENTED AND VERIFIED; core/kernel.py production-leaf quarantine —
IMPLEMENTED AND VERIFIED; executive_brain AI/provider production-family
quarantine — IMPLEMENTED AND VERIFIED; executive_brain tools production-family
quarantine — IMPLEMENTED AND VERIFIED; final remaining executive_brain
production-family quarantine — IMPLEMENTED AND VERIFIED; workflow production-family
quarantine — IMPLEMENTED AND VERIFIED; partial core production quarantine —
IMPLEMENTED AND VERIFIED

Owner and Approval Authority: Founder Vinay B

Maintainer: JAOS Engineering

Last Updated: 2026-09-28

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
F06D2C is committed and pushed at checkpoint `1862f78`.

ADR-0012 clarifies that older Phase 8 manager and registry names identify
logical responsibilities and historical integration boundaries, not canonical
runtime authority for the exact `executive_brain.managers.*` or
`executive_brain.registries.*` implementations. F06D2D added configured
aggregate `ExecutiveController` metrics coverage before retiring nine configured
manager/registry files carrying 94 source tests into byte-identical non-Python
archives. Configured legacy-facing files are now 35 and configured
`executive_brain` importers are 22. FORTRESS-06D2D — IMPLEMENTED AND VERIFIED.

ADR-0014 records the Founder-approved disposition for the final two configured
`executive_brain` provider importers. Their 20 collected source tests exercise
unreachable, offline/mock-based shadow OpenAI and Ollama adapters. Both files
were retired only after exactly three provider-neutral canonical invariants
received configured evidence. At that provider-retirement checkpoint, counts
were 13 configured legacy-facing files and zero configured `executive_brain`
importers. Provider retirement is IMPLEMENTED AND VERIFIED.

The ten configured satellite/runtime integration tests carrying 30 source and
collected cases are now preserved as exact non-Python archives under
`legacy_quarantine/tests/integration/`. No capability behavior was ported and
no production source changed. At that satellite-retirement checkpoint, counts
were three configured legacy-facing files and zero configured
`executive_brain` importers.
FORTRESS-06D satellite/runtime shadow-test retirement is IMPLEMENTED AND
VERIFIED.

The two configured core/kernel runtime integration tests carrying six source
and collected cases are now preserved as exact non-Python archives under
`legacy_quarantine/tests/platform/`. No canonical behavior was ported and no
production source changed. Current counts are one configured legacy-facing
file and zero configured `executive_brain` importers. The intentionally
retained file is `tests/tests/platform/test_config_containment.py` with nine
source definitions and eleven collected cases. FORTRESS-06D core/kernel
shadow-runtime test retirement is IMPLEMENTED AND VERIFIED.

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
| `legacy_quarantine/production/communication/*.py.legacy` | E — ARCHIVE-ONLY | Six byte/blob-identical non-Python archives of the former top-level communication satellite stack. | Unreachable from `run_jaos.py`; the live `communication/` root is absent. | Zero configured direct importers; seven excluded flat historical tests retain stale imports as F06G/F06H debt. | None. | F06E preservation; F06G/F06H excluded-test disposition. | MOVE COMPLETE in the F06E pilot; deletion or import from quarantine is PROHIBITED. |
| `core/` | D — QUARANTINE | PARTIAL ROOT DISPOSITION: prior kernel leaf (section 25) plus 18 approved sources (section 30) archived; exactly 16 sources remain live. | Retained root is unreachable from run_jaos.py and reachable from legacy main.py; zero supported callers into retired subset. | One configured direct importer remains: tests/tests/platform/test_config_containment.py; excluded flat debt and earlier archives preserved. | ActionHistory, SnapshotManager, BackupManager and ConfigManager remain live unchanged; no F06F writer or responsibility moved. | F06D, F06E and later F06F/F06G launcher disposition. | Partial move COMPLETE; core remains D; no separate E entry. Remaining-root movement PROHIBITED pending writer isolation, launcher decision and rollback evidence. |
| `legacy_quarantine/production/dashboard/*.py.legacy` | E — ARCHIVE-ONLY | 7 byte/SHA/blob-identical non-Python archives of the former dashboard production root. | Unreachable from `run_jaos.py`; the live root is absent. | Zero configured direct importers; 7 / 12 excluded files / direct statements and 1 excluded-only dynamic registration remain F06G/F06H debt. | None; low-risk in-memory disposition confirmed. | F06E preservation; F06G/F06H excluded debt. | MOVE COMPLETE; deletion or import from quarantine is PROHIBITED. |
| `legacy_quarantine/production/development/*.py.legacy` | E — ARCHIVE-ONLY | 7 byte/blob-identical non-Python archives of the former development production root. | Unreachable from `run_jaos.py`; the live root is absent. | Zero configured direct importers; 7 / 12 excluded flat files / direct import statements remain F06G/F06H debt. | None; low-risk in-memory disposition confirmed. | F06E preservation; F06G/F06H excluded-test disposition. | MOVE COMPLETE; deletion or import from quarantine is PROHIBITED. |
| `legacy_quarantine/production/engineering/` | E — ARCHIVE-ONLY | 13 Python-source archives and one historical Markdown archive preserve exact checkout bytes/SHA/size and Git-normalized blobs. | Unreachable from `run_jaos.py`; live engineering root absent; no active production or CLI caller. | Zero configured importers; 13 excluded files / 24 direct imports, five registrations, and stale directory validation remain F06G/F06H debt. | No active F06F writer authority; explicit import execution adjudicated excluded-test-only. | F06E preservation; F06G/F06H excluded debt. | MOVE COMPLETE; deletion or import from quarantine is PROHIBITED. |
| `legacy_quarantine/production/executive_brain/` | E — ARCHIVE-ONLY | Complete Executive root history: 13 AI/provider + 42 tools + 36 final sources = 91 byte/SHA/blob-identical inert archives. ADR-0012, ADR-0013, and ADR-0014 dispositions preserved; no shadow replacement. | Live root absent; canonical and other live production importers zero. | Zero configured importers; final-family debt is 17 quarantined files / 47 edges and 12 excluded flat files / 21 edges, unchanged and inert. | Final 36 own only transient state and lifecycle/context/event interactions; no F06F protected-writer split required. | F06E preservation; future responsibilities remain separately governed. | MOVE COMPLETE; archive fidelity and caller authority containment verified; full regression evidence recorded in section 28. Deletion or import from quarantine PROHIBITED. |
| `legacy_quarantine/production/infrastructure/*.py.legacy` | E — ARCHIVE-ONLY | 9 byte/blob-identical non-Python archives of the former infrastructure production root. | Unreachable from `run_jaos.py`; the live root is absent. | Zero configured direct importers; 9 / 16 excluded flat files / direct import statements remain F06G/F06H debt. | None; low-risk in-memory disposition confirmed. | F06E preservation; F06G/F06H excluded-test disposition. | MOVE COMPLETE; deletion or import from quarantine is PROHIBITED. |
| `legacy_quarantine/production/kernel/` | E — ARCHIVE-ONLY | Twelve exact non-Python archives preserve the former shadow boot, lifecycle, context, permission, and service stack. | Live kernel root absent; zero canonical or remaining legacy production callers. | Zero configured importers; 11 excluded files / 18 direct imports remain F06G/F06H debt. | No kernel-owned persistent runtime/config/data writer. | F06E preservation; F06G/F06H excluded debt. | MOVE COMPLETE; deletion or import from quarantine is PROHIBITED. |
| `legacy_quarantine/production/knowledge/*.py.legacy` | E — ARCHIVE-ONLY | 7 byte/SHA/blob-identical non-Python archives of the former knowledge production root. | Unreachable from `run_jaos.py`; the live root is absent. | Zero configured direct importers; 7 / 12 excluded files / direct statements and 1 excluded-only dynamic registration remain F06G/F06H debt. | None; low-risk in-memory disposition confirmed. | F06E preservation; F06G/F06H excluded debt. | MOVE COMPLETE; deletion or import from quarantine is PROHIBITED. |
| `memory/` | D — QUARANTINE | Root legacy Memory implementation distinct from canonical `jaos.memory`. | Unreachable from `run_jaos.py`. | Zero configured direct importers; nine excluded flat-test importers. | Owns `LongTermMemory`, `MemoryCleanup`, and `MemoryExport` writers. | F06D, F06E, and F06F. | PROHIBITED until writer isolation, data-preservation proof, relocation plan, and rollback evidence pass. |
| `legacy_quarantine/production/pc_control/*.py.legacy` | E — ARCHIVE-ONLY | 8 byte/blob-identical non-Python archives of the former pc_control production root. | Unreachable from `run_jaos.py`; the live root is absent. | Zero configured direct importers; 8 / 14 excluded flat files / direct import statements remain F06G/F06H debt. | None; low-risk in-memory disposition confirmed. | F06E preservation; F06G/F06H excluded-test disposition. | MOVE COMPLETE; deletion or import from quarantine is PROHIBITED. |
| `legacy_quarantine/production/security/*.py.legacy` | E — ARCHIVE-ONLY | 7 byte/SHA/blob-identical non-Python archives of the former security production root; F07 policy remains separate. | Unreachable from `run_jaos.py`; the live root is absent. | Zero configured direct importers; 7 / 12 excluded files / direct statements and 2 excluded-only dynamic registrations remain F06G/F06H debt. | None; low-risk in-memory disposition confirmed. | F06E preservation; F06G/F06H excluded debt. | MOVE COMPLETE; deletion or import from quarantine is PROHIBITED. |
| `legacy_quarantine/production/system_services/*.py.legacy` | E — ARCHIVE-ONLY | 8 byte/SHA/blob-identical non-Python archives of the former system_services production root. | Unreachable from `run_jaos.py`; the live root is absent. | Zero configured direct importers; 8 / 14 excluded files / direct statements and 1 excluded-only dynamic registration remain F06G/F06H debt. | None; low-risk in-memory disposition confirmed. | F06E preservation; F06G/F06H excluded debt. | MOVE COMPLETE; deletion or import from quarantine is PROHIBITED. |
| `legacy_quarantine/production/workflow/` | E — ARCHIVE-ONLY | Nine former workflow sources relocated as inert `.py.legacy` archives; no replacement behavior. | No live workflow source or namespace. | Excluded demo scripts and archived runtime test remain historical debt. | None; F06F writers remain outside workflow. | F06E; compatibility disposition remains F06G. | MOVE COMPLETE; regression verified. Deletion or import from quarantine remains prohibited. |
| `main.py` | D — QUARANTINE | Alternate launcher for `core.engine.JarvisEngine`; manually executable despite canonical non-reachability. | Not reachable from `run_jaos.py`; independently invokable. | No configured importer. | Indirectly reaches the `core` action-history, snapshot, and configuration writers. | F06E and F06F. | PROHIBITED until the legacy-launcher compatibility decision, writer isolation, and rollback evidence pass. |
| `legacy_quarantine/tests/phase14_integration_test.py.legacy` | E — ARCHIVE-ONLY | Byte-identical preservation of the historical root module-body script under a suffix that is neither Python-importable nor pytest-discoverable. | Unreachable from `run_jaos.py`; archived payload is not a normal Python module. | None; removed from supported pytest collection by F06B. | None in FORTRESS-02 inventory. | F06B preservation; F06E final disposition. | MOVE COMPLETE in F06B; deletion or further movement PROHIBITED until F06E approval. |
| `legacy_quarantine/production/kernel/jaos_kernel_backup.py.legacy` | E — ARCHIVE-ONLY | Exact archive of the previously separate shadow-kernel backup classification; this file-specific refinement remains represented within the archived kernel root. | Live source absent; unreachable from canonical production. | No configured importer. | None in FORTRESS-02 inventory. | F06E preservation. | MOVE COMPLETE; deletion or import from quarantine is PROHIBITED. |
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
| D — QUARANTINE | 4 |
| E — ARCHIVE-ONLY | 15 |
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
non-Python archive payloads. The F06E communication pilot adds
`legacy_quarantine/production/communication/` for six exact non-Python
production-source archives. Subsequent F06E slices add 24 exact archives for
development/infrastructure/pc_control and 29 for
dashboard/knowledge/security/system_services (59 production archives total).
No directory under `legacy_quarantine` contains `__init__.py`, and no file under it
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

F06D2C does not complete F06D or FORTRESS-06. At the F06D2C checkpoint,
RAA-003 remained OPEN, RAA-007 remained RESOLVED WITH EVIDENCE, and F06D2D was
ADJUDICATED with its governance decision approved but implementation NOT
STARTED. F06D2E+ and FORTRESS-07 remained NOT STARTED, Step 7 remained IN
PROGRESS, Step 8 remained NOT STARTED — BLOCKED BY STEP 7, Fortress
certification remained NOT STARTED, and major Phase 8 expansion remained
PAUSED. F06D2C is IMPLEMENTED AND VERIFIED.

---

## 12. F06D2D Current State and Stop Boundary

ADR-0012 remains authoritative. Older Phase 8 references to ExecutiveBrain,
Manager Layer, MissionManager, PlanningManager, DecisionManager,
ExecutionManager, ResultManager, RegistryManager, and Registry Layer are
responsibility labels and historical integration boundaries. They do not
preserve the exact `executive_brain.managers.*` or
`executive_brain.registries.*` implementations as canonical runtime
authorities.

FORTRESS-06D2D — IMPLEMENTED AND VERIFIED. The exact 9-file /
94-source-test baseline was reconciled before edits and retired as follows:

| Retired configured file | Source tests | Non-Python archive |
|---|---:|---|
| `tests/tests/manager_layer/test_decision_manager.py` | 10 | `legacy_quarantine/tests/executive/managers/test_decision_manager.py.legacy` |
| `tests/tests/manager_layer/test_execution_manager.py` | 9 | `legacy_quarantine/tests/executive/managers/test_execution_manager.py.legacy` |
| `tests/tests/manager_layer/test_mission_manager.py` | 14 | `legacy_quarantine/tests/executive/managers/test_mission_manager.py.legacy` |
| `tests/tests/manager_layer/test_planning_manager.py` | 8 | `legacy_quarantine/tests/executive/managers/test_planning_manager.py.legacy` |
| `tests/tests/manager_layer/test_registry_manager.py` | 7 | `legacy_quarantine/tests/executive/managers/test_registry_manager.py.legacy` |
| `tests/tests/manager_layer/test_result_manager.py` | 9 | `legacy_quarantine/tests/executive/managers/test_result_manager.py.legacy` |
| `tests/tests/registry_layer/test_execution_plan_registry.py` | 13 | `legacy_quarantine/tests/executive/registries/test_execution_plan_registry.py.legacy` |
| `tests/tests/registry_layer/test_mission_registry.py` | 12 | `legacy_quarantine/tests/executive/registries/test_mission_registry.py.legacy` |
| `tests/tests/registry_layer/test_result_registry.py` | 12 | `legacy_quarantine/tests/executive/registries/test_result_registry.py.legacy` |
| Total | 94 | 9 archives |

Each archive matches its former configured source by both SHA-256 and Git blob
identity:

| Archived payload | SHA-256 | Git blob |
|---|---|---|
| `test_decision_manager.py.legacy` | `ba1b17667115e75129ed8b5c27a24a433b96d71991ddcd7ea6c763588cef4e5a` | `ee75451c16fb1ac5dc9beccf8c1c3c0a0711988f` |
| `test_execution_manager.py.legacy` | `229639f71adbcb519c62fc1fee8c7f4b708169d469115f61fdd45971c1d88997` | `c61701d450617ba7999af843780603be0275cc0f` |
| `test_mission_manager.py.legacy` | `60b4d90e80ca2750109fcfae23e1c42b960302ee0fb6dd9eeccc9640af193b88` | `5a759d50b3c8e4457ae01197e535b15eddcbb69b` |
| `test_planning_manager.py.legacy` | `a56b590b241de2aec25b1bfa3c6c1f513ccd91e3d134cd963a5d0054adbea516` | `19ddc0016f4128aa274df271e48cc1ff16b93fc4` |
| `test_registry_manager.py.legacy` | `473bd4914180c0be406bb69a319183c5759149ec75b1cf8614e44390419eadcd` | `e15df860b2765e7703b39be9adea1bc4e218ca17` |
| `test_result_manager.py.legacy` | `15c84c43aadbecc91a0e8f82cd8e300510c9ad5c7909b5b973f06e16ec52e628` | `f9e662fc1992f1936555d1d5cb537bb93de87f4c` |
| `test_execution_plan_registry.py.legacy` | `6174dd08b9ad419684b4994f0bc2ebe2053892cad804959bd8916efbb647a111` | `9b095bae9ca7c3416b0fe576b07b91c2247dbabc` |
| `test_mission_registry.py.legacy` | `e91aadb273f1175d424ad4e4a5a70e4c39aebfc1256931bba4677a2803c6b0e6` | `11603bf56e628a3726328472f92914a485038ce2` |
| `test_result_registry.py.legacy` | `ae977136dcd578136ba074d9bd741d6c69f1fbd710e103aa382508be0440ea7e` | `dc41a75bc99ab64431aac219235f301fe107e79a` |

Every archive ends in `.py.legacy`, remains outside Python import and pytest
collection suffixes, and no `__init__.py` exists under `legacy_quarantine/`.

Before retirement, the configured canonical Executive suite added
`test_execution_metrics_record_truthful_real_tool_outcomes`. It executes one
successful and one missing-file request through `ExecutiveController`,
`ExecutionCoordinator`, `ToolManager`, and real `ReadFileTool`, then verifies
the existing aggregate metrics contract: 2 executed, 1 succeeded, 1 failed,
1 last-plan step, and 0.5 success rate. No production code changed.

Literal manager readiness and health states, generic RegistryManager ownership,
hard-coded registry graphs/counts, automatic approval/confidence, simulated
execution success, fabricated results, legacy IDs and lookup exceptions,
persistence assumptions, direct platform/service binding, and global
cross-registry authority were intentionally not ported.

The existing containment authority now verifies the nine absent configured
paths, nine pinned byte-identical non-Python archives, canonical-only Executive
test imports, and the exact remaining configured `executive_brain` inventory:
16 F06D2E prototype-tool importers, 4 deferred Memory importers, and 2 deferred
provider importers. Those 22 out-of-scope files remain unchanged.

AST inspection mechanically verified the achieved count changes:

- configured legacy-facing files: 44 -> 35;
- configured `executive_brain` importers: 31 -> 22;
- F06D2E prototype-tool importers: 16 unchanged;
- deferred Memory importers: 4 unchanged; and
- deferred provider importers: 2 unchanged.

The retired manager/registry implementations and tests use in-memory registry
dictionaries. They execute no persistent repository runtime-state writer.
F06D2D performed no runtime-data migration and changed no protected JSON file.

Verified F06D2D evidence, all recorded successful gates exit code 0:

| Gate | Result |
|---|---|
| Canonical aggregate Executive metrics prerequisite | 1 passed |
| Canonical ExecutiveController and containment | 28 passed |
| Focused Executive/metrics/containment/import/status/ToolManager | 90 passed |
| Executive suite | 7 passed |
| Tools suite | 220 passed |
| Composition suite | 49 passed |
| Platform suite | 375 passed, 1 skipped |
| Integration suite | 51 passed |
| Combined subsystem suites | 702 passed, 1 skipped |
| Full configured `tests/tests` | 1,934 passed, 1 skipped |
| Repository-root collection | 1,935 collected |
| Ruff on both changed Python files | All checks passed |

The successful pytest gates used repository Python,
`PYTHONDONTWRITEBYTECODE=1`, `-B`, `-p no:cacheprovider`, unique external
`--basetemp` paths, and the established Windows ACL runner shim. An initial
direct metrics invocation exited 1 before test execution because pytest's
Python 3.14 `0o700` basetemp ACL denied access. The shim changed only temporary
directory inheritance and no repository file or test behavior. The one skip is
the known Windows directory-symlink privilege limitation.

Future logical mission, planning, decision, result, durable state, persistence,
recovery, and replay responsibilities remain preserved but require explicitly
approved canonical owners. F07/F08/F09/F10/F11 ownership remains unchanged and
major Phase 8 expansion remains PAUSED.

FORTRESS-06D2D — IMPLEMENTED AND VERIFIED. It completes neither F06D nor
FORTRESS-06. F06D2E+ and FORTRESS-07 remain NOT STARTED, Step 7
remains IN PROGRESS, Step 8 remains NOT STARTED — BLOCKED BY STEP 7, Fortress
certification remains NOT STARTED, RAA-003 remains OPEN, RAA-007 remains
RESOLVED WITH EVIDENCE, and major Phase 8 expansion remains PAUSED.

---

## 13. F06D2E Current State and Stop Boundary

FORTRESS-06D2E — IMPLEMENTED AND VERIFIED. The exact baseline was mechanically
reconciled before edits: 16 configured prototype-tool files, 101 source tests,
35 configured legacy-facing files, and 22 configured `executive_brain`
importers.

| Family | Files | Source tests | Archive family |
|---|---:|---:|---|
| Browser | 5 | 32 | `legacy_quarantine/tests/tools/browser/` |
| Windows/Desktop | 6 | 39 | `legacy_quarantine/tests/tools/windows/` |
| Development/VS Code | 5 | 30 | `legacy_quarantine/tests/tools/development/` |
| Total | 16 | 101 | 16 `.py.legacy` archives |

All 101 source test definitions were top-level, synchronous, pytest-collectable
cases. The containment authority gained two net-new tests, contributing two
collected cases. Collection therefore reconciles exactly:

```text
1,935 pre-D2E collected cases
- 101 retired collected cases
+   2 new containment cases
= 1,836 post-D2E collected cases
```

The 16 exact archive moves are:

| Former configured path | Non-Python archive |
|---|---|
| `tests/tests/tools/test_browser_automation_tool.py` | `legacy_quarantine/tests/tools/browser/test_browser_automation_tool.py.legacy` |
| `tests/tests/tools/test_cookies_tool.py` | `legacy_quarantine/tests/tools/browser/test_cookies_tool.py.legacy` |
| `tests/tests/tools/test_downloads_tool.py` | `legacy_quarantine/tests/tools/browser/test_downloads_tool.py.legacy` |
| `tests/tests/tools/test_tabs_tool.py` | `legacy_quarantine/tests/tools/browser/test_tabs_tool.py.legacy` |
| `tests/tests/tools/test_web_search_tool.py` | `legacy_quarantine/tests/tools/browser/test_web_search_tool.py.legacy` |
| `tests/tests/tools/test_clipboard_tool.py` | `legacy_quarantine/tests/tools/windows/test_clipboard_tool.py.legacy` |
| `tests/tests/tools/test_close_application_tool.py` | `legacy_quarantine/tests/tools/windows/test_close_application_tool.py.legacy` |
| `tests/tests/tools/test_launch_application_tool.py` | `legacy_quarantine/tests/tools/windows/test_launch_application_tool.py.legacy` |
| `tests/tests/tools/test_notification_tool.py` | `legacy_quarantine/tests/tools/windows/test_notification_tool.py.legacy` |
| `tests/tests/tools/test_process_manager_tool.py` | `legacy_quarantine/tests/tools/windows/test_process_manager_tool.py.legacy` |
| `tests/tests/tools/test_services_tool.py` | `legacy_quarantine/tests/tools/windows/test_services_tool.py.legacy` |
| `tests/tests/tools/test_build_tool.py` | `legacy_quarantine/tests/tools/development/test_build_tool.py.legacy` |
| `tests/tests/tools/test_debug_tool.py` | `legacy_quarantine/tests/tools/development/test_debug_tool.py.legacy` |
| `tests/tests/tools/test_git_tool.py` | `legacy_quarantine/tests/tools/development/test_git_tool.py.legacy` |
| `tests/tests/tools/test_project_tool.py` | `legacy_quarantine/tests/tools/development/test_project_tool.py.legacy` |
| `tests/tests/tools/test_run_tool.py` | `legacy_quarantine/tests/tools/development/test_run_tool.py.legacy` |

Each archive is byte-identical to its former source by both SHA-256 and Git blob
identity. Every archive ends in `.py.legacy`, remains outside Python import and
pytest collection suffixes, and no `__init__.py` exists anywhere under
`legacy_quarantine/`.

No replacement browser, desktop, or development capability test was required.
The generic Tool Platform requirements are already configured against canonical
`jaos.tools` contracts, registry, manager, execution engine, and
permission/approval/audit boundaries. Prototype `ToolResponse`/`ToolStatus`
shapes, tool-name identities, browser/profile/download internals, direct browser
and clipboard behavior, process and service implementation details, unsafe
launch behavior, arbitrary command execution, VS Code coupling, and prototype
Git plumbing were intentionally not ported.

Browser, desktop/PC-control, and Developer Platform capability remain assigned
to future approved owning workstreams. F07 permission/approval/risk/audit policy
and F11 injection, path-boundary, malicious-input, and platform-abuse testing
remain deferred. F06D2E introduced none of those capabilities or policies.

The existing collection containment authority proves the 16 configured paths
are gone, the 16 pinned archives are non-importable and non-collectable, zero
configured prototype-tool importers remain, and the six remaining
`executive_brain` importers are exactly:

- `tests/tests/integration/test_memory_runtime_integration.py`;
- `tests/tests/memory/test_memory_manager.py`;
- `tests/tests/memory/test_memory_registry.py`;
- `tests/tests/memory/test_working_memory.py`;
- `tests/tests/ai/test_ollama_provider.py`; and
- `tests/tests/ai/test_openai_provider.py`.

AST inspection mechanically verified 35 -> 19 configured legacy-facing files
and 22 -> 6 configured `executive_brain` importers. The exact remaining 19
legacy-facing configured files comprise:

- six Memory/provider `executive_brain` importers listed above;
- ten satellite/runtime integrations:
  `test_communication_runtime_integration.py`,
  `test_dashboard_runtime_integration.py`,
  `test_development_runtime_integration.py`,
  `test_engineering_runtime_integration.py`,
  `test_infrastructure_runtime_integration.py`,
  `test_knowledge_runtime_integration.py`,
  `test_pc_control_runtime_integration.py`,
  `test_security_runtime_integration.py`,
  `test_system_services_runtime_integration.py`, and
  `test_workflow_runtime_integration.py`, all under `tests/tests/integration/`;
  and
- three platform/core/kernel/config containment tests:
  `tests/tests/platform/test_config_containment.py`,
  `tests/tests/platform/test_core_runtime_integration.py`, and
  `tests/tests/platform/test_kernel_runtime_integration.py`.

The corresponding 16 production prototype modules remain untouched and
importable for F06E disposition, but are not registered or loaded by canonical
`ToolManager`, referenced by `PlatformComposition`, or imported by canonical
production code. No production code changed.

The retired configured tests use mocks, fakes, or test-owned temporary paths.
They perform no real browser/network operation, process launch or termination,
service or clipboard mutation, Git/build/run command, download, repository
runtime-data write, or persistent runtime-state write. No runtime-data migration
occurred.

Verified F06D2E evidence, all recorded successful gates exit code 0:

| Gate | Result |
|---|---|
| Focused containment/import/Tool contracts/registry/manager/filesystem/Executive | 204 passed |
| Tools suite | 119 passed |
| Executive suite | 7 passed |
| Composition suite | 49 passed |
| Platform suite | 377 passed, 1 skipped |
| Integration suite | 51 passed |
| Full configured `tests/tests` | 1,835 passed, 1 skipped |
| Repository-root collection | 1,836 collected |
| Ruff on the changed Python containment authority | All checks passed |

All successful pytest gates used repository Python,
`PYTHONDONTWRITEBYTECODE=1`, `-B`, `-p no:cacheprovider`, and unique external
`--basetemp` paths with the established temporary Windows ACL runner shim. The
shim changed no repository source or test behavior and is not retained in this
change set. The one skip remains the known Windows directory-symlink privilege
limitation.

FORTRESS-06D2E completes neither F06D nor FORTRESS-06. RAA-003 remains OPEN,
RAA-007 remains RESOLVED WITH EVIDENCE, FORTRESS-07 remains NOT STARTED, Step 7
remains IN PROGRESS, Step 8 remains NOT STARTED — BLOCKED BY STEP 7, Fortress
certification remains NOT STARTED, and major Phase 8 expansion remains PAUSED.

---

## 14. FORTRESS-06D Memory Adjudication Governance

The read-only Memory adjudication completed on 2026-08-31 and mechanically
identified four configured files containing 30 source tests:

| Configured path | Source tests | Adjudication result before ADR-0013 |
|---|---:|---|
| `tests/tests/integration/test_memory_runtime_integration.py` | 4 | Clear quarantine candidate |
| `tests/tests/memory/test_memory_manager.py` | 9 | Founder-gated compatibility conflict |
| `tests/tests/memory/test_memory_registry.py` | 7 | Clear quarantine candidate |
| `tests/tests/memory/test_working_memory.py` | 10 | Founder-gated compatibility conflict |
| Total | 30 | Four configured files |

ADR-0013 records the Founder-approved supersession of exact
`executive_brain.memory.WorkingMemory` API compatibility. The exact legacy
`WorkingMemory`, `MemoryManager`, and `MemoryRegistry` implementations are
shadow architecture, while their logical responsibilities remain preserved for
canonical persistent Memory or explicitly deferred future owners. No
replacement Working Memory runtime authority is authorized.

All four configured Memory files are therefore governance-approved quarantine
candidates. Controlled implementation has NOT STARTED. The current counts
remain 19 configured legacy-facing files and six configured `executive_brain`
importers. The following are projections only after successful controlled
implementation:

- configured legacy-facing files: 19 -> 15;
- configured `executive_brain` importers: 6 -> 2; and
- remaining importers: `tests/tests/ai/test_openai_provider.py` and
  `tests/tests/ai/test_ollama_provider.py`.

Persistent Memory remains owned by canonical `MemoryStore`/`SQLiteStore`.
Transient request/context ownership awaits an approved Context Platform or
task-session owner; transient mission/plan/decision/result references await
explicit future canonical owners, with durable forms assigned to FORTRESS-08
where applicable; health/readiness/degradation belongs to FORTRESS-10;
Experience Memory remains a separate future platform; and RAA-009 continues to
govern deferred `MemoryContextSource`/`MemorySearchEngine` coupling.

No test, production source, or quarantine artifact changed, and no runtime data
migrated. Legacy production Memory sources remain untouched pending their
approved FORTRESS-06 production-source and compatibility disposition. RAA-003
remains OPEN and RAA-009 remains OPEN — DEFERRED. F06D and FORTRESS-06 remain IN
PROGRESS; F08 and F10 remain NOT STARTED; Step 8 and Fortress certification
remain NOT STARTED; and major Phase 8 expansion remains PAUSED.

---

## 15. FORTRESS-06D Memory Retirement

ADR-0013 is authoritative. Controlled implementation retired the four
configured legacy Executive Memory test paths and preserved their exact payloads:

| Retired configured path | Collected tests | Archive | SHA-256 |
|---|---:|---|---|
| `tests/tests/integration/test_memory_runtime_integration.py` | 4 | `legacy_quarantine/tests/integration/test_memory_runtime_integration.py.legacy` | `83bdf8e9cfd5b01fc9b487b4a1d9928fd30e14128beded4a226a97b7f30b9024` |
| `tests/tests/memory/test_memory_manager.py` | 9 | `legacy_quarantine/tests/memory/test_memory_manager.py.legacy` | `1c888f4d7c9950a2f1090fe06d8dff3de77ea9d7bdbc02c49a73fa5b5e90b094` |
| `tests/tests/memory/test_memory_registry.py` | 7 | `legacy_quarantine/tests/memory/test_memory_registry.py.legacy` | `b2503c77d160f01dd9c6a3b284086862cb27da297f52b78f5a39abdd0013378e` |
| `tests/tests/memory/test_working_memory.py` | 10 | `legacy_quarantine/tests/memory/test_working_memory.py.legacy` | `a09fa6bb85e7716d1622a2d75275963ba0081ac8ba36bee05bbcba76e35bb353` |
| Total | 30 | Four byte-identical `*.py.legacy` archives | Verified |

The archives are non-Python and non-collectable, no `__init__.py` exists under
`legacy_quarantine/`, and no configured legacy Memory importer remains. No
canonical replacement `WorkingMemory`, `MemoryManager`, or `MemoryRegistry` was
created. Canonical persistent Memory continues through independently tested
`MemoryStore`/`SQLiteStore`; transient context and mission/plan/decision/result
responsibilities remain preserved for explicit future owners; FORTRESS-08 owns
applicable durable forms, FORTRESS-10 owns future health semantics, Experience
Memory remains a separate future platform, and RAA-009 remains OPEN — DEFERRED.

Mechanical AST/import analysis verified the achieved reductions:

- configured legacy-facing files: 19 -> 15; and
- configured `executive_brain` importers: 6 -> 2.

The remaining two `executive_brain` importers are exactly:

- `tests/tests/ai/test_ollama_provider.py`; and
- `tests/tests/ai/test_openai_provider.py`.

The remaining 15 configured legacy-facing files are:

| Family | Configured path |
|---|---|
| Provider | `tests/tests/ai/test_ollama_provider.py` |
| Provider | `tests/tests/ai/test_openai_provider.py` |
| Satellite/runtime | `tests/tests/integration/test_communication_runtime_integration.py` |
| Satellite/runtime | `tests/tests/integration/test_dashboard_runtime_integration.py` |
| Satellite/runtime | `tests/tests/integration/test_development_runtime_integration.py` |
| Satellite/runtime | `tests/tests/integration/test_engineering_runtime_integration.py` |
| Satellite/runtime | `tests/tests/integration/test_infrastructure_runtime_integration.py` |
| Satellite/runtime | `tests/tests/integration/test_knowledge_runtime_integration.py` |
| Satellite/runtime | `tests/tests/integration/test_pc_control_runtime_integration.py` |
| Satellite/runtime | `tests/tests/integration/test_security_runtime_integration.py` |
| Satellite/runtime | `tests/tests/integration/test_system_services_runtime_integration.py` |
| Satellite/runtime | `tests/tests/integration/test_workflow_runtime_integration.py` |
| Platform/core/kernel/config | `tests/tests/platform/test_config_containment.py` |
| Platform/core/kernel/config | `tests/tests/platform/test_core_runtime_integration.py` |
| Platform/core/kernel/config | `tests/tests/platform/test_kernel_runtime_integration.py` |

The retired tests and legacy implementations mutate only in-memory dictionaries,
dataclass fields, `ServiceContainer`, `RuntimeContext`, and `EventBus` state.
They invoke neither canonical `SQLiteStore` nor another filesystem writer. No
runtime-data migration or protected-state mutation occurred. Legacy
`executive_brain.memory` production modules remain importable for later approved
production-source/compatibility disposition and remain outside the canonical
launcher, composition, Executive, and Conversation production paths.

Verification used repository Python 3.14.6,
`PYTHONDONTWRITEBYTECODE=1`, `-B`, `-p no:cacheprovider`, unique external
`--basetemp` roots, and the established temporary Windows ACL runner shim:

| Gate | Result |
|---|---|
| Four retired files before quarantine | 30 collected |
| Focused containment/Memory/composition/import boundary | 243 passed |
| Memory suite | 361 passed |
| Composition suite | 49 passed |
| Platform suite | 379 passed, 1 skipped |
| Integration suite | 47 passed |
| Full configured `tests/tests` | 1,807 passed, 1 skipped |
| Root collection | 1,808 collected |
| Ruff | All checks passed |

Collection reconciles as `1,836 - 30 + 2 = 1,808`: 30 previously collected
Memory cases retired and two containment cases added. Preliminary runs exposed
the documented Python 3.14 Windows `0o700` pytest temp-tree ACL limitation; the
established ACL shim changed only external temporary-directory inheritance.
The first valid focused run then exposed one stale D2C containment assertion,
which was reconciled with ADR-0013 before the complete ladder passed.

No production source or canonical Memory contract changed, no new Working
Memory authority was created, no runtime data migrated, and no provider,
satellite, F06E/F06F/F06G/F06H, F07/F08/F10, RAA-009, Context, Experience
Memory, or Phase 8 expansion began.

FORTRESS-06D Memory retirement — IMPLEMENTED AND VERIFIED.
F06D and FORTRESS-06 remain IN PROGRESS; RAA-003 remains OPEN; RAA-007 remains
RESOLVED WITH EVIDENCE; RAA-009 remains OPEN — DEFERRED; Step 8 remains NOT
STARTED — BLOCKED BY STEP 7; Fortress certification remains NOT STARTED; and
major Phase 8 expansion remains PAUSED.

---

## 16. FORTRESS-06D Provider Adjudication Governance

ADR-0014 is authoritative. The completed read-only adjudication identified the
final two configured `executive_brain` importers:

| Configured file | Source tests | Collected cases | Current disposition |
|---|---:|---:|---|
| `tests/tests/ai/test_ollama_provider.py` | 9 | 9 | PORT + QUARANTINE — GOVERNANCE APPROVED |
| `tests/tests/ai/test_openai_provider.py` | 11 | 11 | PORT + QUARANTINE — GOVERNANCE APPROVED |
| Total | 20 | 20 | Implementation NOT STARTED |

Both files exercise unreachable `executive_brain` shadow adapters through
offline mocks/fakes. They do not establish real Ollama or OpenAI integration
evidence. Before controlled retirement, exactly three provider-neutral current
requirements must receive configured canonical evidence:

1. `AIRequest` rejects blank or whitespace-only prompts.
2. `ProviderManager.generate()` rejects invalid or non-`AIRequest` input before
   provider execution.
3. Provider generation failure is normalized as `ProviderManagerError`, and
   canonical failure metrics/state are updated truthfully.

No provider-specific legacy behavior is to be ported. Canonical provider
authority remains `PlatformComposition` -> `ProviderManager`/`AIManager` ->
canonical provider abstractions -> deterministic `MockProvider`. OpenAI is an
initial FORTRESS-09 reference-provider candidate only, not architectural
authority, a permanent dependency, the sole supported provider, or a
local/offline runtime requirement. Ollama remains optional and is not mandatory
for FORTRESS-09 certification.

FORTRESS-09 remains NOT STARTED and retains later ownership of approved
concrete-provider integration and resilience, including timeouts, retries,
circuit breaking, fallback, health/reachability, unavailable providers, auth
and rate-limit failures, malformed responses, secret/config integration,
graceful degradation, telemetry, model discovery, streaming/capabilities, and
opt-in real-provider tests. None is implemented through this governance record.

At the ADR-0014 governance checkpoint, provider retirement implementation had
NOT STARTED and the mechanically verified counts remained:

- configured legacy-facing files: 15; and
- configured `executive_brain` importers: 2.

Only after separately authorized and verified implementation are the projected
counts 15 -> 13 and 2 -> 0. No provider test, production source, quarantine
artifact, credential, network state, or runtime data changed. Once this
governance change was checkpointed, provider retirement became READY FOR
CONTROLLED IMPLEMENTATION subject to separate implementation authorization.
The later verified implementation is recorded in section 17. RAA-003 remained
OPEN; F06D and FORTRESS-06 remained IN PROGRESS; Step 8 and Fortress
certification remained NOT STARTED; and major Phase 8 expansion remained PAUSED.

---

## 17. FORTRESS-06D Provider Retirement

ADR-0014 is authoritative. Before quarantine, exactly three provider-neutral
requirements were added as configured canonical evidence in
`tests/tests/ai/test_canonical_provider_contract.py`:

1. blank and whitespace-only `AIRequest` prompts are rejected;
2. non-`AIRequest` input is rejected by `ProviderManager.generate()` before
   provider execution or state mutation; and
3. provider generation failure emerges as `ProviderManagerError`, with truthful
   canonical request, success, failure, and last-error state.

All three passed before retirement through canonical `jaos.*` contracts and the
deterministic `MockProvider`. They use no real provider, network, or credential
and port no OpenAI- or Ollama-specific behavior.

The exact shadow-provider payloads are preserved outside configured execution:

| Retired configured path | Source/collected tests | Archive | SHA-256 | Git blob |
|---|---:|---|---|---|
| `tests/tests/ai/test_ollama_provider.py` | 9 | `legacy_quarantine/tests/ai/test_ollama_provider.py.legacy` | `4b25c507f2bb886479514e324bfd4df0d366f98db2898e87ff7070dbd1153c30` | `6a260352bd1fd2db5b0072322be43479988d5e93` |
| `tests/tests/ai/test_openai_provider.py` | 11 | `legacy_quarantine/tests/ai/test_openai_provider.py.legacy` | `cfc6d61aa8886c6b8a07d28c8108ca2998103bcf7129212a05771c9ee04192e6` | `de205e557bed369bac57e0254cbe76c497afe5e0` |
| Total | 20 | Two byte/blob-identical `*.py.legacy` archives | Verified | Verified |

Both archives are non-importable and non-collectable, and no `__init__.py`
exists under `legacy_quarantine/`. The existing containment authority also
proves that both executable paths are absent, the canonical replacement imports
only `jaos` and `pytest`, the configured `executive_brain` importer count is
zero, and both legacy provider production sources remain present for later F06
disposition.

Mechanical AST/import analysis verified the achieved reductions:

- configured legacy-facing files: 15 -> 13; and
- configured `executive_brain` importers: 2 -> 0.

The exact 13 configured legacy-facing files remaining at that provider
checkpoint were:

| Family | Configured path |
|---|---|
| Satellite/runtime | `tests/tests/integration/test_communication_runtime_integration.py` |
| Satellite/runtime | `tests/tests/integration/test_dashboard_runtime_integration.py` |
| Satellite/runtime | `tests/tests/integration/test_development_runtime_integration.py` |
| Satellite/runtime | `tests/tests/integration/test_engineering_runtime_integration.py` |
| Satellite/runtime | `tests/tests/integration/test_infrastructure_runtime_integration.py` |
| Satellite/runtime | `tests/tests/integration/test_knowledge_runtime_integration.py` |
| Satellite/runtime | `tests/tests/integration/test_pc_control_runtime_integration.py` |
| Satellite/runtime | `tests/tests/integration/test_security_runtime_integration.py` |
| Satellite/runtime | `tests/tests/integration/test_system_services_runtime_integration.py` |
| Satellite/runtime | `tests/tests/integration/test_workflow_runtime_integration.py` |
| Platform/core/kernel/config | `tests/tests/platform/test_config_containment.py` |
| Platform/core/kernel/config | `tests/tests/platform/test_core_runtime_integration.py` |
| Platform/core/kernel/config | `tests/tests/platform/test_kernel_runtime_integration.py` |

Legacy `executive_brain.ai.providers.openai_provider` and
`executive_brain.ai.providers.ollama_provider` remain importable production
shadow sources for later F06 disposition. OpenAI remains only an initial F09
reference-provider candidate; Ollama remains optional and nonmandatory; F09
remains NOT STARTED. No production code, concrete provider capability,
credential, network request, localhost inference, subprocess, provider-memory
writer, repository writer, or runtime-data migration changed or ran.

Verification used repository Python 3.14.6, `PYTHONDONTWRITEBYTECODE=1`, `-B`,
`-p no:cacheprovider`, unique external `--basetemp` roots, and the established
temporary Windows ACL runner shim:

| Gate | Result |
|---|---|
| Three port-first canonical requirements | 3 passed |
| Focused retirement/containment | 8 passed |
| Focused canonical AI/composition/containment/import/conversation failure | 127 passed |
| Supplemental flat canonical ProviderManager evidence | 14 passed |
| Configured AI suite | 16 passed |
| Composition suite | 49 passed |
| Platform suite | 381 passed, 1 skipped |
| Integration suite | 47 passed |
| Full configured `tests/tests` | 1,792 passed, 1 skipped |
| Repository-root collection | 1,793 collected |
| Ruff on both changed Python files | All checks passed |

Collection reconciles exactly as `1,808 - 20 + 3 + 2 = 1,793`. Explicit
supplemental invocation of excluded flat `tests/test_provider_router.py` and
`tests/test_mock_provider.py` exited 2 during collection because those
historical files import concrete `MockProvider` from a public facade where the
active configured facade contract intentionally does not export it. They were
not modified, are outside configured `tests/tests` certification, do not block
this provider-retirement checkpoint, and remain legacy/facade debt for later
appropriate Fortress disposition.

FORTRESS-06D provider retirement — IMPLEMENTED AND VERIFIED.
This state completes neither F06D nor FORTRESS-06. RAA-003 remains OPEN;
RAA-007 remains RESOLVED
WITH EVIDENCE; RAA-009 remains OPEN — DEFERRED; F07/F08/F09/F10 remain NOT
STARTED; Step 8 remains NOT STARTED — BLOCKED BY STEP 7; Fortress certification
remains NOT STARTED; and major Phase 8 expansion remains PAUSED.

---

## 18. FORTRESS-06D Satellite/Runtime Shadow-Test Retirement

The read-only adjudication found no current canonical capability requirement
that depended uniquely on the ten configured satellite/runtime integration
files. Their exact classes remain unreachable shadow, prototype, or
future-platform authorities, while their generic lifecycle and composition
requirements are already covered by configured canonical tests. The ten files
were therefore retired without adding capability behavior or modifying
production code.

The exact baseline and archive integrity evidence is:

| Retired configured path | Source/collected tests | Archive | SHA-256 | Git blob |
|---|---:|---|---|---|
| `tests/tests/integration/test_communication_runtime_integration.py` | 3 | `legacy_quarantine/tests/integration/test_communication_runtime_integration.py.legacy` | `64a85ec44c7469fd9b1e5b8334668d67e6e736a4ed8b9c077073b676c033c8e3` | `bd1a3f3c733db842c2891bbb29318c521daa6b33` |
| `tests/tests/integration/test_dashboard_runtime_integration.py` | 3 | `legacy_quarantine/tests/integration/test_dashboard_runtime_integration.py.legacy` | `7d098bc62d40594125a3ba631187438685e25a9b7842d30986ed21ae98b12428` | `90305b7807659ca75ec33210d38ce1f824f3ddab` |
| `tests/tests/integration/test_development_runtime_integration.py` | 3 | `legacy_quarantine/tests/integration/test_development_runtime_integration.py.legacy` | `3e269159210a0a0c17592bb59ffff53cfcec53cb5fd4a2c60fd2f42ec9116888` | `cb94116c640290a0bdf4b6d4c0a9c5ddb23b167a` |
| `tests/tests/integration/test_engineering_runtime_integration.py` | 3 | `legacy_quarantine/tests/integration/test_engineering_runtime_integration.py.legacy` | `4fcef4fcca5c604f613f229b81916aea7fa8a5d8e96dc362ee83475c76eb62fd` | `0535adff6467fa511f13b380f5a2f848dfad1c46` |
| `tests/tests/integration/test_infrastructure_runtime_integration.py` | 3 | `legacy_quarantine/tests/integration/test_infrastructure_runtime_integration.py.legacy` | `773d975c2155aa093a3f16cf8f6748b3870016e3ac401704f6ffd40f6361b04a` | `3a84c609b3245e9ce94b5c8ef16ed0059240d05a` |
| `tests/tests/integration/test_knowledge_runtime_integration.py` | 3 | `legacy_quarantine/tests/integration/test_knowledge_runtime_integration.py.legacy` | `b4551ead376823afdfee721322f5015326adab87be229d7971621a8d49f4c2ef` | `9c6451c32de8dd5b6e86b095c799344632a5035e` |
| `tests/tests/integration/test_pc_control_runtime_integration.py` | 3 | `legacy_quarantine/tests/integration/test_pc_control_runtime_integration.py.legacy` | `d97e91ef336b7fc6086ce97d03bc5e102b3d01b6cee2acadd37d57bbd79a881c` | `fac8e45d19b3745200a4a9668164d80ba3954d73` |
| `tests/tests/integration/test_security_runtime_integration.py` | 3 | `legacy_quarantine/tests/integration/test_security_runtime_integration.py.legacy` | `32e56102ec63eced4534ab17f914c6d71a1ed9132e5430c37d5057b1a25e64d7` | `f013bc3b6db79ba4edb3e1e1fe01ef96905e5c74` |
| `tests/tests/integration/test_system_services_runtime_integration.py` | 3 | `legacy_quarantine/tests/integration/test_system_services_runtime_integration.py.legacy` | `1db3d498db9633d21d809ae5bfa7d9f58f1c14866fcd1f98f660eb53efdcf097` | `f9438f1c8aa963ae8bc98a4ec0bd2a2b735a0a53` |
| `tests/tests/integration/test_workflow_runtime_integration.py` | 3 | `legacy_quarantine/tests/integration/test_workflow_runtime_integration.py.legacy` | `6bbfc848eeb30af9788bc2f3ad0897810dec8f4c6ced072227f3ac8e808bf83b` | `7ff01598377ef5c1b671a8e79b358f90fb93114c` |
| Total | 30 | Ten byte/blob-identical `*.py.legacy` archives | Verified | Verified |

All archives are non-importable and non-collectable, and no `__init__.py`
exists under `legacy_quarantine/`. The existing containment authority gained
exactly two cases: archive/payload containment and current residual-inventory
plus production-source preservation. Mechanical import analysis verified:

- configured legacy-facing files: 13 -> 3; and
- configured `executive_brain` importers: 0 -> 0.

The exact remaining configured legacy-facing inventory at the satellite
checkpoint was:

| Disposition | Configured path | Collected cases |
|---|---|---:|
| KEEP TEMPORARILY | `tests/tests/platform/test_config_containment.py` | 11 |
| Separate later retirement slice | `tests/tests/platform/test_core_runtime_integration.py` | 3 |
| Separate later retirement slice | `tests/tests/platform/test_kernel_runtime_integration.py` | 3 |

At that checkpoint all three files remained configured and unchanged, and
core/kernel retirement had not started. The later core/kernel retirement is
recorded in Section 19. The config containment file continues to certify the
legacy writer and alternate-launcher boundary until later authorized F06E/F06F
disposition.

The production satellite modules remain present and unchanged under
`communication/`, `dashboard/`, `development/`, `engineering/`,
`infrastructure/`, `knowledge/`, `pc_control/`, `security/`,
`system_services/`, and `workflow/` for later F06E production-source
disposition. `core/`, `kernel/`, `main.py`, and `executive_brain/` also remain
unchanged. No future satellite capability or policy work began.

The retired tests exercised only in-memory prototype behavior. They performed
no network access, subprocess or thread/process launch, desktop control,
Windows service mutation, repository/runtime-data write, provider-memory
write, or runtime-data migration.

Verification used repository Python 3.14.6, `PYTHONDONTWRITEBYTECODE=1`, `-B`,
`-p no:cacheprovider`, unique external `--basetemp` roots, and the established
temporary Windows ACL runner shim:

| Gate | Result |
|---|---|
| Ten retired files before quarantine | 30 collected |
| Focused containment/canonical runtime and ownership | 166 passed |
| Integration suite | 17 passed |
| Platform suite | 383 passed, 1 skipped |
| Composition suite | 49 passed |
| Full configured `tests/tests` | 1,764 passed, 1 skipped |
| Root collection | 1,765 collected |
| Ruff | All checks passed |

Collection reconciles exactly as `1,793 - 30 + 2 = 1,765`. Preliminary direct
pytest attempts encountered the documented Python 3.14 Windows `0o700` temp
ACL limitation; the successful in-memory runner shim changed only external
temporary-directory inheritance and left no repository helper or diff.

FORTRESS-06D satellite/runtime shadow-test retirement — IMPLEMENTED AND
VERIFIED. F06D and FORTRESS-06 remain IN PROGRESS. RAA-003 remains OPEN;
RAA-007 remains RESOLVED WITH EVIDENCE; RAA-009 remains OPEN — DEFERRED;
F07/F08/F09/F10 remain NOT STARTED; Step 8 remains NOT STARTED — BLOCKED BY
STEP 7; Fortress certification remains NOT STARTED; and major Phase 8 expansion
remains PAUSED.

---

## 19. FORTRESS-06D Core/Kernel Shadow-Runtime Test Retirement

The authorized core/kernel slice retired the two remaining shadow-runtime
integration tests. `core.engine.JarvisEngine` remains an alternate legacy
composition root reachable through `main.py`, not the canonical `run_jaos.py`
and `PlatformComposition` path. `kernel.jaos_kernel.JAOSKernel` remains a
shadow runtime wrapper with separate lifecycle and registry ownership. Their
durable runtime-identity, registration, lifecycle, readiness, and shutdown
requirements already have configured canonical evidence, so no behavior was
ported and no production code changed.

The exact baseline and archive integrity evidence is:

| Retired configured path | Source/collected tests | Archive | SHA-256 | Git blob |
|---|---:|---|---|---|
| `tests/tests/platform/test_core_runtime_integration.py` | 3 | `legacy_quarantine/tests/platform/test_core_runtime_integration.py.legacy` | `7cea6699d3842677ba3b78796f385e8f57670ae22208418955d01666bed8bd39` | `152c1cd59fadcd84f48ff6ac0c03cd07002784a7` |
| `tests/tests/platform/test_kernel_runtime_integration.py` | 3 | `legacy_quarantine/tests/platform/test_kernel_runtime_integration.py.legacy` | `d629bbb6ee27bff0bcb170c04b7e13ec6946a67f05e9ef041a93994f57cea85d` | `29f30e0ce9ec5e28060d3a3660d092134a1495e6` |
| Total | 6 | Two byte/blob-identical `*.py.legacy` archives | Verified | Verified |

Both archives are non-importable and non-collectable, and no `__init__.py`
exists under `legacy_quarantine/`. The original configured paths are absent.
The existing containment authority gained exactly two cases: core/kernel
archive-payload containment and final configured legacy-facing inventory plus
production-source preservation. Mechanical import analysis verified:

- configured legacy-facing files: 3 -> 1;
- configured `executive_brain` importers: 0 -> 0; and
- configured legacy-facing progression:
  `67 -> 59 -> 52 -> 48 -> 44 -> 35 -> 19 -> 15 -> 13 -> 3 -> 1`.

The sole remaining configured legacy-facing file is
`tests/tests/platform/test_config_containment.py`. It remains intentionally
configured and byte-unchanged at SHA-256
`d862bd601301ae7bfc85aa16a5cc9f31e5f77b23bc54e84689a4276a5a2a447c`,
with nine source definitions and eleven collected cases. It continues to
certify tracked-default immutability, overlay precedence, mutable-key and
save-target restrictions, path containment, `ConfigManager` responsibility
separation, and absence of `JAOS_RUNTIME_DIR` redirection until later
authorized F06E/F06F disposition.

No `JarvisEngine`, `JAOSKernel`, alternate registry, literal lifecycle state,
or alternate runtime-ownership behavior was ported. `core/`, `kernel/`,
`main.py`, and `executive_brain/` remain present and unchanged for later
authorized production-source, writer, and compatibility disposition. The
retired tests do not invoke `JarvisEngine.start()`, action-history, snapshot,
recovery, plugin, or interactive-loop behavior; they perform no network,
subprocess, desktop-control, or persistent runtime-state operation. The
production writer graph remains present and untouched, and no runtime-data
migration occurred.

Verification used repository Python 3.14.6, `PYTHONDONTWRITEBYTECODE=1`, `-B`,
`-p no:cacheprovider`, unique external `--basetemp` roots, and the established
temporary Windows ACL runner shim:

| Gate | Result |
|---|---|
| Two retired files before quarantine | 6 collected |
| Focused containment/config/runtime/composition/launcher tests | 166 passed |
| Platform suite | 379 passed, 1 skipped |
| Composition suite | 49 passed |
| Integration suite | 17 passed |
| Full configured `tests/tests` | 1,760 passed, 1 skipped |
| Root collection | 1,761 collected |
| Ruff on the changed Python file | All checks passed |

Collection reconciles exactly as `1,765 - 6 + 2 = 1,761`.

FORTRESS-06D core/kernel shadow-runtime test retirement — IMPLEMENTED AND
VERIFIED. F06D and FORTRESS-06 remain IN PROGRESS. RAA-003 remains OPEN;
RAA-007 remains RESOLVED WITH EVIDENCE; RAA-009 remains OPEN — DEFERRED;
F07/F08/F09/F10 remain NOT STARTED; Step 8 remains NOT STARTED — BLOCKED BY
STEP 7; Fortress certification remains NOT STARTED; and major Phase 8 expansion
remains PAUSED. No later slice started.

---

## 20. FORTRESS-06E Communication Production-Root Quarantine Pilot

The first controlled F06E production-source slice removed the live
`communication/` root after re-verifying its six-source inventory and exact
caller boundary. Mechanical static analysis found zero canonical production
callers, zero legacy production callers, zero configured-test callers, and no
active dynamic loader capable of reaching `communication.*`. Seven excluded
flat historical tests retain stale imports outside configured `tests/tests`
certification; they are unchanged and remain later F06G/F06H compatibility
debt.

The authoritative original-to-archive mapping is:

| Original production path | Archive path | SHA-256 | Git blob | Disposition |
|---|---|---|---|---|
| `communication/calendar_manager.py` | `legacy_quarantine/production/communication/calendar_manager.py.legacy` | `de550bf3ddb8ea4c7c9be56e492f54c54dfa5280a7e8ef853def40eea8894911` | `807089aa2bc86cf92f42ae65fa8ececddc13db98` | ARCHIVE-ONLY — exact source preserved |
| `communication/communication_hub.py` | `legacy_quarantine/production/communication/communication_hub.py.legacy` | `d34c4f6b33410c69498493675fef02d59ae88e7bee366c97d6311c0295eca02b` | `65bb8f303128b6847fa2ac9913af5d627ad82ec1` | ARCHIVE-ONLY — exact source preserved |
| `communication/contacts_manager.py` | `legacy_quarantine/production/communication/contacts_manager.py.legacy` | `2f0c86a51200d40513d3827def63c464c8f3fc10d2cce433a761a999932bb565` | `69f189614e5c5fbf707561752b99fec3fd9a154f` | ARCHIVE-ONLY — exact source preserved |
| `communication/conversation_manager.py` | `legacy_quarantine/production/communication/conversation_manager.py.legacy` | `8bace0ec95836012cf3cf7fceb2fae929068ca975c010502a33e51a05cb0e72b` | `3dacf67cda7110b7b92c8b76e9141a63ee5470c4` | ARCHIVE-ONLY — exact source preserved |
| `communication/email_manager.py` | `legacy_quarantine/production/communication/email_manager.py.legacy` | `997d2c4ea5cfb8fd82194d86158a07b5b8d593dcc22cb5f0fec42f595500d08b` | `824e1eccc45973d45aad7988397e86df211b6dd7` | ARCHIVE-ONLY — exact source preserved |
| `communication/meeting_assistant.py` | `legacy_quarantine/production/communication/meeting_assistant.py.legacy` | `e8ff0e6b877b3c4546c4c6810cb418c41b0210b5896956fa60de8608f35bf542` | `c36d257ebcf8a5b91ca4f4c96b43655581a7789a` | ARCHIVE-ONLY — exact source preserved |

All six archive payloads are byte- and Git-blob-identical to HEAD at their
former paths. They use the `.py.legacy` suffix, are non-importable and
non-collectable, and introduce no `__init__.py`. The live `communication/`
root is absent. Repository Python source does not import from
`legacy_quarantine`, and the canonical `run_jaos.py` static closure remains
disjoint from both the former root and the archive.

Static source inspection found no persistent writer, runtime-data writer,
network request, subprocess, process/thread creation, desktop/application or
service control, or other external-effect implementation requiring
preservation. The pilot introduced no replacement capability, forwarding
wrapper, compatibility alias, or canonical production change. `jaos/` and
`jaos_platform/` remain unchanged.

The existing collection-containment authority gained exactly two configured
cases: production archive fidelity and communication caller containment. The
retained `tests/tests/platform/test_config_containment.py` remains unchanged
with nine source definitions and eleven collected cases; the pilot does not
satisfy its F06E/F06F retirement gate.

Verification used repository Python, `PYTHONDONTWRITEBYTECODE=1`, `-B`,
`-p no:cacheprovider`, and fresh external Windows-safe `--basetemp` roots:

| Gate | Result |
|---|---|
| Two new F06E communication containment cases | 2 passed |
| Focused containment/import/launcher/runtime/composition/service/config | 179 passed |
| Platform suite | 381 passed, 1 skipped |
| Composition suite | 49 passed |
| Integration suite | 17 passed |
| Full configured `tests/tests` | 1,762 passed, 1 skipped |
| Repository-root collection | 1,763 collected |
| Ruff on the changed Python file | All checks passed |

Collection reconciles exactly as `1,761 + 2 = 1,763`. Quarantining production
source removed no configured test case.

FORTRESS-06E communication production-root quarantine pilot — IMPLEMENTED AND
VERIFIED. F06E and FORTRESS-06 remain IN PROGRESS. F06D remains IN PROGRESS
because the config-containment authority remains intentionally configured.
RAA-003 remains OPEN. No later F06E cluster or F06F/F06G/F06H implementation
started.

---

## 21. FORTRESS-06E Development/Infrastructure/PC-Control Production Quarantine

Date: 2026-09-05. Status: IMPLEMENTED AND VERIFIED.

The controlled slice retired exactly three zero-inbound production roots:
`development/` (7 Python sources), `infrastructure/` (9), and `pc_control/`
(8), totaling 24. The manually resolved cache baseline was mechanically
reverified before movement: exactly these tracked sources, including three
empty `__init__.py` files, and no cache, generated, hidden, untracked,
non-Python, or symlink/reparse artifact in the live roots.

### 21.1 Exact archive and fidelity evidence

| Original source | Production archive | SHA-256 (working bytes) | Git blob |
|---|---|---|---|
| `development/__init__.py` | `legacy_quarantine/production/development/__init__.py.legacy` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `development/build_test_manager.py` | `legacy_quarantine/production/development/build_test_manager.py.legacy` | `06fdfbf986d1b19780849e6838f1d172db6b55c75c0bb3ae866deb14dc2130a3` | `7b639749e046f72b7ed136883624f3df801c3e49` |
| `development/development_workspace_manager.py` | `legacy_quarantine/production/development/development_workspace_manager.py.legacy` | `7d79d7cb5728b37be110d60cb1d8b9466f6227bb2383732ac49a006e9980459f` | `b76b22ddd940ccf2b34b87dcb0a6f2436ed00e2f` |
| `development/git_manager.py` | `legacy_quarantine/production/development/git_manager.py.legacy` | `a2f04a2e1bdcc5e13d2255fa50838c990fa4d2b5de2d684533bf17992e525257` | `ad3fbda7ff8aa614750ae1e6f046ad183211fbde` |
| `development/github_manager.py` | `legacy_quarantine/production/development/github_manager.py.legacy` | `127c256a0efba8bdb82aa52af4741b1ea7aa7c876603b091f31390530028446d` | `51f69adf0f0cfdda9df3282a6fb6757fe36d70d5` |
| `development/repository_manager.py` | `legacy_quarantine/production/development/repository_manager.py.legacy` | `0dc11b690c3f7ffcd2763cf239973d8c0872ee8ff99d3444d469f7fc05e4f5c4` | `bd814f05ab90c0398c66254b46c07b96edb58948` |
| `development/vscode_manager.py` | `legacy_quarantine/production/development/vscode_manager.py.legacy` | `e3a6ff01bf709b8b15c7850f8bba30162463b088b9070cc3f37fa0d9eb9a0401` | `a4a3b4f8ede5e0044df1579e94486cfc42a99221` |
| `infrastructure/__init__.py` | `legacy_quarantine/production/infrastructure/__init__.py.legacy` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `infrastructure/ai_provider_manager.py` | `legacy_quarantine/production/infrastructure/ai_provider_manager.py.legacy` | `07efd3d37b5a4837b8fe34bb33d9400416993c352896b0e0d989a1e74a3142f7` | `b14629f344f4e45160da6a8af602b82d7ec79bd2` |
| `infrastructure/api_intelligence_manager.py` | `legacy_quarantine/production/infrastructure/api_intelligence_manager.py.legacy` | `2ede184c92bdaf1b8a8a66121562fed25462899fa5f9f4d5f5e9fdfbf105fe3a` | `b7a1a49540572714597edfd43b215f34c9f02fb4` |
| `infrastructure/cost_performance_optimizer.py` | `legacy_quarantine/production/infrastructure/cost_performance_optimizer.py.legacy` | `0a09c48ac06f18651c45325d0bd2119539ccc5a0fed7187322bde812283381df` | `bbd23fd3fa6b115d6f31a655b6d693a57c1de501` |
| `infrastructure/database_intelligence.py` | `legacy_quarantine/production/infrastructure/database_intelligence.py.legacy` | `d6ae6833ea8d1b5b825e945b54dab329d51888f8aec8e1316cf23bd8b5835c54` | `b5744255dc054f40e6f3eb4be9083ea3cb4279cc` |
| `infrastructure/infrastructure_intelligence_core.py` | `legacy_quarantine/production/infrastructure/infrastructure_intelligence_core.py.legacy` | `70376a5b24a3bbc98403e2e306f4bc86ffaa0167b55b91a7571bc2899b95ad06` | `3f008fdd954a02520ef45936a543e3637a14a593` |
| `infrastructure/intelligent_resource_orchestrator.py` | `legacy_quarantine/production/infrastructure/intelligent_resource_orchestrator.py.legacy` | `cd0ac6a3632aa160a07d60f8ca7e3373d3dec97f7340f24a445745294b7a354e` | `465aaae65641df53d02b91a096206dbdb665de77` |
| `infrastructure/multi_provider_task_composer.py` | `legacy_quarantine/production/infrastructure/multi_provider_task_composer.py.legacy` | `e570622c0537028fc4f3c7d6dc2e2faf1164d44d87a6b81afb41e199b14db209` | `437cebc9889498d1734f2aeba2e329dc99f71227` |
| `infrastructure/storage_intelligence.py` | `legacy_quarantine/production/infrastructure/storage_intelligence.py.legacy` | `6eb8dcc67cfe0ae4ddc0b6f7015554e1e42834ccd0373a615f44834b93989243` | `0ae20f977b9b0f64cf5d0976ddb17970153bda02` |
| `pc_control/__init__.py` | `legacy_quarantine/production/pc_control/__init__.py.legacy` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `pc_control/application_manager.py` | `legacy_quarantine/production/pc_control/application_manager.py.legacy` | `d77a2a04047212056c837a11ea865ca44565ed2aa6ce8b2ac7d3f7d00cc91c0e` | `804215022857d6e98bc34e5ccb901b9403682101` |
| `pc_control/browser_controller.py` | `legacy_quarantine/production/pc_control/browser_controller.py.legacy` | `cd390fc8b2d5f4ee1f360639bd7a4515799d0bed3e50115f50dcf1ff70cb6e97` | `771bf54ada23504aed7d612cc097451c460b3e2c` |
| `pc_control/file_system_manager.py` | `legacy_quarantine/production/pc_control/file_system_manager.py.legacy` | `f2cc9bc795d4b233dca7dd6f1c5b499d09f51175c42b421521f7b53ec85a8c3f` | `fe32d3bd19e8f9432173f7b1e1f9913f777fb37c` |
| `pc_control/notification_manager.py` | `legacy_quarantine/production/pc_control/notification_manager.py.legacy` | `a4db064b6af39bd96ff7d83720e70788fd5a8b65833e2f78567322b08253aa7b` | `07170c20957ba0bbbb7384b52f53d4de2278b7a2` |
| `pc_control/system_monitor.py` | `legacy_quarantine/production/pc_control/system_monitor.py.legacy` | `dd48ede8aeba5b953c29792c858088e4ed92a0a302dcf7dffb0a56b81178f991` | `cae034fac3af405515c6e587c529b7f484aa0cb2` |
| `pc_control/terminal_controller.py` | `legacy_quarantine/production/pc_control/terminal_controller.py.legacy` | `29c1d5b7b8b0a1df87311d20459358cd30ee8611af42b20a0326926327874aa4` | `485f09d21af144053da8c7dae9a87abe114a37aa` |
| `pc_control/window_manager.py` | `legacy_quarantine/production/pc_control/window_manager.py.legacy` | `d5a9c99b822213b998b688f7a998a1efd3c30ebfa00cb3a83c88277f31f85a89` | `0cbec39e03b321703de8ec79173531dc475fdba4` |

Every archive preserves the original working bytes and SHA-256, and produces
the original HEAD Git blob under both original and archive paths. With
`core.autocrlf=true`, working bytes match HEAD's checkout-filtered bytes;
nonempty raw Git objects use LF while their working copies use CRLF. The
quarantine did not normalize or edit any payload.

All three live roots are absent, including caches. The archives use only
`.py.legacy`, are not Python-importable or pytest-collectable, contain no
importable `__init__.py`, and have no repository Python importer. No wrapper,
stub, forwarding alias, or replacement capability was added. The 24 exact
Git-blob pairs preserve reversible history and R100-equivalent identity;
unstaged source deletions and untracked archives need not display as renames
until a later authorized checkpoint.

### 21.2 Caller, execution, and compatibility boundaries

| Root | Canonical production callers | Legacy production callers | Configured-test callers | Active dynamic load paths | Excluded flat files / direct import statements |
|---|---:|---:|---:|---:|---:|
| `development` | 0 | 0 | 0 | 0 | 7 / 12 |
| `infrastructure` | 0 | 0 | 0 | 0 | 9 / 16 |
| `pc_control` | 0 | 0 | 0 | 0 | 8 / 14 |
| Total | 0 | 0 | 0 | 0 | 24 / 42 |

The exact excluded paths and 42 import statements remain pinned in
`_F06E_SATELLITE_EXCLUDED_IMPORT_STATEMENTS` in
`tests/tests/platform/test_collection_containment.py` as later F06G/F06H debt.
No active compatibility obligation was established. The roots had no imports
of one another. Shared logger and BasePlatformService dependencies did not
constitute inbound canonical reachability.

Static inspection of all 24 sources confirmed LOW-RISK IN-MEMORY disposition:
stored commands, paths, URLs, and descriptions were not executed. No
root-owned persistent/config/runtime-data writer, network/socket/HTTP,
subprocess/shell, process/thread creation, desktop/clipboard/service/registry
mutation, application execution, arbitrary module loading, or path mutation
capability required preservation. Shared logging remained externally
configured; these roots did not configure a persistent writer.

The static canonical closure from `run_jaos.py` remains disjoint. This is
static evidence, not live-runtime certification. `jaos/`, `jaos_platform/`,
`run_jaos.py`, BasePlatformService, and PlatformContract are unchanged.

### 21.3 Containment authority and classification reconciliation

Exactly two grouped cases were added to the existing containment file:
24-source archive fidelity and caller/boundary containment. The prior
live-source requirements for
`development/development_workspace_manager.py`,
`infrastructure/ai_provider_manager.py`, and
`pc_control/application_manager.py` now require their exact archives and
hash/blob evidence. Other live satellite and core/kernel requirements remain.

The canonical import-boundary test had a pre-existing mismatch at `fe2a6c5`:
it expected the communication root in D (D=16/E=3), although the manifest
already classified its production archives as E (D=15/E=4). The authorized
narrow correction updates both exact member sets and counts. Communication,
development, infrastructure, and pc_control are now represented by their
exact production archive patterns in E. D=12, E=7, and the total remains 33.
All unrelated classifications, forbidden-module sets, canonical closure
checks, exact-set checks, and duplicate-classification protection remain.

`tests/tests/platform/test_config_containment.py` remains intentionally
configured and unchanged, with SHA-256
`d862bd601301ae7bfc85aa16a5cc9f31e5f77b23bc54e84689a4276a5a2a447c`,
9 source definitions and 11 cases. Configured legacy-facing remains exactly
1; configured `executive_brain` importers remain 0. Its F06E/F06F writer gate
is unchanged.

### 21.4 Executed verification


All pytest gates use repository Python 3.14.6 with
`PYTHONDONTWRITEBYTECODE=1`, `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, `-B`,
`-p anyio.pytest_plugin -p no:cacheprovider`, and a fresh external
`%TEMP%/jaos-f06e-satellites-<uuid>/pytest` basetemp. The established in-memory
Windows runner changes only restrictive directory creation under that
disposable temp tree to inherit its parent ACL. It leaves no repository helper.

| Gate | Executed result |
|---|---|
| Previously failing manifest/guard contract case | 1 passed |
| Two new production-quarantine cases | 2 passed |
| Full focused set | 150 passed |
| `tests/tests/platform` | 383 passed, 1 skipped |
| `tests/tests/composition` | 49 passed |
| `tests/tests/integration` | 17 passed |
| `tests/tests` | 1,764 passed, 1 skipped |
| `pytest . --collect-only -q` | 1,765 collected |
| Ruff, both changed containment/boundary Python files | PASS |

The focused set comprises the complete collection-containment and canonical
import-boundary files; launcher and banner tests; PlatformRuntime and its
lifecycle tests; PlatformComposition; BasePlatformService; ServiceContainer;
and config containment. No configured test was retired. Exactly two grouped
cases were added: `1,763 + 2 = 1,765`. The single skip is the existing Windows
directory-symlink privilege limitation.

The first full-suite invocation with plugin autoload disabled omitted explicit
AnyIO loading: 17 async tests could not execute (1,747 passed, 1 skipped,
17 warnings). Explicitly loading the installed `anyio.pytest_plugin` corrected
the runner; the two affected files passed all 19 cases and the complete suite
then passed as recorded above. No async test or production behavior changed.

### 21.5 Preserved scope and stop boundary

Only 52 logical task paths are involved: 24 retired sources, 24 archives,
the collection-containment and canonical import-boundary test files, and the
two architecture evidence documents. Protected runtime data, SECURITY.md,
agent/configuration directories, CLAUDE.md, graphify-out, and all unrelated
roots retain their captured hashes. Project-state documents are unchanged.

`dashboard/`, `knowledge/`, `security/`, and `system_services/` remain
pending separate dynamic-path review at that checkpoint; section 22 records
their subsequent approved quarantine. At that checkpoint, `engineering/` remained its separate
dynamic-import-sensitive slice. `workflow/` remains blocked by
`executive_brain.pipeline.executive_pipeline -> workflow.workflow_engine`.
Neither those roots nor core/kernel/Executive/brain/memory/main.py were changed.

F06D, F06E, and FORTRESS-06 remain IN PROGRESS; RAA-003 remains OPEN.
F06F/F06G/F06H and every later slice remain NOT STARTED. The Founder decisions
for main.py and BasePlatformService/PlatformContract remain unresolved.
Step 8 remains blocked, Fortress certification is not started, and major
Phase 8 expansion remains paused. Nothing was staged, committed, or pushed.

---



## 22. FORTRESS-06E Dashboard/Knowledge/Security/System-Services Production Quarantine

Status: **IMPLEMENTED AND VERIFIED**.

### 22.1 Disposition and containment evidence

The separately approved slice continues from HEAD `9dc564f`, after the
communication pilot at `2d2138c` and three-root quarantine at `2fdeadc`.
Exactly 29 tracked sources were retired: dashboard 7, knowledge 7, security 7,
system_services 8. All matched HEAD Git blobs and filtered checkout bytes.
The manually removed caches were absent; no unexpected, hidden, non-Python,
symlink, or reparse-point artifact was present before movement.

All 29 archives preserve raw checkout bytes, SHA-256, size, and Git blob
identity under `legacy_quarantine/production/<original-relative-path>.legacy`.
Original-path and archive-path Git filtering reproduce the same blobs.
These are 29 R100-equivalent moves, reversible through Git history; actual
rename detection awaits a separately authorized checkpoint. Archive payloads
were not edited. The four live roots and caches are absent. No wrapper, stub,
alias, forwarding module, compatibility package, or replacement was added.
Every payload is non-importable/non-collectable `*.py.legacy`; there is no
importable quarantine `__init__.py` or repository Python import from quarantine.

| Root | Canonical production callers | Legacy production callers | Configured-test callers | Direct excluded files / statements | Excluded dynamic registrations |
|---|---:|---:|---:|---:|---:|
| dashboard | 0 | 0 | 0 | 7 / 12 | 1 |
| knowledge | 0 | 0 | 0 | 7 / 12 | 1 |
| security | 0 | 0 | 0 | 7 / 12 | 2 |
| system_services | 0 | 0 | 0 | 8 / 14 | 1 |
| Total | 0 | 0 | 0 | 29 / 50 | 5 |

All five registrations are **EXCLUDED-TEST DEBT ONLY**.
`tests/import_validator_test.py:5-8` registers
`security.permission_manager`, `dashboard.mission_control`,
`system_services.backup_manager`, and `knowledge.knowledge_graph`, then
calls `validate()` at line 10.
`tests/engineering_platform_integration_test.py:46-48` registers
`security.permission_manager` and calls `validate()` at line 105.
Both reach the unchanged
`engineering.import_validator.ImportValidator.validate()`, whose line 34
uses `importlib.import_module(module_path)` for explicitly supplied names.
There is no autodiscovery or production, configured, canonical, or active
runtime/CLI caller.

The shipped `pytest.ini` selects `tests/tests`; `tests/conftest.py`
intentionally excludes the flat executable scripts during configured and root
collection. These paths require explicit legacy invocation. Direct imports
and dynamic registrations span 31 unique excluded files. The unchanged
ProjectStructureValidator retains folder-existence debt through
`tests/project_structure_validator_test.py` and the already-counted engineering
integration script: 32 distinct files including folder debt. These scripts
were neither modified nor executed; all debt remains F06G/F06H.

Static review reconfirms **LOW-RISK IN-MEMORY** for all 29 sources: no implemented
root-owned filesystem/runtime-data/config persistence, network/HTTP/socket
operation, subprocess/shell/process/thread creation, desktop/clipboard/service/
registry mutation, arbitrary module execution, or arbitrary path mutation.
Shared externally configured logging and injected event publication do not
establish root-owned writer authority. There are no cross-imports among the
four roots; outbound shared logger/service contracts do not make them canonical.

The existing collection-containment authority now preserves archives for
`dashboard/mission_control.py`, `knowledge/knowledge_base.py`,
`security/security_monitor.py`, and `system_services/startup_manager.py`.
The four prior whole-root inventory hashes remain exact, reconstructed from
archive bytes under original path identities. Engineering/workflow,
core/kernel/config, canonical, and existing quarantine guards remain enforced.
Exactly two grouped configured cases cover archive fidelity/inertness and
caller/excluded-debt/boundary containment, reusing the existing archive helper.

The manifest and existing canonical guard have exact synchronized membership:
A=10, B=1, D=8, E=11, F=3, TOTAL=33. The four live-root entries leave D and are
represented by their production archive patterns in E. No duplicate or missing
classification exists; all unrelated members and forbidden-import checks are
unchanged. The manifest/guard pair was updated after quarantine verification,
with final synchronized-state verification following the update.

`run_jaos.py`, `jaos/`, and `jaos_platform/` are unchanged. Their static
launcher closure through JAOSApplication, PlatformRuntime/BootManager, and
PlatformComposition remains disjoint from the four roots. This is static
evidence, not live-runtime certification.

`tests/tests/platform/test_config_containment.py` remains
**KEEP TEMPORARILY / INTENTIONALLY CONFIGURED**, SHA-256
`d862bd601301ae7bfc85aa16a5cc9f31e5f77b23bc54e84689a4276a5a2a447c`,
9 definitions / 11 collected cases; configured legacy-facing exactly 1;
configured `executive_brain` importers 0. Its F06E/F06F writer gate and
unauthorized retirement status are unchanged.

### 22.2 Exact source/archive map and fidelity

| Original source | Archive destination | Bytes | SHA-256 (checkout/archive) | Git blob |
|---|---|---:|---|---|
| `dashboard/__init__.py` | `legacy_quarantine/production/dashboard/__init__.py.legacy` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `dashboard/action_timeline.py` | `legacy_quarantine/production/dashboard/action_timeline.py.legacy` | 1130 | `10480d72d139275b1238e2784079375f5888f670038d44e55efdeb7c5740a476` | `c4c537e3a79b8378f921e8a03e2e5292c7c687b9` |
| `dashboard/capability_viewer.py` | `legacy_quarantine/production/dashboard/capability_viewer.py.legacy` | 941 | `e0be93481d37e8f10e18d1e70b2440ee8ae452ba24158e194092cac79a0386db` | `58d2cc7e53120e07be525a39760e8cb02ba22103` |
| `dashboard/mission_control.py` | `legacy_quarantine/production/dashboard/mission_control.py.legacy` | 1045 | `a73958d4944a04f78154836872227b22e1516ff9a6eee7b0f8568f92334d9989` | `b3920709eb0d700dd8eea45d1c861691437d5029` |
| `dashboard/notification_center.py` | `legacy_quarantine/production/dashboard/notification_center.py.legacy` | 1188 | `9ea544bd133670f720493a33ac992af762155ffd7a362761011f9d3c494aa92b` | `8e4b8742f91f075baa4bef609396134f43d3f3dd` |
| `dashboard/platform_status_dashboard.py` | `legacy_quarantine/production/dashboard/platform_status_dashboard.py.legacy` | 911 | `31779d7ea5bd7c2f692dd23ac7dc3294333c1cee7422081ea5a7f39f97945e4d` | `a0237b32d2fef1e4b9106f4cf6895717a1490594` |
| `dashboard/system_health_dashboard.py` | `legacy_quarantine/production/dashboard/system_health_dashboard.py.legacy` | 669 | `c04f683a92c491edf20303d2bd7982adb4866c1ab1b06de486021cb2f69def4f` | `e9c085d56097f060870df66acc56118d37a10140` |
| `knowledge/__init__.py` | `legacy_quarantine/production/knowledge/__init__.py.legacy` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `knowledge/document_manager.py` | `legacy_quarantine/production/knowledge/document_manager.py.legacy` | 789 | `43eda5b09f5d79359a5b712f7b235cf33843d7984c7ac6fdf2ff21f6c6043175` | `619f5f2924f4f08357df9f9388e1c677824544e9` |
| `knowledge/knowledge_base.py` | `legacy_quarantine/production/knowledge/knowledge_base.py.legacy` | 1062 | `ee77f8dae0dcfdbbfd27f659ee59c492f18849376e3e326adfc78c08d4e35db0` | `19e4e41a456080fbf59b66f543a3b52005b2866d` |
| `knowledge/knowledge_graph.py` | `legacy_quarantine/production/knowledge/knowledge_graph.py.legacy` | 841 | `474167d74cddae05211f60b7bd25c8d6318474328899a0da76af88ca21626726` | `cb893f4219b2acf600e8c748992769270ed1ed20` |
| `knowledge/learning_synchronizer.py` | `legacy_quarantine/production/knowledge/learning_synchronizer.py.legacy` | 860 | `e4d208d8819c3756a41869c4c83d46e95ae12a46ac3cae8689fd0c3038ac896e` | `2c7581746f092c428a795bb2924b17513f5474df` |
| `knowledge/ocr_manager.py` | `legacy_quarantine/production/knowledge/ocr_manager.py.legacy` | 793 | `ed713c0a8d3a3a110b8137896c79a74781338ef6b20331e5d48eafd9273e97cc` | `d01852ef87c5da54a7b2a8d5a5901e1b232f1e1c` |
| `knowledge/research_manager.py` | `legacy_quarantine/production/knowledge/research_manager.py.legacy` | 836 | `56ddc816a9a61ceee53df03e3722a1ee9cf558d7daa42746ac5f5f14f4107ef9` | `a50ad601e2a7e20be6a9de8080a33c70bcb0c930` |
| `security/__init__.py` | `legacy_quarantine/production/security/__init__.py.legacy` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `security/audit_logger.py` | `legacy_quarantine/production/security/audit_logger.py.legacy` | 990 | `e2b3da6feee771808c94fcadc45309ed8e74be29c331e3d9879d4cee77656649` | `188ba9ce48cf2ea773bb6a97febc1b88a63f41a0` |
| `security/authentication_manager.py` | `legacy_quarantine/production/security/authentication_manager.py.legacy` | 841 | `e3c09581d762e71e0fb81e41b52b4fcfeb61fc93906ea5b25637fe19d942c2d8` | `35dab4a63e96a68d0d5a34571aac41bc41aff195` |
| `security/authorization_manager.py` | `legacy_quarantine/production/security/authorization_manager.py.legacy` | 762 | `da1f03b10c71b962c199a75b1712e406b36b299958f73ffb470d475d39c1632c` | `5e4758bf6d0fd1fd879619ec3dfb0369a95d4027` |
| `security/identity_manager.py` | `legacy_quarantine/production/security/identity_manager.py.legacy` | 844 | `27183e3775239b6c17f910a19144e595f28c477fe1151d1cc137fb3c607bb4c1` | `060e1ff57c54d6f2236f9433236ff642fded86ab` |
| `security/permission_manager.py` | `legacy_quarantine/production/security/permission_manager.py.legacy` | 951 | `3d6e374399115292e175c696fdaf3fc37211ef472a43aacb30f6380ecbe6160b` | `98cf266fd3906d93ec9016987fcd329b7854bddf` |
| `security/security_monitor.py` | `legacy_quarantine/production/security/security_monitor.py.legacy` | 1101 | `df81267649ba9ca8f00613e37214af45130b58ed8018968b46f12c3e879b244c` | `75f3c2c9ea2ac26da3d4902b6b3fcee81774f5c5` |
| `system_services/__init__.py` | `legacy_quarantine/production/system_services/__init__.py.legacy` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `system_services/backup_manager.py` | `legacy_quarantine/production/system_services/backup_manager.py.legacy` | 820 | `2363a9c574a57420f3a9713b86a3090f7565df272356c320b7d35370979733e7` | `bacee2a048354455599271602adfa36e31ca605f` |
| `system_services/cache_manager.py` | `legacy_quarantine/production/system_services/cache_manager.py.legacy` | 846 | `18208fa63f7371582824891efce046930456e3e3196e993a5bee50e51b77f6a6` | `867751a0ce7c73d594122e619c9acb33116bc2b6` |
| `system_services/cleanup_manager.py` | `legacy_quarantine/production/system_services/cleanup_manager.py.legacy` | 866 | `e21c4506267731644a9e57f5742090bf1c4427282cf558063e76741507ab265a` | `a9fc5bf27009fa49f14ac2b4490231d82a0df3da` |
| `system_services/configuration_manager.py` | `legacy_quarantine/production/system_services/configuration_manager.py.legacy` | 688 | `8d6217b9a2b788792cc34247b71687bd1cd1d0ea579fa96010f8f49a117893f7` | `200a0b9114352833fc8525f563c0c8cabc89a2b6` |
| `system_services/scheduler.py` | `legacy_quarantine/production/system_services/scheduler.py.legacy` | 635 | `179d173bdd2ca70d5470fad407c804350589f261760e7789052e601d1e2a762a` | `e7253b39c6ffc686697957338e7285abfed81ce2` |
| `system_services/startup_manager.py` | `legacy_quarantine/production/system_services/startup_manager.py.legacy` | 1140 | `fa6ce315391ff114aaafe30792ae865b21bc0ba63794e641956a213358f990b0` | `19794eaa15a69d2df5dd168d87f0f561d29bf8ad` |
| `system_services/update_manager.py` | `legacy_quarantine/production/system_services/update_manager.py.legacy` | 818 | `479ba26e1a1e5f2c4b9c1b559da97165c9bd063f6376ad1f5f314d3d1fe4ad7b` | `6066cb60c167c6b33f7d2e4bc7df735ee2759a17` |

### 22.3 Executed verification

All gates exited 0 using `.venv/Scripts/python.exe -B`,
`PYTHONDONTWRITEBYTECODE=1`, `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`,
`-p anyio.pytest_plugin -p no:cacheprovider`, and unique external
`%TEMP%/jaos-f06e-satellites-<uuid>/pytest` basetemp directories.
The established in-memory Windows runner changes restrictive directory creation
only under that disposable tree to inherit its parent ACL. No repository
helper or cache was created.

| Gate (pytest includes `-q`) | Result |
|---|---|
| Two new `test_f06e_dynamic_satellite_*` cases | 2 passed |
| Previous F06D satellite, F06E communication, and F06E three-root cases | 6 passed |
| Full `tests/tests/platform/test_collection_containment.py` | 40 passed |
| Full `tests/tests/platform/test_canonical_import_boundary.py` | 55 passed |
| Integration `test_run_jaos_launcher.py` and `test_run_jaos_banner.py` | 8 passed |
| Platform `test_platform_runtime_lifecycle.py` and `test_platform_runtime.py` | 21 passed |
| Composition `test_platform_composition.py` | 8 passed |
| Platform `test_base_platform_service.py` and `test_service_container.py` | 9 passed |
| Platform `test_config_containment.py` | 11 passed |
| Complete focused set, counting unique cases | 152 passed |
| `tests/tests/platform` | 385 passed, 1 skipped |
| `tests/tests/composition` | 49 passed |
| `tests/tests/integration` | 17 passed |
| `tests/tests` | 1,766 passed, 1 skipped |
| `pytest . --collect-only -q` | 1,767 collected |
| `ruff check --no-cache` on both changed Python test files | PASS |

Exactly two configured cases were added; none retired:
`1,765 + 2 = 1,767`. The skip is the existing Windows directory-symlink
privilege limitation. An initial launcher attempt selected the Windows Python
alias, which lacked pytest and ran no tests; selecting repository Python
corrected the runner without changing test or application behavior.

### 22.4 Preserved scope and stop boundary

The task has exactly 62 logical paths: 29 retired sources, 29 archives, two
existing test files, and two architecture evidence documents. Protected state,
canonical roots, engineering, workflow, project-state documents, and every
path outside that scope retain their pre-task hashes. HEAD remains
`9dc564f`, aligned with origin; the index is empty. Nothing was staged,
committed, or pushed.

At this earlier checkpoint, `engineering/` remained separate for its arbitrary
import validator and non-Python artifact; section 23 records its subsequent
approved retirement. `workflow/` remains blocked by
`executive_brain.pipeline.executive_pipeline -> workflow.workflow_engine`.
No other F06E root or F06F/F06G/F06H slice began. F06D, F06E, and FORTRESS-06
remain IN PROGRESS; RAA-003 remains OPEN. The main.py and
BasePlatformService/PlatformContract Founder dispositions remain unresolved.
Step 8 remains blocked, Fortress certification has not started, and major
Phase 8 expansion remains paused.

---

## 23. FORTRESS-06E Engineering Production-Root Quarantine

FORTRESS-06E engineering production-root quarantine:
IMPLEMENTED AND VERIFIED against the unstaged working tree based on `d8ad3af`.
This records the approved engineering slice; it is not Fortress certification
or live-runtime certification.

### 23.1 Scope and archive fidelity

The slice retired exactly 14 tracked files: 13 Python sources and the empty
historical `engineering/releases/RELEASE_NOTES_v0.9.0-alpha.md` artifact.
The manually removed `engineering/__pycache__/` was absent before movement;
no generated, hidden, untracked, or symlink/reparse artifact accompanied the
tracked baseline. All original files matched HEAD's normalized Git blobs.

Every archive preserves the exact checkout bytes, SHA-256, file size, and
Git-normalized blob. The 12 nonempty Python sources had CRLF checkout bytes
and LF Git blobs; both representations were verified separately. Paths follow
`legacy_quarantine/production/<original-relative-path>.legacy`: 13
`*.py.legacy` archives and one `*.md.legacy` archive. No payload was edited.
The live engineering root and cache are absent. No wrapper, stub, alias,
forwarding package, replacement, or compatibility facade was added.
The 14 source/archive pairs have R100-equivalent identity; Git history
preserves the original sources for reversal. No staging or commit occurred.

The empty release-note artifact is historical preservation, not a current
runtime input. The escaped release-index reference in `docs/README.md` remains
separate documentation-navigation debt; that file was not changed.

| Original path | Archive path | Checkout bytes | Checkout SHA-256 | Git-normalized blob |
|---|---|---:|---|---|
| `engineering/__init__.py` | `legacy_quarantine/production/engineering/__init__.py.legacy` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `engineering/capability_truth_engine.py` | `legacy_quarantine/production/engineering/capability_truth_engine.py.legacy` | 1229 | `8bf1bf8e0e6d142c6538631cc97a99c887fc45419a6f8a56351253ff6d27afc2` | `e909ca3db8fe262d218a3ee8977e905a3dadf8cb` |
| `engineering/configuration_validator.py` | `legacy_quarantine/production/engineering/configuration_validator.py.legacy` | 1088 | `33863a72231b920503cde328770e160dac49c347e298a19dfeb03e6cccc7f852` | `8be30d920d3309a02cc2f855af4811c6cce5029a` |
| `engineering/dependency_validator.py` | `legacy_quarantine/production/engineering/dependency_validator.py.legacy` | 880 | `4700288929eb6ed2c57229412b3354183b54eca9c24b36e7bb77204f403e277c` | `6d5b0d27654a0b637fa72a8095b94caf67eb0d4d` |
| `engineering/engineering_report_generator.py` | `legacy_quarantine/production/engineering/engineering_report_generator.py.legacy` | 1107 | `ee0451839f923fb75998d10a11ccdcbac9dd9cee60cd144eb17bbe1d1aca7d4e` | `15fb94bf179839fd67fcf07fca925597b7a7f470` |
| `engineering/import_validator.py` | `legacy_quarantine/production/engineering/import_validator.py.legacy` | 1108 | `9a79d5c0093bb1eb01cf8f2cce651b4f7aa214b2dd33345bc4d57f5936346a32` | `38e9d2584bd1da71ebe2797dca166384e2595d02` |
| `engineering/integration_test_runner.py` | `legacy_quarantine/production/engineering/integration_test_runner.py.legacy` | 1039 | `9a54364f00f2316a49a4b1e2becdeeb1127c81b9009082b9ff138c8b0abac9d5` | `08c9a2be80d5126fb91d772040852e6c7cf837e7` |
| `engineering/module_registry.py` | `legacy_quarantine/production/engineering/module_registry.py.legacy` | 1084 | `71f1409fab6ab7137ed8db681d65c47389a9ef669074954fa71749c39a23cba1` | `f22524a1c33eef4b6eacae1603791b59db26ed54` |
| `engineering/package_registry.py` | `legacy_quarantine/production/engineering/package_registry.py.legacy` | 820 | `f9a3308ee1a631d61e63b4d0b77e2d7260c7a4bc98595f14cbfde9ce47ba7d18` | `30456374a1a4e748a1eebdde14fde5e027a25a54` |
| `engineering/platform_health_dashboard.py` | `legacy_quarantine/production/engineering/platform_health_dashboard.py.legacy` | 1879 | `9be1bfc29ed0be429faccdece9260dd1f86b7ee8e6a422a99a6f9926a855c998` | `0d8f599fd47c914602b77ff31b1c8997f62bdd0f` |
| `engineering/platform_registry.py` | `legacy_quarantine/production/engineering/platform_registry.py.legacy` | 957 | `a77251a129bfc7710468ea68ba652c11952db7759840302ab01d50821a5eb377` | `af8233ebf94be9d87c87278a84f7d654370f2729` |
| `engineering/project_structure_validator.py` | `legacy_quarantine/production/engineering/project_structure_validator.py.legacy` | 1204 | `d58f00665a0d388e7d7545648b2475d6035b3787ba6571e45fb10f46b627f350` | `e15bd00354790aa2837b436735b18d5488b5d422` |
| `engineering/releases/RELEASE_NOTES_v0.9.0-alpha.md` | `legacy_quarantine/production/engineering/releases/RELEASE_NOTES_v0.9.0-alpha.md.legacy` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `engineering/startup_validator.py` | `legacy_quarantine/production/engineering/startup_validator.py.legacy` | 1693 | `227e30ab2b285bafeaaf61ae14994305bb4b96481ce90e1d6f5a31abcdb3487e` | `25b678c2dd5cecd427453c388a7b26afa8077117` |

### 23.2 Caller, execution, and compatibility disposition

Mechanical repository AST/import scans found zero canonical production,
legacy production, configured-test, and separate non-test script/tool callers
for every engineering module. There is no active CLI/entry-point or runtime
registry dependency and no engineering target in canonical lazy-import maps.
The static `run_jaos.py` -> `JAOSApplication` -> `PlatformRuntime / BootManager`
-> `PlatformComposition` closure remains disjoint: 207 files / 206 modules,
zero violations. No engineering loader or excluded executable script was run.

`ImportValidator` is DYNAMIC-EXECUTION CAPABLE but EXCLUDED-TEST DEBT ONLY.
Its archived `add_import()` stores explicit names in an instance list and
`validate()` calls `importlib.import_module()`; there is no autodiscovery or
registration persistence. Such imports can execute target module bodies, but
no active JAOS path required this capability. Its only callers remain
`tests/import_validator_test.py` and
`tests/engineering_platform_integration_test.py`.

`ProjectStructureValidator` is READ-ONLY FILESYSTEM / LEGACY VALIDATION DEBT:
`Path` construction, path joining, and existence checks only, with no
file-content reads or mutation. Its only excluded callers remain
`tests/project_structure_validator_test.py` and the engineering integration
script. Its stale directory-existence requirements remain F06G/F06H debt.

The exact debt is 13 unique excluded files / 24 direct engineering import
statements: 12 component scripts plus 12 imports in the engineering integration
script. Five explicit dynamic registrations remain pinned:
`tests/import_validator_test.py` lines 5-8 target
`security.permission_manager`, `dashboard.mission_control`,
`system_services.backup_manager`, and `knowledge.knowledge_graph`;
the integration script's registration at line 46 additionally targets
`security.permission_manager`. These scripts remain tracked, unchanged,
excluded from configured and directory-based root collection, and uncalled
by production. They remain F06G/F06H debt, not active compatibility contracts.

No active engineering-owned F06F writer authority was found. There is no
engineering-owned persistent/config/runtime-data writer, network/HTTP/socket
behavior, subprocess, thread/process creation, Git/environment mutation,
desktop/service/registry mutation, or arbitrary path mutation. Shared logging
and injected runtime event publication are externally owned.

Retiring `platform_health_dashboard.py` reduces BasePlatformService's legacy
direct consumers from 3 to 2:
`workflow/workflow_engine.py` and
`executive_brain/memory/memory_manager.py`.
`BasePlatformService`, `PlatformContract`, and `ServiceContainer` are unchanged;
the Founder compatibility disposition remains unresolved for later F06G.

### 23.3 Containment and classification

The existing collection-containment authority was extended with exactly two
grouped cases: 14-file archive fidelity and engineering caller/debt/boundary
containment. The live `engineering/platform_health_dashboard.py` obligation
and exact 14-file retained engineering inventory/hash now use archive evidence.
The existing archive helper preserves nested original paths and the exact
Markdown suffix alongside Python suffixes. Existing source/archive SHA/blob
guards, workflow preservation, and excluded-script guards remain enforced.
The exact five-registration/two-validator debt guard is reused.

The manifest and canonical-boundary guard replace only D entry `engineering/`
with E entry `legacy_quarantine/production/engineering/`, representing all
14 archives. Classification is A=10, B=1, D=7, E=12, F=3, TOTAL=33, with no
duplicate or missing classification and no unrelated membership change.
The forbidden-root guards still include engineering and quarantine.

The seven remaining D entries are `brain/`, `core/`, `executive_brain/`,
`kernel/`, `main.py`, `memory/`, and `workflow/`. Workflow's blocker remains
`executive_brain.pipeline.executive_pipeline -> workflow.workflow_engine`.

`tests/tests/platform/test_config_containment.py` remains unchanged and
INTENTIONALLY CONFIGURED: 9 source definitions / 11 collected cases;
SHA-256 `d862bd601301ae7bfc85aa16a5cc9f31e5f77b23bc54e84689a4276a5a2a447c`.
Configured legacy-facing files remain exactly 1 and configured
`executive_brain` importers remain 0. Config-test retirement is not authorized.

### 23.4 Executed verification

Commands used repository `.venv/Scripts/python.exe -B`,
`PYTHONDONTWRITEBYTECODE=1`, `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`,
`-p no:cacheprovider -p anyio.pytest_plugin`, `-q`, and fresh external
`%TEMP%/jaos-f06e-engineering-<uuid>/pytest` basetemp directories.
The established in-memory Windows shim permits inherited directory ACLs only
inside that disposable tree. No repository runner or cache was created.

| Gate | Executed result |
|---|---|
| New engineering containment cases | 2 passed |
| Relevant earlier containment cases | 8 passed |
| Full collection containment | 42 passed |
| Full canonical import boundary | 55 passed |
| Launcher/banner | 8 passed |
| PlatformRuntime/lifecycle | 21 passed |
| PlatformComposition | 8 passed |
| BasePlatformService/ServiceContainer | 9 passed |
| Config containment | 11 passed |
| Focused union, unique cases | 154 passed |
| `tests/tests/platform` | 387 passed, 1 skipped |
| `tests/tests/composition` | 49 passed |
| `tests/tests/integration` | 17 passed |
| Full configured `tests/tests` | 1,768 passed, 1 skipped |
| `pytest . --collect-only -q` | 1,769 collected |
| Ruff on both changed Python test files | PASS |


No configured test retired. Actual collection reconciles
`1,767 + 2 = 1,769`. Classification metadata was synchronized only after the
initial required regression and collection gates passed, then checked against
the final synchronized files. The preserved skip is the Windows
directory-symlink privilege limitation.

### 23.5 Preservation and remaining gates

The exact logical task scope is 32 paths: 14 retired originals, 14 archives,
two existing test files, and two architecture evidence documents.
Protected state and all paths outside that scope retain their pre-task hashes.
Canonical `run_jaos.py`, `jaos/`, `jaos_platform/`, workflow, every other D
root, and project-state documents are unchanged. HEAD remains `d8ad3af`,
aligned with origin; the index is empty. Nothing was staged, committed, or
pushed.

F06D, F06E, and FORTRESS-06 remain IN PROGRESS; RAA-003 remains OPEN.
No workflow, Executive-family, other D-root, or F06F/F06G/F06H slice began.
The main.py and compatibility-contract Founder decisions remain unresolved.
Step 8 remains blocked, Fortress certification has not started, and major
Phase 8 expansion remains paused.

---

## 24. FORTRESS-06E Kernel Production-Root Quarantine

Status: IMPLEMENTED AND VERIFIED

Baseline: `d240a66` on `phase8-ai-intelligence`. This checkpoint is
unstaged and uncommitted. The approved slice retired exactly 12 tracked Python
sources from `kernel/`; the manually cleared kernel cache was absent before
movement. All sources matched HEAD, with checkout SHA-256, sizes, and
Git-normalized blobs captured before movement.

The 12 R100-equivalent source/archive pairs preserve checkout bytes, SHA-256,
file sizes, and Git-normalized blob identity. Archives retain each original
relative path below `legacy_quarantine/production/` and end in `.py.legacy`.
The live kernel root and its cache are absent. No archive payload was edited,
and no wrapper, stub, alias, forwarding module, or replacement capability was
added. No importable `__init__.py` exists under quarantine; the archives are
non-importable and non-collectable, with no repository Python import or
literal dynamic import from quarantine. Git history retains the originals
for reversal; no staging was used to obtain rename evidence.

Canonical production callers, remaining legacy production callers,
configured-test callers, and separate script/tool callers are all zero.
The exact 11 excluded flat scripts / 18 direct imports remain unchanged as
F06G/F06H debt. They are excluded by `tests/conftest.py` from directory-based
collection, and are outside `pytest.ini`'s configured `tests/tests` tree.
No runtime-active dynamic loader or entry-point obligation was found.

This removes the live shadow lifecycle, boot, context, permission, and
service-registry stack. The old `JAOSKernel` construction of
`PlatformRuntime` did not establish canonical runtime ownership. Static
inspection found no kernel-owned persistent runtime/config/data writer or
network/process/desktop implementation. Shared logging and runtime-event
publication remain externally owned. No kernel behavior was executed.

The existing collection authority gained exactly two grouped cases:
12-source archive fidelity/non-importability, and caller/debt/canonical/config
containment. Its two earlier `kernel/jaos_kernel.py` live-source obligations
now require exact kernel archive fidelity. Core/config/main requirements
remain, with explicit live `core/kernel.py` preservation. Exact source
inventory hashes also preserve `executive_brain/` and `workflow/`, while
all earlier quarantine and forbidden-import guards remain intact.

Exact classification is now A=10 / B=1 / D=6 / E=13 / F=3, total 33.
`kernel/` leaves D and is represented by
`legacy_quarantine/production/kernel/` in E. The existing separate
`kernel/jaos_kernel_backup.py` E entry is relocated to
`legacy_quarantine/production/kernel/jaos_kernel_backup.py.legacy`.
The file-specific refinement is preserved without adding or dropping an
unrelated classification. The manifest summary's stale D=8/E=11 integers are
corrected to D=6/E=13; the exact pre-slice membership was D=7/E=12.

The six remaining D entries are `brain/`, `core/`, `executive_brain/`,
`main.py`, `memory/`, and `workflow/`. `core/kernel.py` remains untouched
and still imports `executive_brain.managers.registry_manager`.
ExecutiveBrain and workflow are untouched. Workflow remains blocked by
`executive_brain.pipeline.executive_pipeline -> workflow.workflow_engine`.

Canonical `run_jaos.py`, `jaos/`, and `jaos_platform/` are unchanged.
The static launcher closure remains disjoint from kernel; this is not live
runtime certification. `tests/tests/platform/test_config_containment.py`
remains KEEP TEMPORARILY / INTENTIONALLY CONFIGURED, with 9 definitions and
11 passing cases; SHA-256
`d862bd601301ae7bfc85aa16a5cc9f31e5f77b23bc54e84689a4276a5a2a447c`.
Configured legacy-facing files remain 1 and Executive importers remain 0.
Config-test retirement remains unauthorized.

Verification used repository `.venv/Scripts/python.exe -B -` with an
in-memory pytest runner, `PYTHONDONTWRITEBYTECODE=1`,
`PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, `-p no:cacheprovider`,
`-p anyio.pytest_plugin`, and fresh external
`%TEMP%/jaos-f06e-kernel-<uuid>/pytest` basetemp roots. The established Windows
mkdir shim permits inherited ACLs only inside each disposable external tree.
The runner prepends the repository interpreter directory to child PATH.
No repository runner was created. All listed test commands exited 0.

| Gate | Executed result |
|---|---|
| New kernel containment cases | 2 passed |
| Relevant earlier containment cases | 10 passed |
| Full collection containment | 44 passed |
| Full canonical import boundary | 55 passed |
| Launcher/banner | 8 passed |
| PlatformRuntime/lifecycle | 21 passed |
| PlatformComposition | 8 passed |
| BasePlatformService/ServiceContainer | 9 passed |
| Config containment | 11 passed |
| Focused union, unique cases | 156 passed |
| `tests/tests/platform` | 389 passed, 1 skipped |
| `tests/tests/composition` | 49 passed |
| `tests/tests/integration` | 17 passed |
| Full configured `tests/tests` | 1,770 passed, 1 skipped |
| `pytest . --collect-only -q` | 1,771 collected |
| Ruff on both changed Python test files | PASS |

No configured case retired. Actual root collection reconciles
`1,769 + 2 = 1,771`. The preserved skip is the Windows directory-symlink
privilege limitation. Classification metadata was synchronized only after the
initial required regression and collection gates passed, following the
engineering checkpoint's evidence order. The synchronized manifest and exact
boundary guard then passed all 55 import-boundary cases plus the two new kernel
cases (57 passed, exit 0); final Ruff and static membership/fidelity checks
also passed.

The authorized logical scope is 28 paths: 12 retired originals, 12 archives,
two existing test files, and two architecture documents. Protected state and
all out-of-scope file hashes match the pre-task baseline. Existing unrelated
modified/untracked work is preserved. Project-state documents, other legacy
roots, core/Executive caches, and canonical contracts are unchanged.

F06D, F06E, and FORTRESS-06 remain IN PROGRESS; RAA-003 remains OPEN.
F06F/F06G/F06H and later slices have not started. Founder decisions remain
unresolved. Step 8 remains blocked, Fortress certification has not started,
and major Phase 8 expansion remains paused. Nothing was staged, committed,
or pushed.

### 24.1 Exact source/archive fidelity

| Original | Archive | Checkout bytes | Checkout SHA-256 | Git-normalized blob |
|---|---|---:|---|---|
| `kernel/__init__.py` | `legacy_quarantine/production/kernel/__init__.py.legacy` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `kernel/boot_manager.py` | `legacy_quarantine/production/kernel/boot_manager.py.legacy` | 480 | `89f5b35b87f5a5e5dddf1e71417d621da244327f62913e3a535c19ae4fe23b21` | `46399e1672240c9e6b4252112ddcf92271abb128` |
| `kernel/boot_phase_manager.py` | `legacy_quarantine/production/kernel/boot_phase_manager.py.legacy` | 1199 | `4118d489075afa66085af5166d00b98e5701f66b17b0fa17d1e0f2ab359783b1` | `d472f5138f243df0fa992834eb2281f92a890ba4` |
| `kernel/jaos_kernel.py` | `legacy_quarantine/production/kernel/jaos_kernel.py.legacy` | 1573 | `9c14d736618909758464687aa8504dfb915f8b246c9c916cb9992ccd2ab54f49` | `d3aa4c707b77b48bdf8d2d53a4a1eabd88166bea` |
| `kernel/jaos_kernel_backup.py` | `legacy_quarantine/production/kernel/jaos_kernel_backup.py.legacy` | 1191 | `04c634467a013a1a7aba8dd1b66797004077beafb38d2b625f5b0660ca625f26` | `26cb19d979951c8c13589ac740e7e17142b07dcc` |
| `kernel/kernel_event_bus.py` | `legacy_quarantine/production/kernel/kernel_event_bus.py.legacy` | 815 | `637eedc0c42c16592588f9e8111b5a78ee35969083fbae6ad0f21c1e0f71ce1c` | `091db8640403011a38bcb0033da4796504196180` |
| `kernel/kernel_health_monitor.py` | `legacy_quarantine/production/kernel/kernel_health_monitor.py.legacy` | 1061 | `7a0440edfeaac853872a151c8f15ebf9d54de46d49ea5f5f6cbaddc82c44e2b1` | `b5def8556b47130f1a1c4efdf509ce10c9b8f2ee` |
| `kernel/kernel_lifecycle_manager.py` | `legacy_quarantine/production/kernel/kernel_lifecycle_manager.py.legacy` | 1235 | `8e80ac58805523df6ae4ea16979cb32505394bede15ac3cca82f8f22253cc9e2` | `cb9af0d1f15140b42bb1badcbb9a78083b07f6ac` |
| `kernel/kernel_permission_gateway.py` | `legacy_quarantine/production/kernel/kernel_permission_gateway.py.legacy` | 1040 | `0cf8d18024bda6e385c91c215f5f772fa2fa6b133e8fba660536ce9e13c6d7c3` | `8cb8845237e9fa4abe620746f31dc863e85bcd1c` |
| `kernel/kernel_router.py` | `legacy_quarantine/production/kernel/kernel_router.py.legacy` | 882 | `3dcd6c1deedebe73900b271f53978a634a41ef9ffd7a321bdc57a488b8c4f4c7` | `893d63d939770b630f2e94f43d930400f2f6d5e1` |
| `kernel/kernel_service_registry.py` | `legacy_quarantine/production/kernel/kernel_service_registry.py.legacy` | 628 | `a09ef7f7ebb6650255e1e3f0f0e66220adf6dad1f69a60f48206efa20300705a` | `665e42e331b642ca9ff7f3be4300873af3dda33e` |
| `kernel/runtime_context.py` | `legacy_quarantine/production/kernel/runtime_context.py.legacy` | 945 | `d3df9aea50620c7f956666be55cf7261edd84d3a727fb917329d3f9b7727d110` | `f855d6c38c95c3c502bb840bab71902a455f68b8` |

### 24.2 Exact excluded import debt

| Excluded script | Direct kernel module imports |
|---|---|
| `tests/boot_manager_test.py` | `kernel.boot_manager` |
| `tests/boot_phase_manager_test.py` | `kernel.boot_phase_manager` |
| `tests/jaos_kernel_test.py` | `kernel.jaos_kernel` |
| `tests/kernel_event_bus_test.py` | `kernel.kernel_event_bus` |
| `tests/kernel_health_monitor_test.py` | `kernel.kernel_health_monitor` |
| `tests/kernel_integration_test.py` | `kernel.jaos_kernel`, `kernel.kernel_event_bus`, `kernel.kernel_health_monitor`, `kernel.kernel_lifecycle_manager`, `kernel.kernel_permission_gateway`, `kernel.kernel_router`, `kernel.kernel_service_registry`, `kernel.runtime_context` |
| `tests/kernel_lifecycle_manager_test.py` | `kernel.kernel_lifecycle_manager` |
| `tests/kernel_permission_gateway_test.py` | `kernel.kernel_permission_gateway` |
| `tests/kernel_router_test.py` | `kernel.kernel_router` |
| `tests/kernel_service_registry_test.py` | `kernel.kernel_service_registry` |
| `tests/runtime_context_test.py` | `kernel.runtime_context` |

---

## 25. FORTRESS-06E core/kernel.py Production-Leaf Quarantine

Historical checkpoint: the 91-source Executive inventory below predates the
AI/provider family retirement recorded in section 26.

Status: IMPLEMENTED AND VERIFIED

Baseline: `3247c0d` on `phase8-ai-intelligence`, aligned with origin.
This implementation checkpoint is unstaged and uncommitted. It retires only
`core/kernel.py`; it does not retire the `core/` root.

The original was tracked and matched HEAD: 1,888 checkout bytes, 79 CRLF line
endings and no bare LF, SHA-256
`12614a613c9156be0dee4aaab6630e161efd04f49b169ce97d27e321086fa86f`,
Git-normalized blob `7c56418aa60b29dbecaa00f35abeadf70ee65fa9`.
Its exact destination is
`legacy_quarantine/production/core/kernel.py.legacy`. Checkout bytes, SHA-256,
size, line-ending representation, and normalized blob identity are preserved.
This is one R100-equivalent move, reversible through Git history; no archive
payload was edited.

The live leaf and associated `core/__pycache__/kernel.cpython-314.pyc` are
absent. Other core cache artifacts were not removed. The other 34 core Python
sources and `main.py` are unchanged. No wrapper, stub, alias, forwarding
module, or replacement capability was added. The archive is non-importable
and non-collectable; no quarantine `__init__.py` or repository Python import
from `legacy_quarantine` was introduced.

Canonical production, remaining legacy production, configured-test, excluded
direct, and separate script/tool callers of `core.kernel` are all zero.
Static canonical launcher closure (207 files) and the legacy `main.py`
closure (31 files, including `core.engine`) do not reach this leaf. These are
static findings, not live-runtime certification. The source owns no persistent
runtime-data, config, checkpoint, JSON, network, subprocess, or filesystem
writer requiring F06F treatment; this finding applies only to the retired leaf.

Before retirement, the leaf imported
`executive_brain.managers.registry_manager.RegistryManager` at module import
time, but constructed it only inside `JAOSKernel.boot()`. Removing this
uncalled leaf removed RegistryManager's sole external-root production importer:
**1 -> 0**. Its six Executive internal importers remain unchanged; RegistryManager
itself is not declared independently removable.

The existing source-classification model continues to classify `core/` as D.
Its row now records PARTIAL ROOT DISPOSITION and links this archived leaf to
the slice evidence. No independent category-E member was added for the leaf.
Exact membership remains A=10 / B=1 / D=6 / E=13 / F=3, total 33, with no
duplicate, missing, or changed classification member. The six D entries remain
`brain/`, `core/`, `executive_brain/`, `main.py`, `memory/`, and `workflow/`.
`test_canonical_import_boundary.py` required no modification.

The existing collection-containment authority now handles explicitly archived
leaves within live roots while preserving root-absence checks for earlier
whole-root slices. Two former live-leaf obligations and the retained
`core/kernel.py` inventory/hash guard now require archive fidelity. Exactly
two grouped cases were added: archive fidelity and caller/dependency
containment. All other core, canonical, Executive, workflow, config, and
previous-quarantine guards remain.

`test_config_containment.py` remains KEEP TEMPORARILY / INTENTIONALLY
CONFIGURED, unchanged at SHA-256
`d862bd601301ae7bfc85aa16a5cc9f31e5f77b23bc54e84689a4276a5a2a447c`,
9 source definitions and 11 collected/passing cases. Configured legacy-facing
files remain 1 and configured `executive_brain` importers remain 0. Retirement
of that test and the `main.py -> core.engine -> core.config_manager` writer
boundary remains unauthorized.

Verification used repository `.venv/Scripts/python.exe -B -` with the
established in-memory pytest runner, `PYTHONDONTWRITEBYTECODE=1`,
`PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, `-p no:cacheprovider`,
`-p anyio.pytest_plugin`, and a fresh external
`%TEMP%/jaos-f06e-core-leaf-<uuid>/pytest` basetemp with inherited Windows ACLs.

| Executed verification | Result |
|---|---|
| Two new leaf cases | 2 passed |
| Relevant existing containment: `-k "f06d_satellite_retirement or f06d_core_kernel or f06e_kernel"` | 5 passed, 41 deselected |
| Full `test_collection_containment.py` | 46 passed |
| Full `test_canonical_import_boundary.py` | 55 passed |
| Launcher/banner | 8 passed |
| PlatformRuntime/lifecycle | 21 passed |
| PlatformComposition | 8 passed |
| BasePlatformService/ServiceContainer | 9 passed |
| Config containment | 11 passed |
| Unique focused coverage across separate runs | 158 passed |
| `tests/tests/platform` | 391 passed, 1 skipped |
| `tests/tests/composition` | 49 passed |
| `tests/tests/integration` | 17 passed |
| Full configured `tests/tests` | 1,772 passed, 1 skipped |
| `pytest . --collect-only -q` | 1,773 collected |
| Final Ruff on the changed Python test file | PASS |

All pytest gates exited 0. No configured case retired; actual collection is
`1,771 + 2 = 1,773`. Ruff initially reported SIM102 in a new nested condition;
combining the same predicates resolved it. Final Ruff exited 0, and both new
cases then passed again (2 passed, exit 0). No production behavior changed
during that lint correction.

Canonical `run_jaos.py`, `jaos/`, and `jaos_platform/` are unchanged, as are
all 91 Executive sources and all nine workflow sources. Workflow is still
blocked by `executive_brain.pipeline.executive_pipeline -> workflow.workflow_engine`;
this leaf retirement does not unblock it. The planned Executive order remains
AI/provider 13 sources, tools 42, remaining family 36. None of those slices has
started. Writer-sensitive remaining `core/`, `brain/`, `memory/`, and
`main.py` retain their F06F gates; Founder compatibility decisions remain open.

F06D, F06E, and FORTRESS-06 remain IN PROGRESS; RAA-003 remains OPEN.
F06F/F06G/F06H and later work have not started. Step 8 remains blocked, Fortress
certification has not started, and major Phase 8 expansion remains paused.
Protected hashes and out-of-scope state match the baseline. The task covers
five logical paths: one original, one archive, one containment file, and these
two architecture documents. Project-state documents remain untouched.

### 25.1 Exact source/archive baseline

| Field | Verified value |
|---|---|
| Original | `core/kernel.py` |
| Archive | `legacy_quarantine/production/core/kernel.py.legacy` |
| Checkout size | 1,888 bytes |
| Checkout line endings | 79 CRLF; 0 bare LF |
| Checkout SHA-256 | `12614a613c9156be0dee4aaab6630e161efd04f49b169ce97d27e321086fa86f` |
| Git-normalized blob | `7c56418aa60b29dbecaa00f35abeadf70ee65fa9` |

### 25.2 Preserved RegistryManager internal importers

Each file retains one direct import; all six remain inside ExecutiveBrain:

- `executive_brain/brain/executive_brain.py`
- `executive_brain/managers/decision_manager.py`
- `executive_brain/managers/execution_manager.py`
- `executive_brain/managers/mission_manager.py`
- `executive_brain/managers/planning_manager.py`
- `executive_brain/managers/result_manager.py`

The pre-slice external-root edge was `core/kernel.py:22` to RegistryManager;
construction occurred at line 47 inside `JAOSKernel.boot()`. That external
edge is removed; these internal dependencies remain.

---

## 26. FORTRESS-06E Executive AI/Provider Production-Family Quarantine

Historical implementation-time record: the following 78-source state and
unstarted tools slice predate section 27. Preserve this checkpoint evidence.

Date: 2026-09-23. Status: **IMPLEMENTED AND VERIFIED** in the uncommitted
working tree based on `0627453` on `phase8-ai-intelligence`; HEAD and origin
remain aligned. This is the separately authorized FORTRESS-06E executive_brain
AI/provider production-family quarantine, not completion of F06E or live-runtime
certification.

The pre-move inventory contained exactly 13 tracked Python sources, all present
in HEAD and matching their Git-normalized blobs. Checkout SHA-256, byte size,
and CRLF representation were captured before mutation. The four family caches
(`ai/__pycache__`, `ai/prompt/__pycache__`, `ai/providers/__pycache__`, and
`ai/routing/__pycache__`, all under `executive_brain/`) were absent before and
after the move. No tracked non-Python source, hidden entry, symlink/reparse
point, unexpected untracked artifact, cache, or pyc was present in the family.

All 13 sources moved to `legacy_quarantine/production/executive_brain/ai/`
with `.py.legacy` suffixes. Exact checkout bytes, SHA-256, sizes, line endings,
and Git-normalized blob IDs are preserved. Archive payloads were not edited.
The live `executive_brain/ai/` family is absent, with no wrapper, stub, alias,
or replacement. Archives are non-importable and non-collectable; no quarantine
`__init__.py` or repository Python import from quarantine exists. Git history
preserves reversibility. A read-only `git diff --no-index --name-status
--find-renames=100% --rename-empty` comparison of external before/after trees
reported all 13 mappings as R100 without staging.

AST analysis of repository Python, resolving relative imports and checking
literal dynamic imports, found zero canonical production callers, zero
external remaining legacy production callers, zero configured-test callers,
zero excluded direct callers, and zero separate script/tool callers. No
remaining Executive source or workflow/core/brain/memory/main.py source imports
the family. Before retirement, 11 family-directed import statements in six
family consumers were internal to the 13-source slice and retired together.
The adapters' outbound `config.ai_config` type dependencies did not constitute
outside callers; configuration remains untouched.

Static side-effect review confirmed real Ollama HTTP health/generation, OpenAI
HTTP generation and environment-variable reads, ProviderManager dispatch, and
LLMRouter routing. Their active outside-family production owner/caller count
was zero. No family-owned persistent runtime-data/config/checkpoint/JSON-state
writer, subprocess/shell execution, filesystem mutation requiring F06F, or
environment mutation was found. Environment reads are not mutations. No
OpenAI/Ollama network or provider behavior was executed.

ADR-0014 supersession remains authoritative: the exact legacy OpenAI/Ollama
adapters and APIs are not canonical provider authority, and the legacy manager
does not own canonical `ProviderManager`/`AIManager`. Canonical
`PlatformComposition` -> `ProviderManager`/`AIManager` -> provider abstractions
-> deterministic `MockProvider` is preserved. All three configured canonical
contract cases passed: blank/whitespace request rejection, invalid manager
input rejected before provider execution, and generation failure mapped to
`ProviderManagerError` with truthful failure metrics/state. No provider-specific
compatibility behavior was retained or redesigned. F09 owns future concrete
provider resilience and remains NOT STARTED.

`executive_brain/` remains a live category D root: 91 - 13 = **78** sources,
comprising **42 tools + 36 remaining non-tools** sources. Their checkout-byte
inventory is preserved. The reviewed order remains AI/provider (this slice),
tools (not started), then remaining Executive (not started). RegistryManager
has zero external-root callers and the same six internal Executive callers.
All nine workflow sources are unchanged; the blocker
`executive_brain.pipeline.executive_pipeline -> workflow.workflow_engine`
remains and workflow is not unblocked.

Exactly two grouped configured cases were added to
`tests/tests/platform/test_collection_containment.py`: archive fidelity and
caller/provider/dependency containment. Earlier provider-presence checks now
verify the exact archived payloads. Earlier 91-source Executive inventory checks
reconstruct the original digest using 78 live sources plus 13 archived payloads,
preserving historical evidence rather than replacing it with a weaker count.
The canonical-boundary file required no change. Classification remains
**A=10, B=1, D=6, E=13, F=3, TOTAL=33**; this partial-root disposition adds no
top-level E entry.

Static launcher closure analyzed 207 files / 206 reached modules with no
violations and no `executive_brain.ai` reachability. Canonical lazy-map string
targets contain no retired-family target. Canonical `run_jaos.py`, `jaos/`, and
`jaos_platform/` are unchanged. This static evidence does not certify a live
runtime. Config containment is unchanged: SHA-256
`d862bd601301ae7bfc85aa16a5cc9f31e5f77b23bc54e84689a4276a5a2a447c`,
nine definitions / eleven collected cases, one configured legacy-facing file,
and zero configured Executive importers. Config retirement remains unauthorized.

Verification used repository `.venv/Scripts/python.exe -B` with
`PYTHONDONTWRITEBYTECODE=1`, `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`,
`-p no:cacheprovider`, `-p anyio.pytest_plugin`, and unique external
`%TEMP%/jaos-f06e-executive-ai-<uuid>/pytest` basetemp roots. The established
Windows runner shim changed `os.mkdir` mode only inside each disposable
external tree to inherit its parent ACL. It changed no repository helper,
fixture, production behavior, or test assertion.

The exact command prefix was
`.venv/Scripts/python.exe -B %TEMP%/jaos_f06e_executive_ai_20260923/runner.py`;
the external runner passed the above flags and each row's arguments to
`pytest.main`. All pytest gates exited 0, with no failures or reported warnings.

| Arguments / verification, in executed order | Result |
|---|---|
| `tests/tests/platform/test_collection_containment.py -k f06e_executive_ai -q` | 2 passed, 46 deselected |
| `tests/tests/platform/test_collection_containment.py -k "f06d1 or f06d2d_deferred_provider or f06d_provider or f06d_memory_retirement" -q` | 5 passed, 43 deselected |
| `tests/tests/ai/test_canonical_provider_contract.py -q` | 3 passed |
| `tests/tests/platform/test_collection_containment.py -q` | 48 passed |
| `tests/tests/platform/test_canonical_import_boundary.py -q` | 55 passed |
| `tests/tests/integration/test_run_jaos_launcher.py tests/tests/integration/test_run_jaos_banner.py -q` | 8 passed |
| `tests/tests/platform/test_platform_runtime.py tests/tests/platform/test_platform_runtime_lifecycle.py -q` | 21 passed |
| `tests/tests/composition/test_platform_composition.py -q` | 8 passed |
| `tests/tests/platform/test_base_platform_service.py tests/tests/platform/test_service_container.py -q` | 9 passed |
| `tests/tests/platform/test_config_containment.py -q` | 11 passed |
| `tests/tests/platform -q` | 393 passed, 1 skipped |
| `tests/tests/composition -q` | 49 passed |
| `tests/tests/integration -q` | 17 passed |
| `tests/tests -q` | 1,774 passed, 1 skipped |
| `. --collect-only -q` | 1,775 collected |
| `.venv/Scripts/python.exe -B -m ruff check tests/tests/platform/test_collection_containment.py` | PASS, exit 0 |

Unique focused coverage is 163 passing cases; narrower containment runs are
subsets and are not counted twice. No configured case was retired. The actual
collection reconciliation is **1,773 + 2 = 1,775**, with 1,774 passing and the
one existing skip in the full configured suite.

Protected baseline hashes and all outside-scope files remain unchanged,
including SECURITY.md, the seven named data files, `.agents/`, `.claude/`,
`.codex/`, `.context-bridge/`, CLAUDE.md, graphify-out/, and project-state docs.
No Graphify operation ran. Task scope is exactly **29 logical paths**: 13
originals, 13 archives, one containment test, and these two architecture docs.
The rename-aware task view is **13 R100 + 3 M**. Ordinary unstaged Git output
shows source deletions and untracked archives because the index remains empty.
`git diff --check` passed. HEAD remains `0627453`, aligned with origin; nothing
was staged, committed, or pushed.

RAA-003 remains OPEN; F06E and FORTRESS-06 remain IN PROGRESS. F06F/F06G/F06H,
F09, the tools slice, and the remaining Executive slice have not started.
Step 8 remains blocked, Fortress certification has not started, and major
Phase 8 expansion remains paused. This slice is ready for an atomic checkpoint;
checkpoint execution was not authorized in this task.

### 26.1 Exact 13-source archive inventory

Every source below was tracked and present in `0627453`. Empty package markers
have zero bytes; every nonempty payload uses CRLF only (zero bare LF/CR).

| Original source | Exact archive | Bytes | CRLF | Checkout SHA-256 | Git-normalized blob |
|---|---|---:|---:|---|---|
| `executive_brain/ai/__init__.py` | `legacy_quarantine/production/executive_brain/ai/__init__.py.legacy` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `executive_brain/ai/prompt/__init__.py` | `legacy_quarantine/production/executive_brain/ai/prompt/__init__.py.legacy` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `executive_brain/ai/prompt/prompt_engine.py` | `legacy_quarantine/production/executive_brain/ai/prompt/prompt_engine.py.legacy` | 2276 | 73 | `1424acfe1dd56b959cb848ed9e986235c02e8b353a906e2a931b9d0e303bac51` | `c8d2e25717e88b244ce4d77421ad4f559313663f` |
| `executive_brain/ai/prompt/prompt_models.py` | `legacy_quarantine/production/executive_brain/ai/prompt/prompt_models.py.legacy` | 883 | 50 | `11f8f8293b3af59c7175570ce507b1ace1aa2616506f870f4979c2c2ddc5381a` | `3c83332640dd4caff851095d60a5d4e415518782` |
| `executive_brain/ai/providers/__init__.py` | `legacy_quarantine/production/executive_brain/ai/providers/__init__.py.legacy` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `executive_brain/ai/providers/ai_provider_exceptions.py` | `legacy_quarantine/production/executive_brain/ai/providers/ai_provider_exceptions.py.legacy` | 495 | 24 | `09ed65a45fbbe6ee965b09ae1f9c167af5acb88bfbd7f52083d062cd1d2a1e72` | `b048a757e8ad282194096ba6aa609415524c392a` |
| `executive_brain/ai/providers/ai_provider_interface.py` | `legacy_quarantine/production/executive_brain/ai/providers/ai_provider_interface.py.legacy` | 1046 | 48 | `fa6d2d0b6bb453c0189b840573d4957e5e284e2f6f3d6c5c431a37c30128a5d3` | `c6ba37a7809bd51fc549f4aa87ac465c75fb23cb` |
| `executive_brain/ai/providers/ai_provider_manager.py` | `legacy_quarantine/production/executive_brain/ai/providers/ai_provider_manager.py.legacy` | 2920 | 87 | `7f1125e41a5379e42daffc7d9bd360ad2e0f0db09a4a390c17781b257c7a0618` | `c1b2ca6103c352aaab8f6748cac1dc9116e8e13a` |
| `executive_brain/ai/providers/ai_provider_models.py` | `legacy_quarantine/production/executive_brain/ai/providers/ai_provider_models.py.legacy` | 1028 | 47 | `5b3e4011f8350c8a7dcee9069c9681bab3f694af5c3464c09bb2a85fba1fee54` | `6810938055892b0e72f09473f481b520c73ad1eb` |
| `executive_brain/ai/providers/ollama_provider.py` | `legacy_quarantine/production/executive_brain/ai/providers/ollama_provider.py.legacy` | 3763 | 131 | `51a18d7db6c99646f5905a617b6b8f11543d2f2037de8ea504d0c24aaf46cbb0` | `95144406d1b48487f7af6ebf82c6f5ca80653261` |
| `executive_brain/ai/providers/openai_provider.py` | `legacy_quarantine/production/executive_brain/ai/providers/openai_provider.py.legacy` | 4236 | 146 | `c1a42f8585db3edc84b26735eb4b41e7680ff8a58531596bb608dcf67a10596d` | `bfb0ee10589c054903e214d69285afb8dc8a242f` |
| `executive_brain/ai/routing/__init__.py` | `legacy_quarantine/production/executive_brain/ai/routing/__init__.py.legacy` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `executive_brain/ai/routing/llm_router.py` | `legacy_quarantine/production/executive_brain/ai/routing/llm_router.py.legacy` | 1337 | 46 | `e166501f63aad131377883964664efdf8a2ba30a23d9bcb445f053be1e7305e4` | `cd46a08e075da86f10a9002337b4cc8f474a2349` |

---

## 27. FORTRESS-06E Executive Tools Production-Family Quarantine

Date: 2026-09-23. Status: **IMPLEMENTED AND VERIFIED** in the uncommitted
working tree based on `c38564b` (`phase8-ai-intelligence`), aligned with origin.
The previous AI/provider implementation is committed at `9622619`; its
project-state synchronization is committed at `c38564b`. This section records
only the separately authorized tools-family retirement, not completion of F06E
or live-runtime certification.

The fresh gate verified exactly the requested **42 tracked Python sources**,
all present in HEAD and matching their Git-normalized blobs. Checkout SHA-256,
size and line-ending representation were captured for each source before
movement. All seven caches were absent before and after retirement:
`__pycache__`, `browser/__pycache__`, `core/__pycache__`,
`development/__pycache__`, `development/vscode/__pycache__`,
`file/__pycache__`, and `windows/__pycache__`, each beneath
`executive_brain/tools/`. There was no tracked non-Python file, hidden entry,
symlink/reparse point, unexpected untracked artifact, or `*.pyc` in the family.

All 42 sources moved byte-identically to
`legacy_quarantine/production/executive_brain/tools/<relative-path>.legacy`,
preserving the complete hierarchy and `.py.legacy` suffixes. Every archive
matches the captured checkout bytes, SHA-256, size, CRLF representation and
Git-normalized blob; no archive payload was edited. The live tools family is
absent, without wrapper, stub, alias, or replacement. Archives are
non-importable and non-collectable; there is no quarantine `__init__.py` or
repository Python import from quarantine. Git history preserves reversibility.
A read-only external before/after comparison using
`git diff --no-index --name-status --find-renames=100% --rename-empty`
reported **42 R100** mappings without staging.

Repository-wide AST analysis, including relative imports and literal dynamic
imports, found **0 canonical production callers, 0 external remaining legacy
production callers, 0 configured-test callers, 0 excluded direct callers, and
0 separate script/tool callers**. Every one of the 42 sources was adjudicated.
No remaining Executive source or `workflow/`, `core/`, `brain/`,
`memory/`, `main.py`, `run_jaos.py`, `jaos/`, or `jaos_platform/`
caller reaches the family. Its **57 internal import statements in 30 consumers**
retired together. The family had no active outside production owner/caller.

Static capability review confirmed real effects:

| Family | Adjudicated capability; never executed during retirement |
|---|---|
| Browser | Default-browser URL open, downloads-page open, new tabs, web-search URLs, cookie-database-location inspection. |
| Development / VS Code | Caller-supplied build/debug/run command execution, Git commands, and VS Code process launch. |
| File | Copy, delete, move, read, rename, recursive search, write, and parent-directory creation on caller-supplied paths. |
| Windows | Clipboard read, process termination, shell-capable application launch, notifications/message boxes, process listing, service listing. |
| Managers / registry | In-memory registration/lookup and dispatch to registered browser, tool, and IDE objects. |

These are real capabilities, not inert implementations or permission to
execute them. No legacy browser/file/process/desktop/tool capability was
executed. No family-owned JAOS runtime-data, config, checkpoint/recovery,
canonical audit, or canonical permission persistence authority was found.
The mutating file tools are retirement candidates because they have
caller-supplied paths and no active owner/caller. The existing
`jaos_platform/runtime_state_inventory.py` exclusion is descriptive evidence,
not a dynamic import or canonical owner.

Canonical ownership remains `PlatformComposition` -> `jaos.tools.ToolManager`
-> registry and `ToolExecutionEngine` -> existing permission, approval, and
audit boundaries. Exact legacy APIs are not required for compatibility; no
legacy tool survives solely for F07 or F11. F07 permission/approval/audit
hardening and F11 architecture/runtime/security/chaos testing remain separate
canonical-path workstreams, both **NOT STARTED**. No tool behavior was ported
and no new tool or hardening policy was implemented.

`executive_brain/` remains live category D: **78 - 42 = 36** tracked Python
sources. All 36 source hashes and every internal Executive dependency are
preserved. RegistryManager external-root production callers remain **0**, with
the same six internal callers. ExecutivePipeline remains live. All nine
workflow sources are unchanged and workflow remains blocked by
`executive_brain.pipeline.executive_pipeline -> workflow.workflow_engine`.
Tools retirement did not unblock workflow or begin the remaining Executive
retirement.

Exactly two grouped configured cases were added to the existing
`tests/tests/platform/test_collection_containment.py`: archive fidelity and
caller/effect/dependency containment. Earlier prototype-presence assertions
now verify their exact archived payloads. The existing Executive AST guard is
shared by AI and tools containment. Historical 91-, 78-, and 42-source digests
remain checked using **13 AI archives + 42 tools archives + 36 live sources**;
the historical values were not discarded or weakened. The existing partial-root
archive helper checks each family's exact subtree.
`test_canonical_import_boundary.py` required **no modification**.

Classification remains **A=10, B=1, D=6, E=13, F=3, TOTAL=33**, with no top-level
E entry for tools. The exact D roots remain `brain/`, `core/`,
`executive_brain/`, `main.py`, `memory/`, and `workflow/`.
Static canonical launcher closure still analyzes **207 files / 206 reached
modules**, has no violations and does not reach `executive_brain.tools`.
Canonical lazy-map targets contain no retired-tools target. This does not
certify a live runtime. Canonical `run_jaos.py`, `jaos/`, and
`jaos_platform/` are unchanged.

Config containment is unchanged: SHA-256
`d862bd601301ae7bfc85aa16a5cc9f31e5f77b23bc54e84689a4276a5a2a447c`,
**9 definitions / 11 collected cases**, one configured legacy-facing file, and
zero configured Executive importers. Its disposition remains KEEP TEMPORARILY /
INTENTIONALLY CONFIGURED; retirement remains unauthorized.


Verification used repository `.venv/Scripts/python.exe -B` with
`PYTHONDONTWRITEBYTECODE=1`, `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`,
`-p no:cacheprovider`, and `-p anyio.pytest_plugin`. Every invocation received
a unique external Windows basetemp beneath
`%TEMP%/jaos_f06e_tools_20260923_c38564b/runs/<uuid>/pytest`.
The established external runner adjusts `os.mkdir` mode only inside that
disposable run tree to inherit its parent ACL; repository helpers, fixtures,
production behavior and assertions were not changed for the environment.

Exact pytest command prefix:
`.venv/Scripts/python.exe -B %TEMP%/jaos_f06e_tools_20260923_c38564b/runner.py`.
The runner passes the above flags and the following arguments to `pytest.main`.
All listed gates exited **0**, with no failures, errors or reported warnings.

| Arguments / verification, in executed order | Result |
|---|---|
| `tests/tests/platform/test_collection_containment.py -k f06e_executive_tools -q` | 2 passed, 48 deselected |
| `tests/tests/platform/test_collection_containment.py -k "f06d2a or f06d2b or f06d2e" -q` | 7 passed, 43 deselected |
| `tests/tests/tools/test_tool_manager.py tests/tests/tools/test_tool_registry.py tests/tests/tools/test_tool_interface.py tests/tests/tools/test_tool_models.py tests/tests/tools/test_delete_file_tool.py tests/tests/tools/test_write_file_tool.py tests/tests/executive/test_canonical_executive_controller.py -q` | 47 passed |
| `tests/tests/platform/test_collection_containment.py -q` | 50 passed |
| `tests/tests/platform/test_canonical_import_boundary.py -q` | 55 passed |
| `tests/tests/integration/test_run_jaos_launcher.py tests/tests/integration/test_run_jaos_banner.py -q` | 8 passed |
| `tests/tests/platform/test_platform_runtime.py tests/tests/platform/test_platform_runtime_lifecycle.py -q` | 21 passed |
| `tests/tests/composition/test_platform_composition.py -q` | 8 passed |
| `tests/tests/tools -q` | 119 passed |
| `tests/tests/platform/test_base_platform_service.py tests/tests/platform/test_service_container.py -q` | 9 passed |
| `tests/tests/platform/test_config_containment.py -q` | 11 passed |
| `tests/tests/platform -q` | 395 passed, 1 skipped |
| `tests/tests/composition -q` | 49 passed |
| `tests/tests/integration -q` | 17 passed |
| `tests/tests -q` | 1776 passed, 1 skipped |
| `. --collect-only -q` | 1777 tests collected |
| `.venv/Scripts/python.exe -B -m ruff check --no-cache tests/tests/platform/test_collection_containment.py` | PASS, exit 0 |

The platform skip is the pre-existing directory-symlink escape check requiring
a symlink-capable Windows host. No new skip or warning was introduced. No
configured test was retired: actual root collection reconciles
**1,775 + 2 = 1,777**, with **1,776 passed, 1 skipped** in the full suite.
The earlier 1,774/1 and 1,775 collection results remain historical baselines.

Initial Ruff found three import-layout findings (I001) and one nested-condition
finding (SIM102) in the changed test. These were corrected without changing
assertion behavior; the AI/tools containment rerun passed 4 cases with 46
deselected, and Ruff then passed. A targeted skip-diagnostic run confirmed
`test_profile_symlink_escape_is_rejected` skips with Windows `WinError 1314`
(symlink privilege unavailable), exit 0. No assertion or skip was weakened.

Canonical contract coverage includes manager registration/routing, registry
lookup/duplicate/missing behavior, request validation, existing permission and
approval denial/order, truthful failures and audit outcomes, and shared
composition identity. Canonical filesystem tests operate only on disposable
test paths; no legacy tool tests were resurrected and no archive was executed.

Protected baseline hashes and all 3,041 outside-scope files remain unchanged,
including SECURITY.md, the seven named runtime-data files, `.agents/`,
`.claude/`, `.codex/`, `.context-bridge/`, CLAUDE.md, graphify-out/, all three
project-state documents, remaining Executive, workflow, and canonical sources.
No Graphify operation ran. Scope is exactly **87 logical paths**: 42 originals,
42 archives, one collection-containment test, and these two architecture
documents. The rename-aware task view is **42 R100 + 3 M**. Ordinary unstaged
Git output shows 42 deletions and untracked archives because nothing was staged.
`git diff --check` passed; the index is empty and unchanged. HEAD remains
`c38564b`, aligned with origin. Nothing was committed or pushed.

RAA-003 remains OPEN; F06D, F06E and FORTRESS-06 remain IN PROGRESS. Remaining
Executive retirement, workflow retirement, F06F/F06G/F06H, F07/F11 hardening,
F09 and all later slices have not started. Step 8 remains blocked/not started,
Fortress certification is NOT STARTED, and major Phase 8 expansion remains
paused. Writer-sensitive `brain/`, `core/` except its already retired leaf,
`memory/`, and `main.py` boundaries remain unchanged. The two Founder decisions
for `main.py` and `BasePlatformService` / `PlatformContract` remain unresolved.
This tools slice is **READY FOR ATOMIC CHECKPOINT**; staging, commit and push
are not authorized by this task.

### 27.1 Exact 42-source baseline and archive inventory

Every original below was tracked, present in `c38564b`, and matched its HEAD
Git blob before retirement. Empty package markers have zero bytes; all nonempty
payloads use CRLF only, with zero bare LF or CR. Source and archive SHA-256,
byte count, line endings and normalized Git blobs are identical for every row.

| Original source | Exact archive | Bytes | CRLF | Checkout SHA-256 | Git-normalized blob |
|---|---|---:|---:|---|---|
| `executive_brain/tools/__init__.py` | `legacy_quarantine/production/executive_brain/tools/__init__.py.legacy` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `executive_brain/tools/browser/__init__.py` | `legacy_quarantine/production/executive_brain/tools/browser/__init__.py.legacy` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `executive_brain/tools/browser/browser_automation_tool.py` | `legacy_quarantine/production/executive_brain/tools/browser/browser_automation_tool.py.legacy` | 1370 | 55 | `94625edd3f8c190642bfea5cf0c328fdc0a86411de5b2f2969f4409266a567e7` | `2e3c19713edbf0959b06c53bc28069f526a9f408` |
| `executive_brain/tools/browser/browser_exceptions.py` | `legacy_quarantine/production/executive_brain/tools/browser/browser_exceptions.py.legacy` | 448 | 24 | `2c52f39e26cc50d97f1321d70da839545dec86e2fa681f55b9cf29bc689f23f4` | `0fd188159229f457af49e095e4437c12df22cd11` |
| `executive_brain/tools/browser/browser_interface.py` | `legacy_quarantine/production/executive_brain/tools/browser/browser_interface.py.legacy` | 962 | 44 | `3e1aad93e8ff6f4e7f67562bd714e01941f49629fd0a8a9cde32157ee55a4109` | `6d2ec19432df7f648de01dfb633d5c88c199c3fd` |
| `executive_brain/tools/browser/browser_manager.py` | `legacy_quarantine/production/executive_brain/tools/browser/browser_manager.py.legacy` | 1577 | 55 | `9c4fc7a34891cd58593aeee2701e6eaab19c908389250f2f635d03d1a3059e88` | `88921d49c88e5c4eb8dac4f35158f96619bfc336` |
| `executive_brain/tools/browser/browser_models.py` | `legacy_quarantine/production/executive_brain/tools/browser/browser_models.py.legacy` | 753 | 41 | `c4a5e762e6b2f306a2abebfe372e905e3325d729dc54867fa660acaee7724c6d` | `a230257f2a4ab6f794172b70a19aceeb69fe2c70` |
| `executive_brain/tools/browser/cookies_tool.py` | `legacy_quarantine/production/executive_brain/tools/browser/cookies_tool.py.legacy` | 1562 | 56 | `c5b1dc692ac7afc563c32734c4fdcf2cc4981e29ca6dc4978d08df49ec87f10e` | `cf67977d8be064a8aec3ca42a80c722464731e68` |
| `executive_brain/tools/browser/downloads_tool.py` | `legacy_quarantine/production/executive_brain/tools/browser/downloads_tool.py.legacy` | 2025 | 74 | `0ba872af8c97367b7dc43f8a237f9a765c0105a41009fa1a3858aa139708f0c9` | `8a9db1f72a826ea9109c70c0b3b22ffb14e0f1f5` |
| `executive_brain/tools/browser/tabs_tool.py` | `legacy_quarantine/production/executive_brain/tools/browser/tabs_tool.py.legacy` | 1261 | 51 | `094694c808538bc4304ca70e33ce7d1ca1aaf71fa481b235cb344f309fbdc066` | `3bfcb920891f08490605e31c2f090f24367b583e` |
| `executive_brain/tools/browser/web_search_tool.py` | `legacy_quarantine/production/executive_brain/tools/browser/web_search_tool.py.legacy` | 2543 | 85 | `2194b4a2381297a1d1e2b61189757c489d01075fd801e3b916926fd1c62f1904` | `de1ed10efeecc1e315c0dd17b3683de180ca10b4` |
| `executive_brain/tools/core/__init__.py` | `legacy_quarantine/production/executive_brain/tools/core/__init__.py.legacy` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `executive_brain/tools/core/tool_exceptions.py` | `legacy_quarantine/production/executive_brain/tools/core/tool_exceptions.py.legacy` | 433 | 24 | `b987ce63de86442b9eeef4440e51edff7d9c4b4e485cc58ff66f4cdc41262441` | `f4f41abd6a00e40b8f19840299d7963246df7e3b` |
| `executive_brain/tools/core/tool_interface.py` | `legacy_quarantine/production/executive_brain/tools/core/tool_interface.py.legacy` | 740 | 36 | `55984992fea16fb9ca09d7838225dc271c20fb309d51319833a7e487a31d1ce6` | `e2958718da6db818dec67b39cee4b374722c89e4` |
| `executive_brain/tools/core/tool_manager.py` | `legacy_quarantine/production/executive_brain/tools/core/tool_manager.py.legacy` | 1813 | 69 | `39d431f7bdad18539d28ee5f55e28fcad3a7e291865c40992d0418d9334107a7` | `158af932d819d82574e484c975692b1b2247afbe` |
| `executive_brain/tools/core/tool_models.py` | `legacy_quarantine/production/executive_brain/tools/core/tool_models.py.legacy` | 689 | 41 | `5cbbd91e926b62e272a5512604b681569cfaa9750f7c26242c821ebb274b3e7a` | `0b7eb1bc0a7cb3faff4dfdfd2a9fd66c61d3f74c` |
| `executive_brain/tools/core/tool_registry.py` | `legacy_quarantine/production/executive_brain/tools/core/tool_registry.py.legacy` | 1937 | 79 | `2f36bcc4da3264667ad4c3d98660a911d115eb9c1859c8bd8a81e74070ffa000` | `f975f4d13ce59d91536b5971b0282757bd8d2f46` |
| `executive_brain/tools/development/__init__.py` | `legacy_quarantine/production/executive_brain/tools/development/__init__.py.legacy` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `executive_brain/tools/development/ide_exceptions.py` | `legacy_quarantine/production/executive_brain/tools/development/ide_exceptions.py.legacy` | 419 | 24 | `66864cd78449d61948e2335f164b384054356204afb9bcb83f43bd64653b1582` | `4d6fe467f159abc75fed471bf5d7103d4cf23c64` |
| `executive_brain/tools/development/ide_interface.py` | `legacy_quarantine/production/executive_brain/tools/development/ide_interface.py.legacy` | 918 | 44 | `af0f2c4defa9e39c606426cde68901dcbe10f9746de64dc40912f795453f9059` | `b329312b490422437de071c11f6ee54943a13a9a` |
| `executive_brain/tools/development/ide_manager.py` | `legacy_quarantine/production/executive_brain/tools/development/ide_manager.py.legacy` | 1498 | 55 | `9e5c5d05c34f83e2a787af8f5c7f7775e29cee09d4d54bedf4f2db6a69e194cb` | `7334058d11ef3906fd8b1450b270bf70785bc3b2` |
| `executive_brain/tools/development/ide_models.py` | `legacy_quarantine/production/executive_brain/tools/development/ide_models.py.legacy` | 728 | 41 | `9f0ef34d04fe91845d1fab1c2d7f75ef2d0d4e1a064d984800a53fa949c4f8c4` | `2c1abc6775a46a9969f748cb9c94ce48fcc10acc` |
| `executive_brain/tools/development/vscode/build_tool.py` | `legacy_quarantine/production/executive_brain/tools/development/vscode/build_tool.py.legacy` | 2491 | 85 | `f4ab7ab8484d44c57aba2b863167714f37dd2a2fb996aa5332e217083bf344fd` | `522502abb21161765b65599a5a5ec28d028c75de` |
| `executive_brain/tools/development/vscode/debug_tool.py` | `legacy_quarantine/production/executive_brain/tools/development/vscode/debug_tool.py.legacy` | 2491 | 85 | `6c81cdb86c9b08a8ccf5c933d1a5f4c8fcaf49c314542decfa9885f234a2a05d` | `7d6e1a2acf0e467484fbca433c322c81a13d86e7` |
| `executive_brain/tools/development/vscode/git_tool.py` | `legacy_quarantine/production/executive_brain/tools/development/vscode/git_tool.py.legacy` | 2531 | 85 | `2becf449a18dfc9d697e1d2c6f101389b7f1c97b866ebd2049b1e1d0e24d5553` | `0d071742e785daa15ad147127f7cb739406535ef` |
| `executive_brain/tools/development/vscode/project_tool.py` | `legacy_quarantine/production/executive_brain/tools/development/vscode/project_tool.py.legacy` | 1829 | 69 | `382a761e3082bef712a6bca97479bb25b2a65a766995ba4599ca5d8d95719aaa` | `9239cbafc2400ab29df1a73bf7f57f3399106da2` |
| `executive_brain/tools/development/vscode/run_tool.py` | `legacy_quarantine/production/executive_brain/tools/development/vscode/run_tool.py.legacy` | 2475 | 85 | `ecac46d4c53114edffa3c13d04036ff30831c3a49f8aff821706045c1afde368` | `b754cc86e22c68a43f0c33aa390ab733e211a731` |
| `executive_brain/tools/file/__init__.py` | `legacy_quarantine/production/executive_brain/tools/file/__init__.py.legacy` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `executive_brain/tools/file/copy_file_tool.py` | `legacy_quarantine/production/executive_brain/tools/file/copy_file_tool.py.legacy` | 1807 | 64 | `3e644c8d0f8fc69bce098f5b05307541d7591a2614b12bf43087b9d9b04b8ed8` | `0ec0339b0d02541c4b984a1fd058794e6e9fffc8` |
| `executive_brain/tools/file/delete_file_tool.py` | `legacy_quarantine/production/executive_brain/tools/file/delete_file_tool.py.legacy` | 1560 | 60 | `8ffcd9bb4d1fdb8ff3da76d7232090796b860b7b7be627d93b07f94dbdd0c386` | `0e41a1bebc50dbcc0cb5e2e41d00d7cbdb2bce7f` |
| `executive_brain/tools/file/move_file_tool.py` | `legacy_quarantine/production/executive_brain/tools/file/move_file_tool.py.legacy` | 1813 | 64 | `3d82c2503a95a13bdc10a279124938ab7ab2b627d1d4679ceb9b73ebfe36943b` | `13f078ecfd4d87764f89e26e77789ce531d1e24a` |
| `executive_brain/tools/file/read_file_tool.py` | `legacy_quarantine/production/executive_brain/tools/file/read_file_tool.py.legacy` | 1670 | 63 | `39fc62167618107278d7aa09edf0518b88a10891d2a6da174b6eb874611967c9` | `cf97c669c661a62223534d479a5e616f96723b9b` |
| `executive_brain/tools/file/rename_file_tool.py` | `legacy_quarantine/production/executive_brain/tools/file/rename_file_tool.py.legacy` | 1763 | 62 | `bd5a07b2ded36955d922e2a612d823d4a8199ad8c7756dc89c3d3d5b35682734` | `d2cab21e55b8c1f3ff69c4d9381f4b38f0ed6e65` |
| `executive_brain/tools/file/search_file_tool.py` | `legacy_quarantine/production/executive_brain/tools/file/search_file_tool.py.legacy` | 2002 | 72 | `77aa69e3e998dc225babfb3cad4279299e10dfa264c5a20614ea8ce544a5d551` | `826cc9a938d01a9146b562ec30c2e681e578f525` |
| `executive_brain/tools/file/write_file_tool.py` | `legacy_quarantine/production/executive_brain/tools/file/write_file_tool.py.legacy` | 1449 | 54 | `915de2957409dbd5968fbdbf175653711fb7ef238f580a10ebc681bae05be61c` | `39e9c76a4b66687cdff61c175f7d2590a792e030` |
| `executive_brain/tools/windows/__init__.py` | `legacy_quarantine/production/executive_brain/tools/windows/__init__.py.legacy` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `executive_brain/tools/windows/clipboard_tool.py` | `legacy_quarantine/production/executive_brain/tools/windows/clipboard_tool.py.legacy` | 1134 | 50 | `ed5e7daa97eb65d7b6c22c253215748157dda40d64e0043723197126b48eb652` | `1c5369dd46a49a732fc0183117f62e0a7b869d03` |
| `executive_brain/tools/windows/close_application_tool.py` | `legacy_quarantine/production/executive_brain/tools/windows/close_application_tool.py.legacy` | 1421 | 56 | `71c21a6f2a5e7fe62d97d76d11b58626a89c5f96965a36c062494d9f7388070f` | `e1823dd8db67c3dd42f5e7aed8b1a47cfd541425` |
| `executive_brain/tools/windows/launch_application_tool.py` | `legacy_quarantine/production/executive_brain/tools/windows/launch_application_tool.py.legacy` | 2306 | 76 | `3f7cccfc69d21588f35829e457e26108b9037cc006c5282feee3cce49a1421d6` | `72c915b16bb153321ef972c4b8ad4b7d6aa5fbbf` |
| `executive_brain/tools/windows/notification_tool.py` | `legacy_quarantine/production/executive_brain/tools/windows/notification_tool.py.legacy` | 1725 | 65 | `6c0d45dd795c73ac24de914592e4504d2c2a31e883e2563a4e2eac534ac301ca` | `c2d27f11f73555d4f29eeede9c21c7365a6d45c9` |
| `executive_brain/tools/windows/process_manager_tool.py` | `legacy_quarantine/production/executive_brain/tools/windows/process_manager_tool.py.legacy` | 2540 | 95 | `a9a83584fa37ffff623fd6b68b2bd7211488647f0839563fa1ac24f39749266a` | `321048b0fed43b7c9aca6884f4bd69162b4ecef0` |
| `executive_brain/tools/windows/services_tool.py` | `legacy_quarantine/production/executive_brain/tools/windows/services_tool.py.legacy` | 2843 | 98 | `ae661a81f5068938d082d1a08699f3f6d20acfedc7fef7336efc01b77c970287` | `a93dae3232c0c6f3d18124d5906daa23e444acf4` |

### 27.2 Exact remaining 36-source Executive inventory

These 36 live sources match their pre-slice checkout hashes. Their internal
dependencies remain intact; none imports the retired tools family.

```text
executive_brain/__init__.py
executive_brain/brain/__init__.py
executive_brain/brain/executive_brain.py
executive_brain/common/__init__.py
executive_brain/common/enums.py
executive_brain/intent.py
executive_brain/managers/__init__.py
executive_brain/managers/decision_manager.py
executive_brain/managers/execution_manager.py
executive_brain/managers/mission_manager.py
executive_brain/managers/planning_manager.py
executive_brain/managers/registry_manager.py
executive_brain/managers/result_manager.py
executive_brain/memory/__init__.py
executive_brain/memory/memory_manager.py
executive_brain/memory/memory_registry.py
executive_brain/memory/working_memory.py
executive_brain/models/__init__.py
executive_brain/models/context_snapshot_model.py
executive_brain/models/decision_model.py
executive_brain/models/execution_plan_model.py
executive_brain/models/goal_model.py
executive_brain/models/intent_model.py
executive_brain/models/mission_model.py
executive_brain/models/result_model.py
executive_brain/pipeline/executive_pipeline.py
executive_brain/planner/__init__.py
executive_brain/registries/__init__.py
executive_brain/registries/base_registry.py
executive_brain/registries/decision_registry.py
executive_brain/registries/execution_plan_registry.py
executive_brain/registries/goal_registry.py
executive_brain/registries/intent_registry.py
executive_brain/registries/mission_registry.py
executive_brain/registries/result_registry.py
executive_brain/timeline/__init__.py
```

---

## 28. FORTRESS-06E Final Remaining Executive Production-Family Quarantine

FORTRESS-06E final remaining executive_brain production-family quarantine:
**IMPLEMENTED AND VERIFIED**. This is the separately authorized atomic final
36-source family retirement at baseline `b0c2e1e`, not broader F06E closure or
live-runtime certification. The branch is `phase8-ai-intelligence`, aligned
with origin; the index remains empty. Earlier AI/provider and tools checkpoints
are `9622619` and `ae9d00a` respectively.

The fresh gate matched exactly **36 tracked Python sources / 53,957 checkout
bytes / 27 nonempty CRLF files / nine empty initializers / mode 100644**.
Every destination was absent. No cache, `.pyc`, generated or untracked artifact,
symlink, or reparse point existed beneath the live root. All 36 files were
moved byte-identically with their hierarchy preserved and `.py.legacy` suffixes;
SHA-256, sizes, CRLF counts, and normalized source/archive Git blobs match.
Only empty live source directories were removed. Live Executive Python sources
are **0**; its root, caches, and unintended namespace package are absent.
No wrapper, stub, alias, replacement, importable initializer, or import from
quarantine was introduced. Payloads remain inert and reversible.

Before movement, canonical production, other live legacy production,
configured-test, and scripts/tooling/dev importers were each **0 files / 0
edges**. The family had **36 nodes / 55 explicit internal edges / 36 singleton
SCCs / zero multi-node SCCs / zero self-cycles**. All 55 edges retired together.
RegistryManager's six internal Executive callers retired with it; its external
live and canonical/configured callers remain zero. RegistryManager and
ExecutivePipeline are no longer live.

Inert final-family debt remains byte-identical: **17 quarantined test files /
47 edges; 12 excluded flat files / 21 edges; one archived production edge**
from `legacy_quarantine/production/core/kernel.py.legacy` to RegistryManager.
Archived and excluded references are not counted as live callers. Tests parse
their ASTs and verify hashes without executing those payloads.

The preserved historical edge is
`executive_brain.pipeline.executive_pipeline -> workflow.workflow_engine`.
ExecutivePipeline imported and constructed WorkflowEngine; workflow imported
nothing back, with no cycle. Retiring the final production importer removes
that blocker. **workflow remains LIVE, UNTOUCHED, and production-caller-unblocked
for a SEPARATE later adjudication; it is not yet adjudicated for retirement.**
All nine workflow sources retain their prior inventory hash. BasePlatformService
now has exactly **one** direct live production consumer:
`workflow/workflow_engine.py`. PlatformContract has **zero**. Both compatibility
abstractions remain unchanged; their Founder retain/deprecate/archive decision
remains unresolved for F06G.

Static effect review preserved the no-F06F-split conclusion: none of these 36
owns protected JSON, MemoryStore, config, checkpoint, recovery, or runtime-data
persistence; provider/network execution; subprocess/tool execution; or canonical
permission, approval, or audit authority. Legacy transient object, dictionary,
lifecycle, context, and event behavior remains historical only. ExecutiveBrain,
MemoryManager, and ExecutivePipeline can interact with runtime registration,
context, events, and indirect logging if executed; none was executed here.

ADR-0012 and ADR-0013 remain unchanged and authoritative. Exact managers,
registries, WorkingMemory, MemoryRegistry, MemoryManager, planning, pipeline,
and intent APIs were retired without shadow replacements, simulated approvals,
simulated success, legacy identifier/count behavior, or future planning work.
Persistent ownership remains canonical MemoryStore/SQLiteStore; this does not
claim they reproduce every legacy transient API. Future transient Context
ownership stays separately governed, health/degradation remains F10's
responsibility, and no direct MemoryContextSource/MemorySearchEngine coupling
was added. **RAA-009 remains OPEN — DEFERRED.** Canonical ExecutiveController,
MemoryStore, and completed MS-0025A-D ConversationOrchestrator ownership remain
intact. MS-0025X and major Phase 8 expansion remain paused.

Historical reconstruction is **13 AI archives + 42 tools archives + 36 final
archives = 91 original Executive sources**, checked against the pre-retirement
`0627453` Git tree with **zero blob mismatches**. Canonical static launcher
closure remains **207 analyzed files / 206 imported repository modules excluding
the launcher**, with zero Executive reach, service-registration targets, or lazy
targets. `run_jaos.py`, `jaos/`, and `jaos_platform/` are unchanged. Static closure
alone is not evidence of live runtime readiness or certification.

Exactly two grouped configured cases were added to
`tests/tests/platform/test_collection_containment.py`: final-root archive
fidelity and final caller/authority containment. Earlier payload, debt, and
historical inventory evidence remains checked; obsolete live-family assertions
now check final absence and historical reconstruction. The canonical-boundary
test moves the single Executive root history from D to E without separate AI
or tools entries: **A=10 / B=1 / D=5 / E=14 / F=3 / TOTAL=33**. The exact five D
roots are **brain/, core/, main.py, memory/, workflow/**.

Config containment remains unchanged at SHA-256
`d862bd601301ae7bfc85aa16a5cc9f31e5f77b23bc54e84689a4276a5a2a447c`:
**nine definitions / eleven collected cases / one configured legacy-facing
file / zero configured Executive importers**. Its retirement remains unauthorized.

Validation used repository `.venv/Scripts/python.exe -B`,
`PYTHONDONTWRITEBYTECODE=1`, `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`,
`-p no:cacheprovider -p anyio.pytest_plugin`, and a unique external
`--basetemp` under `%TEMP%/jaos_f06e_final_20260924/runs/<uuid>/pytest`.
The established external Windows runner inherits ACLs only for directories
inside each disposable test tree; no repository helper or assertion was bypassed.
Exact runner and per-gate logs are in that external evidence directory.

Common command prefix for each target below:
`.venv/Scripts/python.exe -B %TEMP%/jaos_f06e_final_20260924/runner.py`.
The runner supplies the plugin/cache/basetemp switches above. Every successful
gate below exited **0**, in the requested order.
Later aggregate gates also enabled `-ra` for skip reporting.

| Gate / exact target arguments | Executed result |
|---|---|
| `tests/tests/platform/test_collection_containment.py -k f06e_executive_final -q` | 2 passed, 50 deselected |
| `tests/tests/platform/test_collection_containment.py -q` | 52 passed in 255.60s (0:04:15) |
| `tests/tests/platform/test_canonical_import_boundary.py -q` | 55 passed in 6.57s |
| `tests/tests/executive/test_canonical_executive_controller.py -q` | 4 passed in 0.98s |
| `tests/tests/executive -q` | 7 passed in 0.83s |
| `tests/tests/memory -q` | 361 passed in 12.24s |
| `tests/tests/composition/test_memory_platform_composition.py -q` | 12 passed in 1.76s |
| `tests/tests/intelligence/test_conversation_orchestrator.py -q` | 15 passed in 0.80s |
| `tests/tests/composition/test_intelligence_platform_composition.py -q` | 13 passed in 1.52s |
| `tests/tests/integration/test_run_jaos_launcher.py tests/tests/integration/test_run_jaos_banner.py tests/tests/integration/test_shell_shutdown_lifecycle.py -q` | 17 passed in 1.95s |
| `tests/tests/platform/test_platform_runtime.py tests/tests/platform/test_platform_runtime_lifecycle.py tests/tests/platform/test_boot_manager.py tests/tests/platform/test_fortress_03_lifecycle_closure.py -q` | 47 passed in 1.97s |
| `tests/tests/composition/test_platform_composition.py -q` | 8 passed in 1.61s |
| `tests/tests/platform/test_base_platform_service.py tests/tests/platform/test_service_container.py -q` | 9 passed in 0.75s |
| `tests/tests/platform/test_config_containment.py -q` | 11 passed in 4.15s |
| `tests/tests/platform -q` | 397 passed, 1 skipped in 273.32s (0:04:33) |
| `tests/tests/composition -q` | 49 passed in 5.91s |
| `tests/tests/integration -q` | 17 passed in 1.47s |
| `tests/tests -q` | 1778 passed, 1 skipped in 299.57s (0:04:59) |
| `. --collect-only -q` | 1779 tests collected in 4.71s |
| `python -B -m ruff check tests/tests/platform/test_collection_containment.py tests/tests/platform/test_canonical_import_boundary.py` | All checks passed; exit 0 |

Collection reconciles as **1,777 + 2 = 1,779**; configured execution is
**1,778 passed / one skipped**. These are executed results, not the arithmetic
projection. The full configured suite also covers the remaining MS-0025A-D
configured cases. The one pre-existing skip remains unchanged.
The full run identifies it as `test_profile_symlink_escape_is_rejected`:
Windows directory symlinks are unavailable (`WinError 1314`, required privilege
not held). No test warning summary was reported. Comparing current root node IDs
with the prior tools-checkpoint collection log confirms exactly the two new
cases and zero removed IDs; that 1,777-ID reference is historical, not a rerun.

The first new-case run reported one passed and one failed: the new authority
assertion named ConversationOrchestrator's implementation module while canonical
composition imports the public `jaos.intelligence.conversation` export. Static
inspection confirmed a new-test expectation error; only that assertion was
corrected, then both cases passed before the broader ladder. A PowerShell
invocation stalled before starting Python; it was stopped and replaced with a
file-based launcher, with no test gate represented as executed by that attempt.
The first Ruff run reported I001 import formatting and SIM102 nested-condition
style in the new case. Both were corrected without changing the checked
conditions; Ruff then passed and both new cases were rerun successfully.
The full-suite result above precedes those two style-only corrections; the final
test-file state has the successful focused rerun and Ruff evidence.

Final static and Git validation confirms exactly **76 logical task paths**:
36 originals + 36 archive destinations + two Python tests + two architecture
documents. An external, normalized before/after `git diff --no-index
--find-renames=100% --rename-empty` view reports **36 R100** moves; together with
the four modified files this is **40 logical Git records**. Identical empty
files may pair differently; the exact path mapping and hashes are authoritative.
Ordinary unstaged Git output represents the moves as deletions and untracked
archives because the real index was never changed by staging.

The pre-existing working-tree state is preserved, including SECURITY.md, all
seven named data JSON files, .agents/, .claude/, .codex/, .context-bridge/,
CLAUDE.md, graphify-out/, project-state documents, brain/, core/, memory/,
main.py, workflow/, canonical production, and compatibility abstractions.
`git diff --check` passes. HEAD remains `b0c2e1e`, aligned with origin on
`phase8-ai-intelligence`; the index is empty. No staging, commit, push, reset,
restore, clean, Graphify, legacy execution, or excluded script/test execution
occurred.

**RAA-003 remains OPEN. F06E remains IN PROGRESS pending broader F06E closure.**
F06F, F06G, F06H, and F07-F12 were not started. Workflow retirement and later
adjudication were not started. This exact slice is **READY FOR ATOMIC CHECKPOINT**;
checkpoint actions require separate authorization. Earlier slice sections retain
their historical counts and boundaries; this section records the current result.

### 28.1 Exact 36-source baseline and archive inventory

All rows were mode 100644 at `b0c2e1e`. Checkout bytes, SHA-256, sizes, CRLF
counts, and normalized Git blobs are identical at each exact destination.
Nine empty initializers have zero size and zero line endings; the other 27
have CRLF only, with no bare LF or CR. No archive payload was edited.

| Original source | Exact archive | Bytes | CRLF | Checkout SHA-256 | Git-normalized blob |
|---|---|---:|---:|---|---|
| `executive_brain/__init__.py` | `legacy_quarantine/production/executive_brain/__init__.py.legacy` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `executive_brain/brain/__init__.py` | `legacy_quarantine/production/executive_brain/brain/__init__.py.legacy` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `executive_brain/brain/executive_brain.py` | `legacy_quarantine/production/executive_brain/brain/executive_brain.py.legacy` | 6317 | 168 | `b3b6764a87d49a17d1a3a56f2fdf4d8252956f5d7e42bac21fd429622b083666` | `79022071de3e7867b62d6bcc5c406873869b39c5` |
| `executive_brain/common/__init__.py` | `legacy_quarantine/production/executive_brain/common/__init__.py.legacy` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `executive_brain/common/enums.py` | `legacy_quarantine/production/executive_brain/common/enums.py.legacy` | 322 | 16 | `a52965315e654ca657df47258e443e8b6aadbb1f38a83505c7a65c187ed7de0c` | `7a7e8e4a862aff1218f0628b4e239ed818207f43` |
| `executive_brain/intent.py` | `legacy_quarantine/production/executive_brain/intent.py.legacy` | 1264 | 65 | `5ec559d7657572d122b4e8314ce5cb4fa4af2aff14d2018e2f691294366844e6` | `5f43d48d4d7ff5cadaef8454c86a2befbd1d73ff` |
| `executive_brain/managers/__init__.py` | `legacy_quarantine/production/executive_brain/managers/__init__.py.legacy` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `executive_brain/managers/decision_manager.py` | `legacy_quarantine/production/executive_brain/managers/decision_manager.py.legacy` | 2762 | 90 | `ca6b95e1a54aaf97283e5b8dcce90077e7551a51399d73679d3e4565781289b6` | `e0f71b0f78afd0a443db5acdf265c2252bf9d163` |
| `executive_brain/managers/execution_manager.py` | `legacy_quarantine/production/executive_brain/managers/execution_manager.py.legacy` | 2896 | 93 | `3afb70ab262a1c719da50bfe283b525812247f90a2d8f3265c59946be45229a7` | `9aa525907ccefc7dd628df7f01cb148c101e7939` |
| `executive_brain/managers/mission_manager.py` | `legacy_quarantine/production/executive_brain/managers/mission_manager.py.legacy` | 3248 | 112 | `163bdb92ca057333f21e024adc9bfb34adb521a9d45585805a56d520f88a2192` | `764c12b60b26df084437f86a99905a8a907286ff` |
| `executive_brain/managers/planning_manager.py` | `legacy_quarantine/production/executive_brain/managers/planning_manager.py.legacy` | 2497 | 85 | `2fdab0f81378825fc9b31a739cbb44bcca807456815b0af07a28b689c6a17ea5` | `69e22b7d60db7cf91a4ff71ba59f1831e1613c68` |
| `executive_brain/managers/registry_manager.py` | `legacy_quarantine/production/executive_brain/managers/registry_manager.py.legacy` | 2311 | 64 | `e9d3d8eee3dbf133fa346541d3690d316bd586ea6ca925e325fd0b960979c2d7` | `c11d40f0621b43ace4579363fa7f6f7cde371198` |
| `executive_brain/managers/result_manager.py` | `legacy_quarantine/production/executive_brain/managers/result_manager.py.legacy` | 2476 | 84 | `c6ff7e64b1d5e07d3d8a90504299066d9da3a0ac8a35c6029b9ca14f32ceab45` | `505b66e1e948b176637601474877813e85f76a16` |
| `executive_brain/memory/__init__.py` | `legacy_quarantine/production/executive_brain/memory/__init__.py.legacy` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `executive_brain/memory/memory_manager.py` | `legacy_quarantine/production/executive_brain/memory/memory_manager.py.legacy` | 2340 | 84 | `e6c728007ae18e56ae8f7e9dd305e033d20326d80bd28c272d66131887ed4405` | `e85118e26714e25db8028983ce5e5c682abffa47` |
| `executive_brain/memory/memory_registry.py` | `legacy_quarantine/production/executive_brain/memory/memory_registry.py.legacy` | 916 | 27 | `b3e12a5a0ec2e3a9a2b5f6c0fdd1d0aa0edfd9915c3f17cfed96c1cbdffe2d97` | `34b671274a46da86657b0d5d6fe3a882e4a2f6d0` |
| `executive_brain/memory/working_memory.py` | `legacy_quarantine/production/executive_brain/memory/working_memory.py.legacy` | 2167 | 58 | `ff7f567a9765202bda71fc92c6772a5c043f25394637e485dac9181a6bce1c11` | `b38ba268dca51d4850951c28423added2c4b5bdf` |
| `executive_brain/models/__init__.py` | `legacy_quarantine/production/executive_brain/models/__init__.py.legacy` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `executive_brain/models/context_snapshot_model.py` | `legacy_quarantine/production/executive_brain/models/context_snapshot_model.py.legacy` | 1586 | 61 | `9e2278aa649f19abf985ba05850a6a1c131a4a5d30d3151d39bfecb50b077814` | `24f744ee8c906213d92bfadafb3953a251855cc5` |
| `executive_brain/models/decision_model.py` | `legacy_quarantine/production/executive_brain/models/decision_model.py.legacy` | 1680 | 55 | `deceeee997d672e73cf04e2930ee3a7839529bb5f05ece578f0f8b2238ec0f26` | `c6b036f8505289eb50ca2b251a70067f4ea2cc52` |
| `executive_brain/models/execution_plan_model.py` | `legacy_quarantine/production/executive_brain/models/execution_plan_model.py.legacy` | 1432 | 48 | `a080419965ecb23e8459fd1c8a117fca92d39d964d14726ffebd6d2eedec5cd6` | `8599b02b89af0e9e7d237a4ad323690b6c497677` |
| `executive_brain/models/goal_model.py` | `legacy_quarantine/production/executive_brain/models/goal_model.py.legacy` | 1309 | 38 | `8868b1096b83dfc5a0e4670a695134b9d0b440f235df70cf7857b105c1ba0684` | `d6f87ace400f8ddfc17b73aec421d331d8bb1c3b` |
| `executive_brain/models/intent_model.py` | `legacy_quarantine/production/executive_brain/models/intent_model.py.legacy` | 1386 | 40 | `e894f1cb3b1741e8edab581d159db384140bda66233ca33ac8fadf951b9204c4` | `327bfd5fe9e82b00f142a12982ddf330cd2bb3b0` |
| `executive_brain/models/mission_model.py` | `legacy_quarantine/production/executive_brain/models/mission_model.py.legacy` | 2068 | 59 | `552b761214a9b4cc875a2ea730ce17852bf0f191586e5e014b7790b81b07b45e` | `3b722a1d6627bb576c40b59fbfea9a7d7b8666ef` |
| `executive_brain/models/result_model.py` | `legacy_quarantine/production/executive_brain/models/result_model.py.legacy` | 1251 | 45 | `138a175e6d503b7c2e07c372cd407b03713386130af8fadbfa2fe1d1784de0c5` | `ed99ab110ca751e279948b1a57cd88b52e5189c5` |
| `executive_brain/pipeline/executive_pipeline.py` | `legacy_quarantine/production/executive_brain/pipeline/executive_pipeline.py.legacy` | 851 | 26 | `bf8b105c0de804d67ecf95b53861d00295c9f257038ac6ad68667f7a1239da0b` | `e80c3db6376df497c9f302938524e10c9647743c` |
| `executive_brain/planner/__init__.py` | `legacy_quarantine/production/executive_brain/planner/__init__.py.legacy` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `executive_brain/registries/__init__.py` | `legacy_quarantine/production/executive_brain/registries/__init__.py.legacy` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `executive_brain/registries/base_registry.py` | `legacy_quarantine/production/executive_brain/registries/base_registry.py.legacy` | 1216 | 46 | `0b5192ab84dae8b473949c09af498230193701fdd854d6a55509216258f11a08` | `9f223a34c6585fa58e85311ba810933ee95e40d3` |
| `executive_brain/registries/decision_registry.py` | `legacy_quarantine/production/executive_brain/registries/decision_registry.py.legacy` | 1039 | 34 | `e085fdb64cad672eca2559fd26a8596590b69fae60300e48cfbe718a6e2f5031` | `83c16f1079a4f9d383267c82302f125eb8e09a6e` |
| `executive_brain/registries/execution_plan_registry.py` | `legacy_quarantine/production/executive_brain/registries/execution_plan_registry.py.legacy` | 3145 | 102 | `00c4e82bf2bc4d0b4fb8b6d5def67c0d7b6d68634aa10dae35939dc010fb3c24` | `32eaa1e981314a87fc96cea6d499445fd2510a38` |
| `executive_brain/registries/goal_registry.py` | `legacy_quarantine/production/executive_brain/registries/goal_registry.py.legacy` | 1688 | 56 | `b874a1299dd0ccf08cf7cbf046b5dd798f8572e972bfc8e930dc515f943d3490` | `1d4f2220c2c7434b8f6db4ddbc0183b55e04ca49` |
| `executive_brain/registries/intent_registry.py` | `legacy_quarantine/production/executive_brain/registries/intent_registry.py.legacy` | 702 | 24 | `08c9e3090fe437f7543594b00b2562ed34e9dcf0496848a4bb8b740b7908e481` | `c3f44a29c016b364a361f6f1b786cc1cbe8b9c88` |
| `executive_brain/registries/mission_registry.py` | `legacy_quarantine/production/executive_brain/registries/mission_registry.py.legacy` | 2733 | 99 | `b39d3383026de0010ed273441b8b91466304c9136872aa19ccacc410664157ef` | `de0d1660573e0af1f2f0181bb8c801f0d34d69d9` |
| `executive_brain/registries/result_registry.py` | `legacy_quarantine/production/executive_brain/registries/result_registry.py.legacy` | 2355 | 83 | `5dce7b02020cfbe7b4d474033d311b0f27260c8a32104125d7953006030891b0` | `73af691da99a45bb49c4608e4dc20944989fc35b` |
| `executive_brain/timeline/__init__.py` | `legacy_quarantine/production/executive_brain/timeline/__init__.py.legacy` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |

---

## 29. FORTRESS-06E Workflow Production-Family Quarantine

**Status: IMPLEMENTED AND VERIFIED** for this exact nine-source quarantine.
This is not F06E closure or runtime certification. The Founder approved this
slice and clarified the ordering: only declarative workflow archive/classification
state changed before regression; verification evidence was written after the
first complete ladder passed. The final working tree is the target of the
subsequent final-state verification; evidence files are external to the repository.

Baseline: `phase8-ai-intelligence`, HEAD and origin tracking ref both
`0a04ae26f3b8dff8407b9364247e8d4dfd5ff17e`, empty index. The fresh gate confirmed
exactly nine tracked Python sources, all Git mode `100644`, **7,969 checkout
bytes**, eight nonempty CRLF files and one empty initializer. No cache, bytecode,
artifact, unexpected source, or archive collision was present. Existing protected
changes were fingerprinted before movement and preserved.

All nine sources now reside at
`legacy_quarantine/production/workflow/<original-name>.py.legacy` with identical
checkout bytes, SHA-256, size, EOL counts, normalized Git blob and mode. The exact
mapping is recorded in manifest section 29.1. The original hierarchy is
preserved and the move is reversible. There is no live `workflow/` directory,
Python source, bytecode, cache, generated artifact, or importable workflow
namespace. Archives are non-importable and non-collectable, with no executable
archive initializer. No wrapper, stub, alias, payload edit, quarantine import,
or replacement shadow behavior was introduced.

Static import evidence: canonical production **0 files / 0 edges**, other live
production **0 / 0**, configured tests **0 / 0**, and scripts/tooling/dev **0 / 0**.
Historical reconstruction remains nine nodes, zero explicit internal edges,
**nine singleton SCCs**, zero multi-node SCCs and zero self-cycles.
Eight excluded flat scripts retain exactly 15 workflow import statements:
`automation_rules_engine_test.py`, `dependency_manager_test.py`,
`retry_recovery_engine_test.py`, `task_manager_test.py`, `task_queue_test.py`,
`workflow_engine_test.py`, `workflow_monitor_test.py`, and
`workflow_platform_integration_test.py`, all under `tests/`.
The inert `legacy_quarantine/tests/integration/test_workflow_runtime_integration.py.legacy`
retains one workflow import. Archived ExecutivePipeline retains its one
`workflow.workflow_engine` reference as historical evidence only. Their hashes
and collection exclusions remain unchanged; none was executed or resurrected.

Workflow owns no protected JSON, runtime-data, config, checkpoint, recovery,
or persistent-memory writer, subprocess/tool/provider/network invocation, or
canonical permission/approval/audit mutation. Its historical collections remain
transient dictionaries/lists; logger calls and runtime event publication do not
create canonical execution authority. All declared F06F writers and the runtime
writer inventory remain unchanged outside workflow. **No F06F split is required.**

The canonical authority remains
`ExecutiveController -> ExecutivePlanner -> ExecutionCoordinator -> ToolManager
-> ToolExecutionEngine -> ToolPermissionManager -> ToolApprovalManager
-> tool.execute -> ToolAuditLogger`. Production sources are unchanged; configured
Executive/Tool tests verify the existing authority and denial/approval behavior.
No permission/approval bypass was introduced. Automatic READY, printed demos,
independent workflow dictionaries, fake scheduling/retry/recovery semantics and
legacy exact APIs were not ported. Future Workflow & Automation Platform remains
deferred. BasePlatformService live production consumers fall **1 -> 0**;
PlatformContract remains **0**. Both abstractions are preserved unchanged;
Founder-level compatibility disposition remains F06G.

Static canonical launcher closure remains **207 analyzed files / 206 reached
repository modules excluding the launcher**, with workflow reach, workflow lazy
targets and canonical workflow registrations all **0**. `run_jaos.py`, `jaos/`
and `jaos_platform/` are unchanged. This is static closure evidence, not live
runtime certification.

Exactly two grouped configured cases were added to
`tests/tests/platform/test_collection_containment.py`: workflow archive fidelity
and workflow caller/authority containment. Earlier live-workflow expectations
now reconstruct the original inventories from archives; prior Executive and
archive evidence remains. The boundary guard moves the single workflow root
**D -> E** without a duplicate entry, preserving the prohibition on canonical
workflow reach. Classification is **A=10 / B=1 / D=4 / E=15 / F=3 / TOTAL=33**.
The four D roots are exactly **brain/, core/, main.py, memory/**.

Config containment remains byte-identical at SHA-256
`d862bd601301ae7bfc85aa16a5cc9f31e5f77b23bc54e84689a4276a5a2a447c`:
**9 definitions / 11 cases / 1 configured legacy-facing file / 0 workflow imports**.

Validation used `.venv/Scripts/python.exe -B`, `PYTHONDONTWRITEBYTECODE=1`,
`PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, `-p no:cacheprovider -p anyio.pytest_plugin`,
`-ra`, and a fresh external test-owned `--basetemp` per invocation under
`%TEMP%/jaos_f06e_workflow_20260928/runs/<uuid>/pytest`. The established external
Windows runner inherits ACLs only within each disposable test tree; no repository
helper or assertion was bypassed. Common pytest command prefix:
`.venv/Scripts/python.exe -B %TEMP%/jaos_f06e_workflow_20260928/runner.py`.
Gate 10 includes both PlatformComposition and canonical composition invariants;
the effective target arguments are printed in its log. Every gate below exited 0.

| Gate / exact target arguments | Executed result |
|---|---|
| `tests/tests/platform/test_collection_containment.py -k f06e_workflow -q` | 2 passed, 52 deselected in 17.56s; exit 0 |
| `tests/tests/platform/test_collection_containment.py -q` | 54 passed in 328.78s (0:05:28); exit 0 |
| `tests/tests/platform/test_canonical_import_boundary.py -q` | 55 passed in 7.46s; exit 0 |
| `tests/tests/platform/test_config_containment.py -q` | 11 passed in 4.65s; exit 0 |
| `tests/tests/platform/test_base_platform_service.py tests/tests/platform/test_service_container.py -q` | 9 passed in 0.92s; exit 0 |
| `tests/tests/executive -q` | 7 passed in 1.00s; exit 0 |
| `tests/tests/tools -q` | 119 passed in 5.20s; exit 0 |
| `tests/tests/integration/test_run_jaos_launcher.py tests/tests/integration/test_run_jaos_banner.py tests/tests/integration/test_shell_shutdown_lifecycle.py -q` | 17 passed in 1.82s; exit 0 |
| `tests/tests/platform/test_platform_runtime.py tests/tests/platform/test_platform_runtime_lifecycle.py tests/tests/platform/test_boot_manager.py tests/tests/platform/test_fortress_03_lifecycle_closure.py -q` | 47 passed in 1.78s; exit 0 |
| `tests/tests/composition/test_platform_composition.py tests/tests/composition/test_canonical_composition_invariants.py -q` | 24 passed in 4.81s; exit 0 |
| `tests/tests/platform -q` | 399 passed, 1 skipped in 339.59s (0:05:39); exit 0 |
| `tests/tests/composition -q` | 49 passed in 8.61s; exit 0 |
| `tests/tests/integration -q` | 17 passed in 1.68s; exit 0 |
| `tests/tests -q` | 1780 passed, 1 skipped in 333.43s (0:05:33); exit 0 |
| `. --collect-only -q` | 1781 tests collected in 5.08s; exit 0 |
| `.venv/Scripts/python.exe -B -m ruff check --no-cache tests/tests/platform/test_collection_containment.py tests/tests/platform/test_canonical_import_boundary.py` | All checks passed; exit 0 |


The initial full configured run exited 0 with **1,779 passed / 2 skipped**.
Besides the existing symlink skip, the unchanged junction test skipped because
Windows denied creation of the `cmd` subprocess (`WinError 5`, before a
`mklink /J` result). That same case passed in the platform aggregate and then
passed in isolation with a fresh external basetemp (**1 passed**, exit 0).
The precise cause of the intermittent Windows process denial was not established;
no production or junction-test change was made. The initial Ruff gate exited 1
with eleven ISC004 implicit-string-concatenation findings in the new constants.
Only two constant layouts were rewritten; whole-module AST equality was checked.
Ruff and the two workflow cases passed after correction, then the configured
suite, root collection and Ruff were rerun. The table records successful/latest
ladder results; earlier logs, including both skip reasons and the Ruff failure,
are preserved under `initial_*` in the external evidence directory. Earlier
subsystem results precede that AST-identical formatting correction. The subsequent
final-tree configured run covers every configured case after documentation edits.


Collection reconciles as **1,779 + 2 = 1,781**, with exactly the two new workflow
node IDs and **zero removed IDs**. The 1,779-ID baseline is the historical
Executive-checkpoint collection log, not a rerun. The executed configured suite
is **1,780 passed / 1 skipped**. The unchanged skip is
`test_profile_symlink_escape_is_rejected`: Windows directory symlink privilege
unavailable (`WinError 1314`). No test warning summary was reported.

Scope is **22 logical task paths**: nine originals, nine archive destinations,
two Python tests and these two architecture documents. An external normalized
`git diff --no-index --find-renames=100% --rename-empty` review reports **nine
R100** moves, equivalent to **13 task Git records** including four modifications.
Ordinary unstaged Git represents the moves as deleted sources and untracked
archives; the real index remains empty. No staging, commit or push occurred.
Protected state, project-state documents, brain/core/memory/main.py, canonical
production, compatibility abstractions, excluded debt, skills and Graphify
artifacts remain unchanged. The task does not perform reset, restore, clean,
Graphify, WorkflowEngine execution, excluded flat-script execution or quarantined
test execution.

**RAA-003 remains OPEN. RAA-009 remains OPEN — DEFERRED. F06E remains IN PROGRESS.**
F06F, F06G, F06H and F07-F12 remain NOT STARTED. Project-state synchronization is
reserved for a separately approved checkpoint. Earlier sections retain historical
counts and boundaries; this section records the workflow slice only.

### 29.1 Exact nine-source baseline and archive inventory

All rows have original/archive Git mode `100644`; CRLF = LF = CR counts.

| Original | Exact archive | Checkout SHA-256 | Normalized Git blob | Bytes | CRLF |
|---|---|---|---|---:|---:|
| `workflow/__init__.py` | `legacy_quarantine/production/workflow/__init__.py.legacy` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` | 0 | 0 |
| `workflow/automation_rules_engine.py` | `legacy_quarantine/production/workflow/automation_rules_engine.py.legacy` | `50a6b99cf56a92f8aaedeed18413156714358ac06f87abf8e4c0c4261b0c4369` | `b03024da5a009254a3fd842912dc9a67eeebfe76` | 875 | 49 |
| `workflow/dependency_manager.py` | `legacy_quarantine/production/workflow/dependency_manager.py.legacy` | `f65961110fcb376ab20479892b6042a7726f0d0990bc034142b4d9acb43d65b5` | `0e257fe976c380b202a465f4afdb0259d238d853` | 1072 | 58 |
| `workflow/retry_recovery_engine.py` | `legacy_quarantine/production/workflow/retry_recovery_engine.py.legacy` | `871c387aefda2b8e016c202eb3390bcd5cee8477f2fc92976ed76e8bd704a2de` | `ad5cac211d5e23205b52eb825208779509e9d49a` | 878 | 49 |
| `workflow/scheduler.py` | `legacy_quarantine/production/workflow/scheduler.py.legacy` | `d465c29cdb6c6dbea6c448a66fff33a0b3d6c9cabaf374819b732557d40d575c` | `46c4279e9d1bd1599c6711f79e40cbcc619a5851` | 877 | 49 |
| `workflow/task_manager.py` | `legacy_quarantine/production/workflow/task_manager.py.legacy` | `8221c2a258bb7114019a6882e0be4a527c2895f269eea1e5243443f563106f08` | `4dc03367e039160cd78f9415acd4d88c354a4b61` | 1086 | 58 |
| `workflow/task_queue.py` | `legacy_quarantine/production/workflow/task_queue.py.legacy` | `913b4a80557b1a00a2e7d1746675962990bfd83ab9cee9fee74d835a60f6889d` | `74bfa035e2f9d935493d9a85b63fbb9265a374c0` | 1129 | 61 |
| `workflow/workflow_engine.py` | `legacy_quarantine/production/workflow/workflow_engine.py.legacy` | `bc27c5c52027549d24f2c7407f82aeb1a8b87cccad8109314f16a0122d87226f` | `cb1d36997a7a980a01841bc08e32ad076c5e64f8` | 1218 | 42 |
| `workflow/workflow_monitor.py` | `legacy_quarantine/production/workflow/workflow_monitor.py.legacy` | `2d54c51fb9376fbc5638f6a11649d7d0b192d9e174fed83e4a96bc8fd4b88ea9` | `a6a22ff72607133e586aedbae57b30700d99050d` | 834 | 45 |

---

## 30. FORTRESS-06E Approved Partial Core Quarantine

Date: 2026-09-28. Scope: **CONTROLLED IMPLEMENTATION — partial core only**.
Baseline branch: `phase8-ai-intelligence`; HEAD and origin tracking ref:
`fe170c639428cc6baf3549be92b984781d362305`. The approved 18-source inventory
matched the supplied checkout SHA-256 values, the immutable HEAD blobs and
100644 modes, sizes and EOL evidence before moving. Destinations were absent;
no unexpected core artifacts or reparse points were present. The index was empty.
The eight named, already-modified protected tracked files were snapshotted and
preserved, along with unrelated tooling/untracked state.

Exactly **18 sources are archived and 16 sources remain live**. Every mapping is
`core/<name>.py -> legacy_quarantine/production/core/<name>.py.legacy`.
Moves preserve bytes, checkout SHA-256, normalized Git blob, size, CRLF/LF/CR
counts, mode and hierarchy. The earlier `core/kernel.py.legacy` is unchanged.
No wrapper, stub, shim, re-export, replacement implementation or importable
quarantine payload was introduced.

The 16 retained live files under `core/` are:
`__init__.py`, `action_history.py`, `backup_manager.py`, `command_system.py`,
`config_manager.py`, `diagnostics.py`, `engine.py`, `error_handler.py`,
`event_system.py`, `health_monitor.py`, `module_loader.py`, `plugin_manager.py`,
`recovery_manager.py`, `snapshot_manager.py`, `status_manager.py`, and
`version_manager.py`. Their bytes are pinned by the reconstructed historical
inventory. Exactly 16 retained `.pyc` files remain byte-identical; all 18
candidate caches remain absent. No bytecode was generated or deleted.

Static caller scans before and after the move agree: **0 canonical production,
0 canonical launcher closure, 0 external supported production, 0 configured-test,
0 retained-core and 0 tooling/dev callers** into the retired subset. There are
no literal lazy/registration targets into it. The 18 candidates have zero
internal edges. Sixteen excluded flat files retain exactly sixteen direct
imports, pinned by statement and file SHA; they were not executed. Archived
historical references remain unchanged (zero imports into this subset).

Static canonical closure from `run_jaos.py -> JAOSApplication ->
PlatformRuntime / BootManager -> PlatformComposition -> canonical platforms`
remains **207 files / 206 modules**, with zero violations and no workflow or
retired-core reachability. This is static evidence, not live-runtime certification.

The four direct F06F-sensitive writers remain live and unchanged:
`core/action_history.py`, `core/backup_manager.py`, `core/config_manager.py`,
and `core/snapshot_manager.py`. No writer or F06F responsibility was migrated.
`main.py -> core.engine` and the retained engine dependency graph are unchanged;
their later F06F/F06G disposition is unresolved.
Canonical authority remains `ExecutiveController -> ExecutivePlanner ->
ExecutionCoordinator -> ToolManager -> ToolExecutionEngine ->
ToolPermissionManager -> ToolApprovalManager -> tool.execute -> ToolAuditLogger`.
Owner hashes and permission-before-approval-before-execution/audit checks remain
in force. No canonical production code changed.

Only `tests/tests/platform/test_collection_containment.py` changed for Python
tests. It adds exactly two grouped cases:
`test_f06e_partial_core_archive_fidelity` and
`test_f06e_partial_core_caller_writer_authority_containment`.
The existing 34-source historical core guard remains intact through
**16 retained live + 18 exact archives**, using its original
`f1b1c574626a8e8c0188f1d8c340cecdf5087eb8e423ad77971a2656a523294c` digest.
The shared core archive directory is checked against the exact union of the
previous kernel leaf and the 18 additions. No old configured node is removed.

`tests/tests/platform/test_config_containment.py` is byte-identical, SHA-256
`d862bd601301ae7bfc85aa16a5cc9f31e5f77b23bc54e84689a4276a5a2a447c`:
**9 definitions / 11 statically identifiable cases**, all still valid against
live `core.config_manager`. The canonical import-boundary test is unchanged.

Classification stays **A=10, B=1, D=4, E=15, F=3, TOTAL=33**. D membership is
exactly **brain/, core/, main.py, memory/**. Core remains D; no partial-core E
entry is created. **RAA-003 OPEN; RAA-009 OPEN — DEFERRED; F06E IN PROGRESS;
F06F NOT STARTED; F06G/F06H NOT STARTED; F07-F12 NOT STARTED.**

The first regression ladder below was actually executed after the source/test
changes and before these documentation edits. No results or verification claims
were added to the manifest before that ladder passed. All pytest commands use
`.venv/Scripts/python.exe -B -m pytest -p no:cacheprovider -p anyio.pytest_plugin`,
`PYTHONDONTWRITEBYTECODE=1`, `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, and a different
external `--basetemp` for every invocation. Full commands, output, exit codes and
durations are preserved in
`%LOCALAPPDATA%/Temp/jaos-f06e-core-20260928-a81b/<gate>.json` and `<gate>.log`.
No repository-local temp/cache was used. Ruff also used `--no-cache`.

| Gate | Exact target arguments after the common prefix | Observed result |
|---|---|---|
| 01-core | `tests/tests/platform/test_collection_containment.py::test_f06e_partial_core_archive_fidelity tests/tests/platform/test_collection_containment.py::test_f06e_partial_core_caller_writer_authority_containment -q` | 2 passed in 24.24s; exit 0 |
| 02-collection | `tests/tests/platform/test_collection_containment.py -q` | 56 passed in 330.83s (0:05:30); exit 0 |
| 03-import | `tests/tests/platform/test_canonical_import_boundary.py -q` | 55 passed in 6.46s; exit 0 |
| 04-config | `tests/tests/platform/test_config_containment.py -q` | 11 passed in 4.20s; exit 0 |
| 05-inventory | `tests/tests/platform/test_runtime_state_inventory.py tests/tests/platform/test_runtime_state_inventory_enrichment.py -q` | 49 passed in 1.85s; exit 0 |
| 06-launcher | `tests/tests/integration/test_run_jaos_launcher.py tests/tests/integration/test_run_jaos_banner.py tests/tests/integration/test_shell_shutdown_lifecycle.py -q` | 17 passed in 2.22s; exit 0 |
| 07-runtime | `tests/tests/platform/test_platform_runtime.py tests/tests/platform/test_platform_runtime_lifecycle.py tests/tests/platform/test_boot_manager.py tests/tests/platform/test_lifecycle_state.py tests/tests/platform/test_fortress_03_lifecycle_closure.py -q` | 88 passed in 1.92s; exit 0 |
| 08-platform | `tests/tests/platform -q` | 401 passed, 1 skipped in 358.87s (0:05:58); exit 0 |
| 09-invariants | `tests/tests/composition/test_canonical_composition_invariants.py -q` | 16 passed in 4.96s; exit 0 |
| 10-composition | `tests/tests/composition -q` | 49 passed in 5.76s; exit 0 |
| 11-integration | `tests/tests/integration -q` | 17 passed in 1.51s; exit 0 |
| 12-full | `tests/tests -q -rs` | 1782 passed, 1 skipped in 356.79s (0:05:56); exit 0 |
| 13-explicit-root | `. --collect-only -q` | 1783 tests collected in 4.57s; exit 0 |
| 14-ruff | `ruff check --no-cache tests/tests/platform/test_collection_containment.py` | All checks passed; exit 0 |
| 15-diff | `git diff --check` | Clean; no whitespace errors; exit 0 |

Pre-change configured collection at the repository root was rerun: **1,781 node IDs**. Post-change collection
is **1,783**, reconciled as **1,781 + exactly two new IDs - zero removed IDs**.
The first configured full run is **1,782 passed / 1 skipped**. The unchanged
skip is the Windows directory-symlink privilege case; no test was weakened.
The required final-tree rerun after these documentation edits is recorded
separately in `final-*.json` / `final-*.log` and the implementation completion
report; the table above is explicitly the first ladder, not a claim about a
future run.

Task scope is 18 original paths + 18 archive paths + one test + two architecture
documents = **39 logical paths**. Git rename review uses disposable external
before/after trees and `git diff --no-index --find-renames=100%`; it does not
write or stage the repository index. The observed result is 18 R100
plus three modified files (21 records). Pre-existing protected modifications and unrelated
tooling remain outside this task scope. Project-state summary documents,
protected runtime data and canonical production remain unchanged. Nothing was
staged, committed or pushed. No legacy launcher/demonstration, excluded flat
test, archive payload or Graphify command was executed. This slice does not
authorize the next root or any later workstream.


### 30.1 Exact archive fidelity inventory

Each file has Git mode `100644`. EOL values below are equal counts for
CRLF, LF and CR (no lone CR or LF). The byte counts and SHA-256 values are the
approved checkout identities; Git blobs are normalized original-path identities.

| Original source | Exact archive destination | Bytes | CRLF/LF/CR | Checkout SHA-256 | Git blob |
|---|---|---:|---:|---|---|
| `core/action_queue.py` | `legacy_quarantine/production/core/action_queue.py.legacy` | 1057 | 60 | `7db0adc7a0e50b8092260e9ae55bc0c67a9327c3d8ac08e8ffcc56de2dec17d8` | `a3bdcbd2000e6d4e33484305b4fedca3d1cda2b8` |
| `core/agent_manager.py` | `legacy_quarantine/production/core/agent_manager.py.legacy` | 724 | 39 | `13ecc5c521551b4f52310a22e47c90984b813908637f724b25d5821a916fee93` | `ac314843df10dac30edf142b1a32d8b84e06f1c7` |
| `core/capability_registry.py` | `legacy_quarantine/production/core/capability_registry.py.legacy` | 919 | 41 | `356c33c54830a510d7b4dc6a458ac1e3fba80e74c8551be36da0a9d803ec0069` | `000f3f498b7a5c0e6340b370ab75fd52c58d9b5f` |
| `core/context_manager.py` | `legacy_quarantine/production/core/context_manager.py.legacy` | 811 | 45 | `ade44f59667eca2586261f74526a65b920db5f4c9e90a5e75ef59a3ca19699f7` | `2b248dbcffe89d879a154dbeb41c02b91ad9d066` |
| `core/explain_action.py` | `legacy_quarantine/production/core/explain_action.py.legacy` | 903 | 43 | `9795f10cbae8e7280869e61370d724f801dd23e22eaa07fd76878937620a86ac` | `e0ef7a7e19f361184eb35c7e402d445097e954e3` |
| `core/memory_window.py` | `legacy_quarantine/production/core/memory_window.py.legacy` | 922 | 51 | `56b37751cc8118b4bac5b635aa5527b5beae8d0e209e927eb3e3e7841d5f47a9` | `d6ac230fc9b9bb30f3241a43524ca24bd2dfd5f7` |
| `core/notification_system.py` | `legacy_quarantine/production/core/notification_system.py.legacy` | 848 | 43 | `3bd41fffa7d9a9dca392f10b96071052ef1a1a229c4ce7c82e55f03de617ed51` | `9550eeae84328acf8e185829ba301c9e01335aa2` |
| `core/offline_mode.py` | `legacy_quarantine/production/core/offline_mode.py.legacy` | 737 | 40 | `a1efe85da75fca2f8263d9abbd1dae45226f885412825520efe3e58208802971` | `c9aa82ec058f88a6cbd409a78b32eea791b3d658` |
| `core/performance_monitor.py` | `legacy_quarantine/production/core/performance_monitor.py.legacy` | 913 | 49 | `ce65741ce54da7c1f3b0f5bab33137d3260d9d1174d810bbec79cfaaa27737ae` | `21a4a53dfdb3e5ca6518a93f24c11f3e7c8cfc42` |
| `core/permission_system.py` | `legacy_quarantine/production/core/permission_system.py.legacy` | 762 | 35 | `369307fa88a20ad3b4acea3a65b31af09cabbc3b9c4e633337076efb1d5bb9dc` | `84f08e2cc2ccd0c6543387d71dc7841d55e1cf05` |
| `core/recovery_tracker.py` | `legacy_quarantine/production/core/recovery_tracker.py.legacy` | 812 | 41 | `5e2aafe134566ed2db05d83ad181fd2adca709e3e2b51427be95c8a01569072c` | `6baeedb2d66e098897c8e62720abd18490719b6e` |
| `core/resource_manager.py` | `legacy_quarantine/production/core/resource_manager.py.legacy` | 708 | 37 | `7755a8f5bc3b1ad18d49c2e69cd5345b9a3c62fadcfbb124f0c54fb147dd5a8f` | `f8573a1c3af13bbafd55b8c02f2606bf5fef8f25` |
| `core/scheduler.py` | `legacy_quarantine/production/core/scheduler.py.legacy` | 713 | 41 | `92b164e16980a9b24b37781a0f857f440eb72e2075d5e7cb99cdffcaf1a48339` | `2e11a69cb559f6ca56b9a45e48088fe2c0d21560` |
| `core/session_manager.py` | `legacy_quarantine/production/core/session_manager.py.legacy` | 1303 | 64 | `fc762e7b833ec96f99065cd3dde8cacbd8459a55584d68a490d7f83a87ef978e` | `5324f2e55277ee9e8d80448694768bb0ef00f498` |
| `core/state_manager.py` | `legacy_quarantine/production/core/state_manager.py.legacy` | 502 | 29 | `7b58d7e92d1e9228a683c9183da89a45b73284353c7ced77fd9daf72387a956a` | `03e9e0be2c8e28213f80b08e8990889ef5e613d1` |
| `core/task_manager.py` | `legacy_quarantine/production/core/task_manager.py.legacy` | 704 | 41 | `18e856500ce2ea7bdb2d84083bd7089e4675d345db89b75a62b3fc90ddc01415` | `0a54aedd97712466ee232ee36838d91b2fe53853` |
| `core/thread_manager.py` | `legacy_quarantine/production/core/thread_manager.py.legacy` | 896 | 50 | `c20d908ccdb2323a575a639eeb3dc00cae957f5d277af7eb1e070f89a696fee0` | `a4b714b8adf15aa3b898c97ae014557ebe48dbc9` |
| `core/transparency_layer.py` | `legacy_quarantine/production/core/transparency_layer.py.legacy` | 664 | 34 | `6f05f411158e43c295f8f57aec9e465493f1f1605403981e4d0d34e624d7d036` | `1d676e85d163e5c34fdcfbff5840f588a7a8f974` |


### 30.2 Retained writer and launcher identities

| Retained source | Checkout SHA-256 |
|---|---|
| `core/action_history.py` | `34ba99bfdf9520d12650cc56e0d522620abdec4555303d71e9f4b63e80a4bc30` |
| `core/backup_manager.py` | `0bde3faa0294ee6ea1df76332c776f01e6a82601a399925c51c7c320662ca013` |
| `core/config_manager.py` | `1bac73fa937da8534ef6e5a9dcbf26b521512dd835c22359063a1949b4789611` |
| `core/snapshot_manager.py` | `2b4dfc386821a081caf6bdb406315eab65edcd107a843e4b62eb2d19bdc40c09` |
| `core/engine.py` | `dbb3fbf0030016da5252aa294a7b36c96db11c0f3f1d15bf847a1b889fe01e51` |
| `main.py` | `4194f217f3a896519fed43979407df403a08fdfb3a12fe9d094aef98dba07596` |

---

## 31. Update History

| Date | Version | Change |
|---|---|---|
| 2026-09-28 | 1.27 | Partial core only: 18 exact archives, 16 retained live sources/caches, historical 34-source digest preserved, two grouped cases; first ladder 1,782 passed/1 skipped and 1,783 collected. Core remains D; classification unchanged; four F06F writers and main.py/core.engine untouched. RAA-003 OPEN; RAA-009 OPEN — DEFERRED; F06E IN PROGRESS; later slices NOT STARTED. |
| 2026-09-28 | 1.26 | Verified exact nine-source workflow quarantine, byte/SHA/blob/size/EOL/mode fidelity, zero live namespace/callers, nine singleton SCCs, compatibility consumers 0/0, preserved F06F writers and canonical authority, D=4/E=15/total=33. Full configured 1,780 passed/1 skipped; root 1,781; exactly two new cases; 22 logical paths; no staging. RAA-003 OPEN, RAA-009 OPEN — DEFERRED, F06E IN PROGRESS. |
| 2026-09-24 | 1.25 | Verified the final 36-source Executive root quarantine, exact byte/SHA/blob/size/EOL mapping, 91-source reconstruction, 55 internal edges/36 singleton SCCs, zero live callers, workflow production-caller-unblocked but untouched, compatibility consumers 1/0, ADR-0012/0013 preserved, and D=5/E=14/total=33. Full configured 1,778 passed/1 skipped; root 1,779; 76 logical paths; no staging. RAA-003 OPEN, RAA-009 OPEN — DEFERRED, F06E IN PROGRESS. |
| 2026-09-23 | 1.24 | Recorded the verified 42-source Executive tools family quarantine, exact byte/SHA/blob/size/CRLF fidelity, 42 R100 mappings, two grouped containment cases, zero outside callers, canonical Tool ownership, 36 preserved Executive sources, unchanged workflow/config/protected state, and D=6/E=13/total=33. Full configured 1,776 passed, 1 skipped; root collection 1,777. No legacy capability executed; F07/F11 NOT STARTED; RAA-003 OPEN; F06E IN PROGRESS. |
| 2026-09-23 | 1.23 | Recorded the verified 13-source Executive AI/provider family quarantine with exact checkout SHA/size/CRLF and Git blob fidelity, two grouped containment cases, ADR-0014 canonical contract preservation, 78 remaining Executive sources (42 tools + 36 remaining), and unchanged D=6/E=13/total=33. Full configured 1,774 passed, 1 skipped; root collection 1,775. Canonical/config/protected state preserved; workflow blocked; RAA-003 OPEN; F06E IN PROGRESS; F09 NOT STARTED. |
| 2026-09-07 | 1.22 | Recorded the verified single-leaf core/kernel.py quarantine: exact checkout SHA/size and Git blob fidelity, RegistryManager external-root importers 1 -> 0 with six internal importers preserved, two containment cases, core remaining D, unchanged D=6/E=13/total=33, and no boundary-test edit. Full configured 1,772 passed, 1 skipped; root collection 1,773. Canonical/config/protected state preserved; workflow still blocked; RAA-003 OPEN; F06E IN PROGRESS. |
| 2026-09-07 | 1.21 | Recorded the verified 12-source kernel quarantine with checkout SHA/size and Git blob fidelity, 11 excluded files / 18 imports, two containment cases, D=6/E=13/total=33, preserved backup classification, and corrected stale summary counters. Full configured suite: 1,770 passed, 1 skipped; root collection: 1,771. Canonical/config/protected state preserved; RAA-003 OPEN; F06E IN PROGRESS. |
| 2026-09-06 | 1.20 | Recorded the verified engineering root quarantine: 13 Python sources / one historical Markdown artifact, exact 14-file checkout SHA/size and normalized blob map, 13 excluded files / 24 direct imports, five excluded dynamic registrations, two grouped containment cases, BasePlatformService legacy consumers 3 -> 2, and D=7/E=12 with 33 classifications. Full suite: 1,768 passed, 1 skipped; root collection: 1,769. Canonical/config/protected state preserved; RAA-003 OPEN and F06E IN PROGRESS. |
| 2026-09-06 | 1.19 | Recorded the verified four-root, 29-source dashboard/knowledge/security/system_services quarantine, exact byte/SHA/blob fidelity, excluded-only dynamic adjudication and 29/50 direct plus five-registration debt. Preserved all containment boundaries and synchronized exact classification membership to D=8/E=11, total 33. Full suite: 1,766 passed, 1 skipped; root collection: 1,767. RAA-003 OPEN; F06E IN PROGRESS. |
| 2026-09-05 | 1.18 | Recorded the verified 24-source development/infrastructure/pc_control production quarantine, exact byte/blob fidelity, two containment cases, and the narrowly reconciled classification guard: D=12/E=7, total 33. Configured regression: 1,764 passed, 1 skipped; root collection: 1,765. Canonical and protected state remain unchanged; RAA-003 stays OPEN and F06E stays IN PROGRESS. |
| 2026-09-01 | 1.17 | Recorded the FORTRESS-06E communication production-root quarantine pilot as IMPLEMENTED AND VERIFIED: moved six zero-caller, non-writer sources into exact byte/blob-identical non-Python archives; updated the classification from live quarantine candidate to archive-only preservation; added two containment cases; retained seven excluded flat-test references as F06G/F06H debt; preserved canonical production, `jaos/`, `jaos_platform/`, and the 11-case config-containment gate; reconciled root collection as 1,761 + 2 = 1,763; and verified 1,762 passed with 1 skip. F06E remains IN PROGRESS and RAA-003 remains OPEN. |
| 2026-08-31 | 1.16 | Recorded FORTRESS-06D core/kernel shadow-runtime test retirement as IMPLEMENTED AND VERIFIED: retired 2 configured files / 6 collected source tests into byte/blob-identical `.py.legacy` archives without behavior ports or production changes; added exactly 2 containment cases; achieved 3 -> 1 legacy-facing files while configured `executive_brain` importers remained 0; preserved the 11-case config containment authority unchanged; reconciled root collection as 1,765 - 6 + 2 = 1,761; and verified 1,760 passed with 1 skip. The configured legacy-facing progression is now 67 -> 59 -> 52 -> 48 -> 44 -> 35 -> 19 -> 15 -> 13 -> 3 -> 1. RAA-003 remains OPEN and no later slice started. |
| 2026-08-31 | 1.15 | Recorded FORTRESS-06D satellite/runtime shadow-test retirement as IMPLEMENTED AND VERIFIED: retired 10 configured files / 30 collected source tests into byte/blob-identical `.py.legacy` archives without capability ports or production changes; added exactly 2 containment cases; achieved 13 -> 3 legacy-facing files while configured `executive_brain` importers remained 0; preserved config containment plus core/kernel tests for later separate work; reconciled collection as 1,793 - 30 + 2 = 1,765; and verified 1,764 passed with 1 skip. RAA-003 remains OPEN and no later slice started. |
| 2026-08-31 | 1.14 | Recorded ADR-0014 provider retirement as IMPLEMENTED AND VERIFIED: added 3 configured canonical provider-neutral tests before retiring 2 shadow-provider files / 20 collected cases into byte/blob-identical `.py.legacy` archives; added 2 containment cases; achieved 15 -> 13 legacy-facing files and 2 -> 0 configured `executive_brain` importers; reconciled root collection as 1,808 - 20 + 3 + 2 = 1,793; and verified 1,792 passed with 1 skip. The two unchanged excluded flat provider tests remain non-blocking legacy/facade debt outside configured `tests/tests` certification. Production provider sources, provider independence, credentials, network state, runtime data, F09, and RAA-003 remained unchanged. |
| 2026-08-31 | 1.13 | Added ADR-0014's Founder-approved provider disposition and F09 clarification: 2 configured files / 20 collected source tests against unreachable offline/mock-based shadow adapters; PORT + QUARANTINE approved after three provider-neutral canonical invariants receive configured coverage; current counts remain 15 legacy-facing files and 2 `executive_brain` importers, with 15 -> 13 and 2 -> 0 projected only after controlled implementation. Preserved provider independence, candidate-only OpenAI status, optional Ollama status, untouched production sources, F09 NOT STARTED, and RAA-003 OPEN. |
| 2026-08-31 | 1.12 | Recorded the ADR-0013-controlled Memory retirement as IMPLEMENTED AND VERIFIED: retired 4 configured files / 30 collected source tests into byte-identical `.py.legacy` archives, added 2 containment tests, achieved 19 -> 15 legacy-facing files and 6 -> 2 `executive_brain` importers, and reconciled root collection as 1,836 - 30 + 2 = 1,808. Full configured regression passed 1,807 with 1 skip; production Memory sources, canonical contracts, runtime data, and all deferred boundaries remained unchanged. |
| 2026-08-31 | 1.11 | Added ADR-0013's Founder-approved Executive WorkingMemory compatibility clarification and recorded the completed read-only Memory adjudication: 4 configured files / 30 source tests, all four governance-approved quarantine candidates, implementation not started, current counts unchanged at 19 legacy-facing files and 6 `executive_brain` importers, and projected post-implementation counts of 15 and 2. Preserved canonical persistent-Memory ownership, deferred Context/Experience/F08/F10 responsibilities, RAA-003 OPEN, RAA-009 OPEN — DEFERRED, and untouched legacy production sources. |
| 2026-08-31 | 1.10 | Recorded F06D2E as IMPLEMENTED AND VERIFIED: retired 16 prototype-tool files carrying 101 pytest-collectable source tests into byte/blob-identical `.py.legacy` archives without replacement capability tests; added two containment tests, reconciling root collection as 1,935 - 101 + 2 = 1,836; verified 35 -> 19 legacy-facing and 22 -> 6 `executive_brain` importer reductions; preserved four Memory and two provider importers and all 16 production prototypes for later work; and recorded no production change, external side effect, runtime writer, or data migration. Full configured suite passed 1,835 with 1 skip and Ruff passed. F06D and FORTRESS-06 remain in progress; RAA-003 remains open. |
| 2026-08-30 | 1.9 | Recorded F06D2D as IMPLEMENTED AND VERIFIED: canonical aggregate Executive metrics coverage added before 9 manager/registry files carrying 94 source tests were retired into byte/blob-identical `.py.legacy` archives; configured legacy-facing files reduced 44 -> 35 and `executive_brain` importers 31 -> 22; 16 F06D2E, 4 Memory, and 2 provider importers remain unchanged. No production code or runtime data changed; RAA-003 remains open. |
| 2026-08-30 | 1.8 | Recorded ADR-0012's Founder-approved manager/registry responsibility clarification and F06D2D's exact 9-file / 94-source-test adjudication, approved technical retirement plan, aggregate Executive metrics prerequisite, unchanged current counts of 44 legacy-facing files and 31 `executive_brain` importers, projected 44 -> 35 and 31 -> 22 impact, and implementation-not-started boundary. RAA-003 remains open; no test or production source moved. |
| 2026-08-30 | 1.7 | Recorded F06D2C's exact 4-file / 22-source-test ExecutiveBrain and pipeline retirement, four byte/blob-identical `.py.legacy` archives, two canonical source tests, three containment checks, corrected in-memory writer finding, 48 -> 44 legacy-facing reduction, and 35 -> 31 `executive_brain` importer reduction. Full configured suite 2,025 passed, 1 skipped; repository-root collection found 2,026 tests; Ruff passed. F06D2C is IMPLEMENTED AND VERIFIED; F06D and FORTRESS-06 remain in progress. |
| 2026-08-30 | 1.6 | Recorded F06D2B's four-file Tool Platform core test adjudication, byte-identical archives under `legacy_quarantine/tests/tools/core/` with SHA-256 and Git blob evidence, 19 canonical `jaos.tools` replacement tests, 10 dropped legacy requirements, 3 recorded non-FORTRESS-07 observations, and the 52 -> 48 legacy-facing reduction (39 -> 35 `executive_brain` importers). Synchronized F06D2A to its committed checkpoint `95adce4`. FORTRESS-06 remains in progress, F06D is not complete, and F06D2C+ remains not started. |
| 2026-08-25 | 1.5 | Recorded F06D2A's seven-file filesystem-tool test migration, byte-identical archives, 59 -> 52 legacy-facing reduction, and verification evidence; synchronized F06D1 to its committed checkpoint `51818d2`. FORTRESS-06 remains in progress, F06D is not complete, and F06D2B+ remains not started. |
| 2026-08-25 | 1.3 | Synchronized F06C current-state wording with committed and pushed checkpoint `0a2ea60`; FORTRESS-06 remains in progress, F06D+ remains not started, and certification gates remain unchanged. |
| 2026-08-25 | 1.2 | Recorded F06C's verified injected CLI adapters, canonical lifecycle ownership, exact verification evidence, and RAA-007 resolution. FORTRESS-06 remains in progress and F06D+ remains not started. |
| 2026-08-25 | 1.1 | Recorded F06B's exact two-artifact non-Python archive move, importlib pytest configuration, collection-collision remediation, and unchanged stop boundary. |
| 2026-08-25 | 1.0 | Created the authoritative F06 classification and canonical import-guard contract. No legacy source or runtime data moved. |
