# JAOS Architectural Unification & Runtime Hardening

Document ID: GOV-FORTRESS-01

Program Name: JAOS Architectural Unification & Runtime Hardening ("Fortress Program")

Document Version: 1.20

Certified Repository Baseline: v0.9.0-alpha

Development Target: v0.10.0-alpha

Status: In Progress

Owner and Approval Authority: Founder Vinay B

Maintainer: JAOS Engineering

Founder Direction Recorded: 2026-08-21

Last Updated: 2026-08-31

Related Documents:

- `JAOS_MANIFEST.md`
- `docs/architecture/ARCHITECTURE_DECISIONS.md`
- `docs/architecture/ARCHITECTURE_GOVERNANCE.md`
- `docs/architecture/FORTRESS_06_LEGACY_QUARANTINE_MANIFEST.md`
- `docs/project/ROADMAP.md`
- `docs/project/MILESTONES.md`
- `docs/project/PHASE8_MILESTONES.md`
- `docs/engineering/RUNTIME_ARCHITECTURE_AUDIT.md`
- `docs/engineering/BUG_FIXING_AND_REGRESSION_REPORT.md`

---

## 1. Purpose

The Fortress Program is the mandatory governance, architecture, runtime
hardening, validation, and certification gate that JAOS must pass before major
Phase 8 intelligence expansion may resume.

The approved engineering intent is:

> Every production JAOS capability must be reachable, tested,
> permission-controlled, observable, recoverable, replaceable, and auditable.

Fortress is a controlled continuation of repository stabilization. It does not
erase, rename, reopen, or retrospectively rewrite completed audits,
certifications, releases, or stabilization evidence.

---

## 2. Founder-Approved Hard Gate

The Fortress Program is mandatory. Major capability expansion must remain
paused until Fortress certification is complete and explicit authorization to
resume is recorded.

The pause includes:

- advanced reasoning expansion;
- autonomous workflows;
- multi-agent runtime behavior;
- advanced memory-driven action;
- PC control;
- voice;
- vision;
- IoT;
- robotics; and
- future cloud-GPU execution.

This gate does not reassign those capabilities to different roadmap phases. It
prevents their expansion until the shared production foundation is certified.

Phase 8 may not resume merely because an individual Fortress workstream is
implemented, a test suite passes, or a prior phase remains certified. Resume
requires all of the following:

1. Step 7 is complete and approved.
2. Step 8 Stabilization Certification is complete.
3. FORTRESS-01 through FORTRESS-12 are complete with current evidence.
4. Fortress certification is recorded.
5. Explicit Founder authorization to resume major Phase 8 expansion is
   recorded.

---

## 3. Current Program and Stabilization State

| Item | Current state |
|---|---|
| Fortress Program | ACTIVE — mandatory hard gate |
| FORTRESS-01 | IMPLEMENTED — governance baseline recorded |
| FORTRESS-02 | COMPLETE AND VERIFIED |
| FORTRESS-02G | AUDIT COMPLETE |
| FORTRESS-02H | IMPLEMENTED AND VERIFIED |
| FORTRESS-02I | IMPLEMENTED AND VERIFIED |
| FORTRESS-02J | IMPLEMENTED AND VERIFIED |
| FORTRESS-02K | CLOSURE EVIDENCE COMPLETE |
| FORTRESS-03 | COMPLETE AND VERIFIED |
| FORTRESS-04 | COMPLETE AND VERIFIED |
| FORTRESS-05 | COMPLETE AND VERIFIED — ADR-0011 CONTRACT SATISFIED |
| FORTRESS-06 | IN PROGRESS — THROUGH F06D2E IMPLEMENTED AND VERIFIED |
| FORTRESS-06A | IMPLEMENTED AND VERIFIED — COMMITTED AND PUSHED AT `92aa9d7` |
| FORTRESS-06B | IMPLEMENTED AND VERIFIED — COMMITTED AND PUSHED AT `eea8190` |
| FORTRESS-06C | IMPLEMENTED AND VERIFIED — COMMITTED AND PUSHED AT `0a2ea60` |
| FORTRESS-06D1 | IMPLEMENTED AND VERIFIED — COMMITTED AND PUSHED AT `51818d2` |
| FORTRESS-06D2A | IMPLEMENTED AND VERIFIED — COMMITTED AND PUSHED AT `95adce4` |
| FORTRESS-06D2B | IMPLEMENTED AND VERIFIED — COMMITTED AND PUSHED AT `0ea8e2e` |
| FORTRESS-06D2C | IMPLEMENTED AND VERIFIED — COMMITTED AND PUSHED AT `1862f78` |
| FORTRESS-06D2D | IMPLEMENTED AND VERIFIED |
| FORTRESS-06D2E | IMPLEMENTED AND VERIFIED |
| FORTRESS-06D Memory adjudication | READ-ONLY AUDIT COMPLETE — ADR-0013 ACCEPTED — IMPLEMENTATION NOT STARTED |
| Later FORTRESS-06D slices | NOT STARTED |
| FORTRESS-07 | NOT STARTED |
| Step 7 — Bug Fixing and Regression | IN PROGRESS |
| RAA-002 | PARTIALLY RESOLVED |
| RAA-003 | OPEN |
| RAA-005 | RESOLVED WITH EVIDENCE |
| RAA-007 | RESOLVED WITH EVIDENCE |
| RAA-008 | RESOLVED WITH EVIDENCE |
| RAA-009 | OPEN — MEMORY-CONTEXT ADAPTER DEFERRED |
| Other unresolved RAA findings | REMAIN UNRESOLVED |
| Step 8 — Stabilization Certification | NOT STARTED — BLOCKED BY STEP 7 |
| Fortress certification | NOT STARTED |
| Phase 8 major expansion | PAUSED |

FORTRESS-01 records governance and the canonical target. It does not prove that
the target is implemented, integrated, tested, ready, healthy, or certified.

The Founder-approved FORTRESS-02 runtime-path architecture decision is recorded
in ADR-0010. This decision fixes the design boundary only. It does not implement
`RuntimePaths`, `RuntimePathResolver`, runtime composition, test isolation, or
legacy-data migration, and it does not authorize production-code or test
changes.

Implementation of each completed workstream proceeded under separate
authorization. FORTRESS-02 through FORTRESS-05 are COMPLETE AND VERIFIED at
workstream level. FORTRESS-05 satisfies the narrow ADR-0011 carve-out; its
Conversation authority remains intentionally unrouted. The overall Fortress
Program is not certified. FORTRESS-06 is in progress through the separately
authorized F06D2E prototype-tool shadow-test retirement. F06B moved
only two unsupported root test-shaped scripts as byte-identical non-Python
archives, F06C made the canonical CLI surfaces injected adapters, F06D1
quarantined eight duplicate AI and Core configured tests, F06D2A replaced
seven configured filesystem-tool test files with canonical `jaos.tools`
coverage while archiving their legacy payloads, F06D2B did the same for four
configured Tool Platform core test files, and F06D2C retired four monolithic
ExecutiveBrain/pipeline configured files while adding two canonical Executive
source tests. ADR-0012 records the Founder-approved interpretation for F06D2D.
F06D2D added aggregate canonical Executive metrics coverage, then retired nine
manager/registry configured files carrying 94 source tests into byte-identical
non-Python archives. F06D2E retired 16 configured prototype-tool files carrying
101 source tests into byte/blob-identical non-Python archives without adding or
expanding browser, desktop, development, policy, or autonomous capability.
Configured legacy-facing files are now 19 and configured `executive_brain`
importers are six: four Memory tests and two deferred provider tests. The
read-only Memory adjudication found four files / 30 tests and ADR-0013 records
the Founder-approved supersession of exact legacy Executive `WorkingMemory`
compatibility. All four Memory tests are governance-approved quarantine
candidates, but implementation has not started and the current counts remain 19
and six. No legacy production source moved or was deleted, no runtime data
migrated, F06D is not complete, later implementation work has not started, and
major Phase 8 expansion remains paused.

---

## 4. Canonical Target Architecture

```text
run_jaos.py
    ->
PlatformRuntime
    ->
BootManager / runtime lifecycle
    ->
canonical Memory Platform
canonical AI Platform
canonical Executive
canonical Tool Platform
    ->
Permission / Risk / Approval
    ->
Audit
    ->
Tool Execution
```

`run_jaos.py` is the future sole thin production launcher.

`PlatformRuntime` is the Runtime Platform composition owner. `BootManager` owns
the governed runtime lifecycle beneath that composition root.

`CommandDispatcher` must become an injected interface adapter. It must not own
provider construction, platform startup policy, or an independent composition
root.

The permanent execution authority rule remains:

> Intelligence proposes; Executive executes.

Intelligence may reason, plan, rank, validate, and propose. It must not grant
permission, approve protected actions, or execute protected actions directly.

---

## 5. Canonical Components to Preserve

Controlled Fortress work must preserve and converge on:

- `run_jaos.py` as the future sole thin launcher;
- the `jaos_platform` Runtime Platform;
- `jaos.executive` as system-action authority;
- canonical `jaos.tools` as the controlled execution boundary;
- canonical `jaos.ai` as the provider-independent AI Platform;
- canonical `jaos.memory` as the persistent-memory authority; and
- `jaos.intelligence` proposal contracts without execution authority.

Certified public contracts and completed Phase 8 implementation must be
preserved unless a separately approved migration explicitly changes them.

---

## 6. Legacy Migration and Quarantine Rule

Legacy, duplicate, and shadow launchers, composition roots, providers, memory
systems, tool paths, permission systems, approval systems, audit paths, and
lifecycle systems must be inventoried, migrated, and quarantined through
controlled work.

This governance baseline does not authorize deletion. A legacy path may be
removed only after its callers, compatibility obligations, data, tests, and
rollback plan are known and the removal is separately authorized.

No migration bridge may become a permanent second production authority.

---

## 7. Ordered Fortress Workstreams

Workstreams must proceed in this order unless a later Founder-approved decision
records a safe dependency-preserving adjustment:

| Order | Workstream | Baseline status |
|---|---|---|
| 1 | FORTRESS-01 — Governance and canonical architecture | IMPLEMENTED — governance baseline recorded |
| 2 | FORTRESS-02 — Runtime-data and test isolation | COMPLETE AND VERIFIED — closure evidence recorded in section 7.7 |
| 3 | FORTRESS-03 — Runtime lifecycle correctness | COMPLETE AND VERIFIED — closure evidence recorded in section 7.8 |
| 4 | FORTRESS-04 — One launcher and one composition root | COMPLETE AND VERIFIED — closure evidence recorded in section 7.9 |
| 5 | FORTRESS-05 — Canonical platform composition | COMPLETE AND VERIFIED — ADR-0011 closure evidence in section 7.10 |
| 6 | FORTRESS-06 — Legacy migration and quarantine | IN PROGRESS — THROUGH F06C |
| 7 | FORTRESS-07 — Permission, approval, and audit hardening | PLANNED |
| 8 | FORTRESS-08 — Crash-safe persistence, rollback, and replay | PLANNED |
| 9 | FORTRESS-09 — Real provider resilience | PLANNED |
| 10 | FORTRESS-10 — Central health and graceful degradation | PLANNED |
| 11 | FORTRESS-11 — CI plus architecture/runtime/security/chaos tests | PLANNED |
| 12 | FORTRESS-12 — Repository cleanup and certification | PLANNED |

Workstream presence in this document is sequencing authority, not blanket
implementation authorization. Each workstream must enter through the existing
repository approval, change-control, evidence, and review process.

### 7.1 FORTRESS-02 Runtime-Path Architecture Decision

ADR-0010 establishes the mandatory design for the first FORTRESS-02
implementation slice:

- `jaos_platform` owns runtime-path resolution through the future immutable,
  typed `RuntimePaths` contract and `RuntimePathResolver`;
- the composition root resolves paths exactly once, in this order: explicitly
  injected `RuntimePaths`, an absolute `JAOS_RUNTIME_DIR`, then the
  operating-system local application-data default;
- the standard-library defaults are `%LOCALAPPDATA%\JAOS` on Windows,
  `$XDG_DATA_HOME/jaos` or `~/.local/share/jaos` on Linux, and
  `~/Library/Application Support/JAOS` on macOS;
- the versioned layout is `v1/profiles/<profile-id>/` with `config`, `memory`,
  `state`, `recovery`, `audit`, `logs`, `exports`, `backups`, `migrations`, and
  `tmp` scopes;
- the current single-user profile identifier is `default`; identifiers must
  match `^[A-Za-z0-9_-]{1,64}$` and must not permit absolute, drive-qualified,
  UNC, separator-containing, traversal, junction, or symlink escapes;
- production internal runtime state must not default inside the Git working
  tree, and an override resolving inside the repository must be rejected when
  repository context is known;
- `PlatformRuntime` will inject owned path scopes, `run_jaos.py` remains thin,
  and subsystems must not resolve roots or construct private repository-relative
  runtime paths;
- runtime paths do not authorize persistence of credentials, API keys,
  authorization material, or provider secrets outside the canonical secret
  boundary;
- existing repository data, exports, logs, snapshots, backups, profile state,
  configuration, and modified runtime JSON remain preserved legacy migration
  inputs; no deletion, movement, rewrite, untracking, automatic ingestion, or
  migration is authorized; and
- future tests must use function-scoped disposable roots with worker isolation,
  no repository writes during import or collection, practical external cache
  and bytecode placement, and clean-tree certification checks.

The initial implementation must use the Python standard library. `platformdirs`
is deferred unless later evidence establishes a need. Migration remains a
separately authorized, opt-in, copy-based, dry-run-capable, checksummed,
schema-aware, idempotent, crash-safe, reversible process with explicit approval
for sensitive user data.

This architecture decision does not begin FORTRESS-03, canonical runtime
composition changes, legacy deletion, Git untracking, data migration, or major
Phase 8 expansion. Implementation of the first FORTRESS-02 slice requires a
separate authorization.

### 7.2 FORTRESS-02 Slice State

FORTRESS-02 is COMPLETE AND VERIFIED following the FORTRESS-02K closure
evidence recorded in section 7.7. The following slices are implemented and
independently verified; the evidence sections that follow are retained as the
historical record of each slice.

| Slice | Scope | Status |
|---|---|---|
| FORTRESS-02A | RuntimePaths foundation | IMPLEMENTED AND VERIFIED |
| FORTRESS-02B | PlatformRuntime RuntimePaths ownership | IMPLEMENTED AND VERIFIED |
| FORTRESS-02C | test-state isolation foundation | IMPLEMENTED AND VERIFIED |
| FORTRESS-02D | runtime logging isolation | IMPLEMENTED AND VERIFIED |
| FORTRESS-02E | canonical Memory SQLite path binding | IMPLEMENTED AND VERIFIED |
| FORTRESS-02F | legacy runtime-state inventory foundation | IMPLEMENTED AND VERIFIED |
| FORTRESS-02G | legacy runtime-writer redirection audit (read-only) | AUDIT COMPLETE |
| FORTRESS-02H | canonical containment fixes | IMPLEMENTED AND VERIFIED |
| FORTRESS-02I | collection containment and architecture guards | IMPLEMENTED AND VERIFIED |
| FORTRESS-02J | legacy runtime-state inventory model extension | IMPLEMENTED AND VERIFIED |
| FORTRESS-02K | remaining FORTRESS-02 closure work | CLOSURE EVIDENCE COMPLETE |

Slice verification establishes implemented and verified behavior for the scope
listed above. It does not establish FORTRESS-02 completion, Fortress
certification, Step 8 entry, or authorization to resume major Phase 8
expansion. FORTRESS-02G requires separate authorization before it begins.

No legacy data was migrated, moved, rewritten, untracked, or deleted. The
existing `data/`, `config/`, `logs/`, and `exports/` trees remain preserved
legacy migration inputs under the section 6 rule and ADR-0010.

### 7.3 FORTRESS-02 Checkpoint Reconciliation Evidence

Date: 2026-08-21

Environment: Python 3.14.6, pytest 9.1.1, Windows.

Execution constraints applied: `PYTHONDONTWRITEBYTECODE=1`,
`-p no:cacheprovider`, and external disposable `--basetemp` roots outside the
repository. Excluded flat legacy tests were not run.

| Suite | Exit code | Result |
|---|---|---|
| `tests/tests/platform/test_runtime_paths.py` | 0 | 41 passed, 1 skipped |
| `tests/tests/platform/test_runtime_paths_integration.py` | 0 | 8 passed |
| `tests/tests/platform/test_test_state_isolation.py` | 0 | 13 passed |
| `tests/tests/platform/test_runtime_logging.py` | 0 | 12 passed |
| `tests/tests/memory/test_runtime_memory_binding.py` | 0 | 14 passed |
| `tests/tests/platform/test_runtime_state_inventory.py` | 0 | 16 passed |
| `tests/tests/platform` | 0 | 141 passed, 1 skipped |
| Memory regression set for 02E | 0 | 167 passed |

The Memory regression set comprised `test_provider_factory.py`,
`test_provider_platform.py`, `test_sqlite_store.py`, and
`test_sqlite_transaction.py`.

Protected-tree integrity: a SHA-256 manifest of all 161 files under `data/`,
`config/`, `logs/`, and `exports/` was captured before and after testing. Both
manifests hashed to
`6d58d221901282267b5856bfddb99c0fe70ba489ba8bfe8f32a80251e63e4675`, with no
added, removed, or modified files.

Repository artifact integrity: no SQLite database, WAL, or SHM file, no
pytest-cache entry, no new bytecode, and no migration or runtime-state artifact
was created inside the repository. The pre-existing artifact inventory of 2,021
paths was unchanged, and the working tree remained at its prior 38 entries.

Recorded environment constraint and unrun check: the directory-symlink escape
rejection test at `tests/tests/platform/test_runtime_paths.py:309` skipped with
`[WinError 1314] A required privilege is not held by the client`. Creating
directory symlinks on this host requires elevation. The test and its guard are
present and were not weakened, but the symlink-escape rejection path required by
ADR-0010 was not executed and is therefore not verified on this host. It must be
executed in an elevated or capable environment before Fortress certification.

### 7.4 FORTRESS-02G Through FORTRESS-02I Evidence

Date: 2026-08-21. Environment: Python 3.14.6, pytest 9.1.1, Windows.
Execution constraints for every run: `PYTHONDONTWRITEBYTECODE=1`,
`-p no:cacheprovider`, and external disposable `--basetemp` roots outside the
repository. Excluded flat legacy tests were never executed.

FORTRESS-02G recorded a read-only audit of the seventeen remaining
repository-relative runtime-state writers. One writer required a FORTRESS-02
change; the remainder are classified for FORTRESS-06 quarantine or
archive-only retention. No writer was modernized or migrated.

FORTRESS-02H closed the two canonical containment gaps the audit identified:

- `ConfigManager` no longer writes repository configuration. Repository
  `config/settings.json` is a read-only defaults source, and mutable settings
  are written only beneath an explicitly injected absolute profile path. A
  mutation without a profile target fails closed.
- `SQLiteProvider` and `create_sqlite_connection` reject relative database
  paths before any directory is created or any connection is opened. The
  pre-existing `":memory:"` path remains supported, and `from_memory_scope`
  behaviour is unchanged from 02E.

FORTRESS-02I established collection containment and two architecture guards:

- `tests/conftest.py` excludes the preserved legacy flat scripts beneath
  `tests/` before import, for `pytest`, `pytest tests/`, and `pytest .`.
- A session-scoped guard extends the opt-in FORTRESS-02C protection so no
  configured certification test can mutate `data/`, `config/`, `logs/`, or
  `exports/` undetected. It only reads, tolerates an already-dirty tree, and
  names the affected paths.
- The canonical import-boundary guard proves by AST analysis that the import
  closure of `run_jaos.py` depends on no legacy or shadow package identity.
- The internal path-literal guard proves canonical `jaos/` and
  `jaos_platform/` sources declare no repository-relative mutable
  runtime-state location.

Verified results, all exit code 0:

| Suite | Result |
|---|---|
| Configuration containment (02H) | 11 passed |
| SQLite path containment (02H) | 18 passed |
| Canonical import boundary (02I) | 10 passed |
| Internal path-literal guard (02I) | 20 passed |
| Collection containment (02I) | 12 passed |
| `tests/tests/platform` | 194 passed, 1 skipped |
| Full configured suite `tests/tests` | 1,807 passed, 1 skipped |

Protected-tree integrity: a SHA-256 manifest of all 161 files beneath `data/`,
`config/`, `logs/`, and `exports/` hashed to
`6d58d221901282267b5856bfddb99c0fe70ba489ba8bfe8f32a80251e63e4675` before and
after every run. No SQLite, write-ahead, pytest-cache, bytecode, migration, or
runtime-state artifact was created inside the repository.

Two limitations are recorded rather than resolved:

- Naming an excluded legacy file explicitly on the command line still imports
  it. pytest resolves a directly-specified argument to a module before
  consulting `pytest_ignore_collect`, and `--ignore` and `--ignore-glob`
  behave identically whether supplied on the command line or through
  `addopts`. No conftest-level mechanism prevents this, which is why
  `pytest.ini` was left unchanged and why certification commands must always
  target `tests/tests`. Executable evidence is retained in
  `tests/tests/platform/test_collection_containment.py`.
- `pytest .` exits 2 on a pre-existing repository-structure defect unrelated
  to Fortress: root-level legacy scripts import the production `brain`
  package, and because `tests/tests/` has no `__init__.py` while
  `tests/tests/brain/` has one, pytest names that test module
  `brain.test_executive_brain`. The failure was reproduced in a synthetic tree
  containing no conftest at all. Collection remains state-safe under all three
  invocations; only the exit code is affected. Root-level scripts sit outside
  the `tests/` boundary and belong to a later slice.

### 7.5 FORTRESS-02J Evidence

Date: 2026-08-21. Environment and execution constraints as in section 7.4.

FORTRESS-02J enriched the FORTRESS-02F read-only inventory so every artifact
declares who writes it, which topology reaches that writer, its Fortress
disposition, and whether it is isolated from the canonical path. The inventory
remains read-only and still imports no writer module.

Model additions: a `WriterReachability` enum, a `FortressDisposition` enum, an
immutable `RuntimeStateWriter` descriptor tuple per artifact, an artifact-level
`fortress_disposition` kept separate from the existing
`migration_disposition`, derived `reachability` and `reachable_from_run_jaos`
properties, and a separate `UnownedRuntimeStateLocation` record so unowned
directories are not forced into the artifact model.

Recorded facts: no artifact and no declared writer claims `RUN_JAOS`
reachability, so every legacy runtime-state writer is isolated from the
canonical path; `config/settings.json` carries `CONFIG_SPLIT`;
`config/providers.json` carries `DEFERRED_ARCHITECTURE_DECISION`; snapshots,
backups, exports, and the system log remain `ARCHIVE_ONLY`; no artifact is
marked `CANONICAL_EXTERNALIZED`, because nothing has been migrated — that value
appears only on the `ConfigManager` writer whose mutable write path
FORTRESS-02H externalized. `logs/system.log` declares no writer at all, which
is truthful after FORTRESS-02D removed its repository-relative default.

Silent-desynchronization risk is closed by a test-only AST cross-check that
compares each writer's class-level path constant against the inventory
declaration without importing the module. Eleven writers are statically
verifiable; three declare their paths method-locally
(`memory.memory_cleanup`, `core.snapshot_manager`, `core.backup_manager`) and
are recorded explicitly rather than parsed fragilely.

Deliberate exclusions, asserted by test: `scripts.generate_dg1_docs` is
recorded as an excluded developer writer and never as runtime state; and
`jaos.tools.filesystem` plus the `executive_brain.tools.file` shadow stack own
no artifact, because caller-supplied paths are not internal runtime state.
`data/cache` and `data/diagnostics` are recorded as unowned locations with
`NO_KNOWN_CALLER` and a deferred decision.

Verified results, all exit code 0:

| Suite | Result |
|---|---|
| Inventory enrichment (02J) | 33 passed |
| Legacy runtime-state inventory (02F) | 16 passed |
| Canonical import boundary (02I) | 10 passed |
| Internal path-literal guard (02I) | 20 passed |
| `tests/tests/platform` | 227 passed, 1 skipped |
| Full configured suite `tests/tests` | 1,840 passed, 1 skipped |

Protected-tree integrity: the 161-file manifest hashed to
`6d58d221901282267b5856bfddb99c0fe70ba489ba8bfe8f32a80251e63e4675` both before
and after testing, with no artifact, database, cache, bytecode, or migration
output added to the repository. `data/cache` and `data/diagnostics` remain
empty and untouched.

One test defect was found and fixed during this slice: an initial assertion
required the absence of legacy modules from `sys.modules` process-wide, which
other configured tests legitimately violate by importing `core`. It was
replaced with a delta assertion plus a static check that the inventory module
itself imports no writer.

The FORTRESS-02I limitations remain unchanged: a directly-named legacy test
path still imports that script, `pytest .` still exits 2 on the pre-existing
`brain` package-name collision, and the directory-symlink escape validation
remains unverified on this host.

### 7.6 FORTRESS-02K Closure Evidence — BLOCKED

Date: 2026-08-21. Environment and execution constraints as in section 7.4.

FORTRESS-02K executed the FORTRESS-02 closure evidence run. **FORTRESS-02 is NOT
closed. It remains IN PROGRESS.** One ADR-0010 acceptance criterion is
unsatisfied.

The governing acceptance criteria are ADR-0010 "Validation Required During
Implementation" and "Test Contract" together with the ADR-0010 Decision body.
Section 9 of this document is the PROGRAM-level certification rule over
FORTRESS-01 through FORTRESS-12 and is not a FORTRESS-02 workstream criterion.

**The single blocker.** ADR-0010 enumerates six rejection-test categories:
"Junction, symlink, traversal, drive, UNC, and separator rejection tests."
Traversal, path separators, drive-qualified paths, UNC paths, and absolute paths
are all covered and pass. A junction rejection test does not exist anywhere in
the repository. The implementation is correct — a junction profile escape was
empirically confirmed to raise "profile_root escapes its validated profile
scope" — but no committed regression test guards it, so a future regression
would go undetected. Directory junctions are creatable on this host without
elevation, so no host constraint excuses the gap. Resolving it requires separate
authorization and is not performed by this closure slice.

**Deliberately not blockers**, each with its recorded owner:

| Item | Decision | Owner |
|---|---|---|
| Directory-symlink escape test skipped on this host | Not a FORTRESS-02 blocker; test committed, retained, unweakened, skip disclosed with its exact error | FORTRESS-11 and Fortress certification environment |
| `pytest .` exits 2 on the pre-existing `brain` package-name collision | Not a FORTRESS-02 blocker; ADR-0010's Test Contract is stated in terms of repository state, and every state requirement is met under all three invocations | FORTRESS-06 |
| Explicitly named legacy test path still imports that script | Not a FORTRESS-02 blocker; certified collection excludes legacy scripts, and ADR-0010 declines to reclassify the excluded files | FORTRESS-06 |
| `run_jaos.py` does not route through `PlatformRuntime` | Not a FORTRESS-02 blocker; ADR-0010 twice excludes canonical runtime composition from its own scope | FORTRESS-04 |

**Verified closure evidence**, all exit code 0:

| Area | Result |
|---|---|
| Canonical import boundary | 10 passed |
| Internal path-literal guard | 20 passed |
| Legacy runtime-state inventory (02F) | 16 passed |
| Inventory enrichment (02J) | 33 passed |
| RuntimePaths | 41 passed, 1 skipped |
| RuntimePaths integration | 8 passed |
| Runtime logging isolation | 12 passed |
| Configuration containment | 11 passed |
| SQLite path containment | 18 passed |
| Memory runtime binding | 14 passed |
| Test-state isolation | 13 passed |
| Collection containment | 12 passed |
| Core runtime integration | 3 passed |
| Full configured suite `tests/tests` | 1,840 passed, 1 skipped, 0 failed, 0 errors |

Collection topology: `pytest --collect-only` exit 0 (1,841 collected, 0 legacy
flat scripts); `pytest tests/ --collect-only` exit 0 (1,841, 0 legacy);
`pytest . --collect-only` exit 2 (1,832, 0 legacy). Protected-tree fingerprint
unchanged after all three.

Containment probes from a working directory outside the repository: 12 of 12
relative SQLite paths rejected before any directory creation or connection, with
no artifact left behind; `ConfigManager` mutation without an explicit absolute
profile target fails closed and rejects relative targets; the JAOS logger holds
no handler until `RuntimePaths` is injected, so no fallback to
`logs/system.log` is reachable. Constructing `RuntimePaths` and
`PlatformRuntime` created zero files and zero directories.

Legacy preservation: all 153 inventoried artifact hashes were verified to equal
the raw file bytes exactly; zero artifacts are missing; 152 of 153 declare a
writer, the exception being `logs/system.log`, which correctly declares none
after FORTRESS-02D; no artifact is marked `CANONICAL_EXTERNALIZED`; `data/cache`
and `data/diagnostics` remain represented as unowned and empty.

ADR-0010 Decision-body criteria verified: stdlib-only implementation with
`platformdirs` absent; `RuntimePaths` holds no credential material and the
canonical secret boundary remains `jaos/ai/secrets/`; the versioned layout is
`v1/profiles/default` with all ten scopes beneath the profile root; and the
operating-system default root resolves outside the repository as an absolute
path.

The closure decision was adversarially adjudicated by three independent lenses —
strict ADR-0010 textualism, AGENTS.md evidence discipline, and workstream scope
and ownership. All three returned DO_NOT_CLOSE. The junction gap was judged
blocking by 3 of 3 and assigned to FORTRESS-02 itself; the symlink skip,
`pytest .` exit code, and launcher gap were each judged non-blocking by 3 of 3.

Two incidental observations, neither a FORTRESS-02 criterion: external pytest
cache and bytecode placement currently depends on the operator passing
`-p no:cacheprovider` and `PYTHONDONTWRITEBYTECODE=1` rather than on repository
configuration, and one bytecode file was created during this slice by a
verification probe that omitted the flag; and the untracked `graphify-out/`
directory at the repository root was regenerated by an external tool outside all
four protected trees. Both belong to FORTRESS-12 if they are actioned at all.

---

### 7.7 FORTRESS-02K Re-Run — FORTRESS-02 COMPLETE AND VERIFIED

Date: 2026-08-21. Environment and execution constraints as in section 7.4.
Section 7.6 is retained unchanged as the historical record of the first
FORTRESS-02K attempt, which was correctly blocked.

The single blocker recorded in section 7.6 — the missing junction rejection
regression test required by ADR-0010 — has been remediated by test-only change
to `tests/tests/platform/test_runtime_paths.py`. No production code was
modified. `test_profile_junction_escape_is_rejected` creates a real Windows
directory junction with `mklink /J` under a disposable temporary root, proves
the canonical target escapes the validated profile scope, asserts the resolver
raises `profile_root escapes its validated profile scope`, asserts nothing was
written through the escape, and removes only the reparse point with `os.rmdir`
so the target is never traversed. It executes and passes on this host rather
than skipping.

**ADR-0010 rejection-test matrix — all six categories now have executable
coverage:** traversal, path separators, drive-qualified paths, and UNC paths via
the parametrized profile-grammar test; symlink escape via the retained
capability-gated test; and junction escape via the new test.

Verified closure evidence, all exit code 0:

| Area | Result |
|---|---|
| `test_profile_junction_escape_is_rejected` | 1 passed — executed, not skipped |
| RuntimePaths | 42 passed, 1 skipped |
| RuntimePaths integration | 8 passed |
| Test-state isolation | 13 passed |
| Runtime logging isolation | 12 passed |
| Configuration containment | 11 passed |
| SQLite path containment | 18 passed |
| Memory runtime binding | 14 passed |
| Legacy runtime-state inventory (02F) | 16 passed |
| Inventory enrichment (02J) | 33 passed |
| Collection containment | 12 passed |
| Canonical import boundary | 10 passed |
| Internal path-literal guard | 20 passed |
| Full configured suite `tests/tests` | 1,841 passed, 1 skipped, 0 failed, 0 errors |

Protected-tree integrity: the 161-file manifest across `data/`, `config/`,
`logs/`, and `exports/` hashed to
`6d58d221901282267b5856bfddb99c0fe70ba489ba8bfe8f32a80251e63e4675` both before
and after testing. Artifact inventory unchanged at 2,021 paths with zero
additions. No SQLite, write-ahead, runtime, profile, migration, pytest-cache, or
bytecode artifact appeared inside the repository, and no reparse point remains
anywhere in the working tree. No legacy state changed and no migration occurred.

**FORTRESS-02 — Runtime-data and test isolation — is COMPLETE AND VERIFIED.**

This closes the FORTRESS-02 workstream only. It does not constitute Fortress
Program certification, does not complete Step 7, does not authorize Step 8, does
not resume Phase 8 expansion, and does not authorize FORTRESS-03. Fortress
certification remains governed by section 9 and requires FORTRESS-01 through
FORTRESS-12.

Items deferred at closure, each with its owner, unchanged from the section 7.6
adjudication:

| Deferred item | Owner |
|---|---|
| Directory-symlink escape verification on a capable host | FORTRESS-11 and the certification environment |
| `run_jaos.py` routing through `PlatformRuntime`; `configure_logging` having no production caller | FORTRESS-04 |
| `main.py` retirement and legacy stack disposition | FORTRESS-04 and FORTRESS-06 |
| Legacy writer quarantine; `pytest .` package-name collision; explicitly named legacy test path importing | FORTRESS-06 |
| User-directed filesystem tool path enforcement | FORTRESS-07 |
| Crash-safe persistence hardening for legacy writers | FORTRESS-08 |
| External pytest cache and bytecode placement beyond the certified invocation; repository cleanup and untracking | FORTRESS-12 |

Step 7 remains IN PROGRESS, Step 8 remains blocked by Step 7, Fortress
certification remains NOT STARTED, and major Phase 8 expansion remains PAUSED.

---

### 7.8 FORTRESS-03 Closure Evidence — FORTRESS-03 COMPLETE AND VERIFIED

Date: 2026-08-22. Environment: Python 3.14, pytest, Windows, `.venv`.
Execution constraints for every run: `PYTHONDONTWRITEBYTECODE=1`,
`-p no:cacheprovider`, and external disposable `--basetemp` roots outside the
repository, per section 7.4's established contract.

FORTRESS-03 continued from the already-committed 03A (canonical runtime
lifecycle state model) and 03B (`PlatformRuntime` lifecycle ownership) through
03C–03J, one slice at a time, each with its own atomic commit:

| Slice | Scope | Status |
|---|---|---|
| FORTRESS-03A | Canonical `RuntimeLifecycleState` model and legal-transition table | COMPLETE AND VERIFIED (prior session) |
| FORTRESS-03B | `PlatformRuntime` lifecycle ownership (construct/initialize/start/stop) | COMPLETE AND VERIFIED (prior session) |
| FORTRESS-03C | Truthful readiness | COMPLETE AND VERIFIED |
| FORTRESS-03D | Partial-start rollback and EventBus subscriber isolation | COMPLETE AND VERIFIED |
| FORTRESS-03E | Coordinated shutdown; AI/Memory shutdown hardening | COMPLETE AND VERIFIED |
| FORTRESS-03F | Truthful health | COMPLETE AND VERIFIED |
| FORTRESS-03G | Repeat lifecycle semantics | COMPLETE AND VERIFIED (no production change required; closed with evidence) |
| FORTRESS-03H | Production status honesty | COMPLETE AND VERIFIED |
| FORTRESS-03I | Construction/initialization separation | COMPLETE AND VERIFIED |
| FORTRESS-03J | Lifecycle invariant closure suite and documentation sync | COMPLETE AND VERIFIED |

**RAA-004 resolved with evidence.** `BootManager.boot()` previously ignored
every validator report and unconditionally set `boot_status = READY`,
returning `True` regardless of outcome; `StartupValidator._boot_ready()`
checked `boot_status == "READY"` while the status was still `"BOOTING"`, and
readiness was gated on `config_manager_status`/`executive_brain_status`/
`startup_manager_status` — legacy context keys nothing in the canonical path
sets. `BootManager` now drives the real `PlatformRuntime` lifecycle
(`initialize()` then `start()`), resets `steps` on every attempt, and gates
`READY` on `RuntimeValidator`/`StartupValidator`/`DependencyValidator`
reports computed from the just-started runtime; `StartupValidator` readiness
is derived only from `lifecycle_state` plus real validator delegation.
Evidence: `tests/tests/platform/test_boot_manager.py`,
`test_startup_validator.py`, `test_fortress_03_lifecycle_closure.py`.

**RAA-006 resolved with evidence.** `RuntimeHealthCertifier` marked every
registered service `HEALTHY` unconditionally; `AIStatusProvider.get_status()`
hardcoded `healthy=True`; `MemoryProvider.health_check()` defaulted to `True`
for any provider that did not override it; `ExecutiveStatusProvider`
aggregated two hardcoded-`True` sub-reports into its overall health. All four
now derive their reported status from real, verifiable facts — real service
presence, an actual provider `health_check()` call, a fail-closed default,
and excluding sub-reports with no real failure condition from the aggregate
— with `UNKNOWN`/`DEGRADED`/`FAILED` all reachable where warranted.
`PlatformRuntime.mark_degraded()`/`mark_recovered()` make
`RuntimeLifecycleState.DEGRADED` reachable on a live instance, not just legal
in the abstract transition table; the operational policy for when to use it
remains FORTRESS-10's. Evidence: `tests/tests/platform/test_runtime_health_certifier.py`,
`tests/tests/ai/test_ai_status.py`, `tests/tests/executive/test_executive_status.py`,
`tests/tests/memory/test_provider_platform.py`.

**SHT-003 resolved.** `run_jaos.py` no longer prints an unconditional
`"Boot Complete"` claim (nothing has been constructed at that point in the
launcher, so no replacement claim was invented — the launcher does not yet
route through `PlatformRuntime`; that remains FORTRESS-04). The live CLI
`status` command (`CommandDispatcher._show_status()`) now derives
`Tool Platform`/`AI Platform`/`Executive Controller` from
`self.tool_manager`, `self.ai_manager.get_diagnostic_status()`, and
`self.executive.get_status()` respectively, instead of hardcoded literals.
Evidence: `tests/tests/integration/test_run_jaos_banner.py`,
`tests/test_cli_ai_integration.py`.

**Lifecycle half of RAA-007 resolved.** `CommandDispatcher.__init__`
interleaved object-graph construction with provider registration and
initialization, so a failure after `initialize_provider()` succeeded left an
initialized provider with no reachable owner. Construction now builds the
complete object graph first; provider registration and initialization run
last, as an explicitly separate, rollback-scoped step that unregisters and
shuts down the provider if initialization fails. Composition-root ownership
(moving construction out of `CommandDispatcher` entirely) remains
FORTRESS-04/05. Evidence: `tests/test_cli_ai_integration.py`.

**Partial-start rollback, coordinated shutdown, and subscriber isolation.**
`PlatformRuntime.start()` already unwound partial registration atomically
(03B); `EventBus.publish()` now isolates a subscriber exception so it cannot
propagate into lifecycle progression or block remaining subscribers;
`PlatformRuntime._teardown_platform_services()` now continues past an
individual unregister failure and aggregates every failure into one
`PartialShutdownError`, leaving the runtime truthfully `FAILED` rather than
`STOPPED` when teardown was incomplete. The same defect class was narrowly
hardened at the two named external call sites: `ProviderManager.shutdown_all()`
(AI) and `ProviderRegistry.clear()` (Memory) each now attempt every provider
regardless of individual failures and raise one aggregated error, without any
change to AI/Memory architecture or single-provider shutdown semantics.
Evidence: `tests/tests/platform/test_event_bus.py`,
`test_platform_runtime_lifecycle.py`, `test_fortress_03_lifecycle_closure.py`,
`tests/test_provider_manager.py`, `tests/tests/memory/test_provider_platform.py`.

**Repeat lifecycle semantics (03G).** No production change was required: the
canonical transition table (03A) and the truthful boot gate (03C) already
enforce no silent double initialize/start, no invalid boot-after-terminal-state,
no duplicate registration buildup, no step accumulation, and STOPPED/FAILED
terminal with no restart contract. Explicit test evidence was added to prove
each invariant directly rather than only as a byproduct of other tests.

**Lifecycle invariant closure suite (03J).**
`tests/tests/platform/test_fortress_03_lifecycle_closure.py` is the single
consolidated location proving, against live objects, every required FORTRESS-03J
invariant: construction != readiness; READY only after required readiness;
invalid transitions fail; partial startup rollback; reverse teardown;
shutdown continues through failures; truthful health; DEGRADED reachable; no
canonical legacy readiness keys; production path makes no fabricated
readiness claim; no contradictory RuntimeContext lifecycle facts.

**Documentation synchronized.** `docs/architecture/RUNTIME_LIFECYCLE.md` and
`docs/architecture/BOOT_SEQUENCE.md` each gained a "Canonical ... (FORTRESS-03,
Verified)" section documenting the actual implemented state model and boot/
shutdown flow, with their pre-existing escaped-markdown corruption
(backslash-escaped headings/bullets, `&#x20;` entities, redundant blank
lines) fixed. Their broader pre-existing conceptual content for later phases
is preserved unchanged under an "Extended / Future" heading, not deleted or
contradicted.

**Full configured regression, run after every slice and again at closure:**

| Suite | Result |
|---|---|
| `tests/tests` (final, post-03J) | 1,941 passed, 1 skipped, 0 failed, 0 errors |

Exact per-slice full-suite counts recorded during implementation: 1,904 (03C)
→ 1,909 (03D) → 1,915 (03E) → 1,926 (03F) → 1,929 (03G) → 1,930 (03H) → 1,930
(03I) → 1,941 (03J), against the pre-FORTRESS-03 baseline of 1,841 recorded in
section 7.7.

**Protected-tree evidence.** `git status --porcelain` was inspected before
every stage/commit across all of 03C–03J; `data/`, `config/`, `logs/`, and
`exports/` showed only the pre-existing modified/untracked state already
present at the start of this workstream (the seven pre-existing modified
`data/*.json` files and `SECURITY.md`) at every check, with zero additional
changes introduced by any FORTRESS-03 commit. No commit in this workstream
staged or touched a path under `data/`, `config/`, `logs/`, or `exports/`.

**Deferred items, each with its owner, unchanged or newly recorded:**

| Deferred item | Owner |
|---|---|
| `run_jaos.py` routing through `PlatformRuntime`; launcher composition root | FORTRESS-04 |
| `CommandDispatcher` provider construction moved out of the CLI dispatcher | FORTRESS-04/05 |
| Operational policy for when to call `mark_degraded()`/`mark_recovered()` | FORTRESS-10 |
| Central/unified health contract across AI, Memory, and Executive (today each platform's health surface is truthful but independently shaped) | FORTRESS-10 |
| Directory-symlink escape verification on a capable host | FORTRESS-11 and the certification environment |
| `main.py` retirement and legacy stack disposition | FORTRESS-04 and FORTRESS-06 |
| Legacy writer quarantine; `pytest .` package-name collision | FORTRESS-06 |

**FORTRESS-03 — Runtime lifecycle correctness — is COMPLETE AND VERIFIED.**

This closes the FORTRESS-03 workstream only. It does not constitute Fortress
Program certification, does not complete Step 7, does not authorize Step 8,
does not resume Phase 8 expansion, and does not authorize FORTRESS-04 to
begin without separate authorization. Fortress certification remains
governed by section 9 and requires FORTRESS-01 through FORTRESS-12.

---

### 7.9 FORTRESS-04 Closure Evidence — FORTRESS-04 COMPLETE AND VERIFIED

Date: 2026-08-22. Environment and execution constraints as in section 7.4.

FORTRESS-04's goal was one canonical production launcher and one runtime
composition root, with `run_jaos.py` actually reaching `PlatformRuntime`
rather than merely declaring it as a target.

**RAA-001 resolved with evidence (lifecycle/reachability half).**
`run_jaos.py`'s `JAOSApplication` previously printed a banner and handed off
directly to `JAOSShell`; `PlatformRuntime`/`BootManager` existed but were
never instantiated by the launcher. `JAOSApplication` now owns one
`PlatformRuntime` (constructor-injectable for tests) and one `BootManager`.
`run()`:

1. Prints the banner (unchanged, no status claim).
2. Calls `runtime.configure_logging()` — logging is configured through the
   runtime's own `RuntimePaths`, not a private/hardcoded path.
3. Calls `boot_manager.boot()`. If it returns `False`, the shell is never
   constructed, a truthful failure message is printed,
   `boot_manager.shutdown()` still runs, and `run()` returns `1`.
4. On success, constructs and runs `JAOSShell`, wrapped so an unexpected
   exception during or after construction is caught, logged via the JAOS
   logger, followed by a controlled `boot_manager.shutdown()`, and reported
   as exit code `1` rather than propagating an uncontrolled crash.
5. On the clean path, the final exit code is `0 if boot_manager.shutdown()
   else 1` — shutdown's own truthful result decides the code, it is never
   assumed.

No path prints an unconditional status claim ("Boot Complete", "Ready").
`main.py` is untouched: not imported by `run_jaos.py`, not modernized,
still preserved for FORTRESS-06 quarantine.

**Scope boundary preserved.** This resolves only the lifecycle/reachability
half of RAA-001 — the launcher now reaches and drives `PlatformRuntime`'s
own four platform services. It does not compose AI/Tool/Executive/Memory
into `PlatformRuntime`'s service container; `CommandDispatcher`'s
construction is unchanged and remains FORTRESS-05's composition work.

**Verified results, all exit code 0:**

| Suite | Result |
|---|---|
| `test_canonical_import_boundary.py` | 12 passed |
| `test_run_jaos_banner.py` | 2 passed |
| `test_run_jaos_launcher.py` | 5 passed |
| Full configured suite `tests/tests` | 1,947 passed, 1 skipped, 0 failed, 0 errors |

`test_canonical_closure_reaches_expected_platforms` and the new
`test_canonical_closure_reaches_platform_runtime_lifecycle` run AST analysis
against the real repository `run_jaos.py` (not a synthetic tree) and assert
its closure now reaches `jaos_platform.platform_runtime` and
`jaos_platform.boot_manager` specifically, with zero forbidden-module
violations — direct evidence the launcher reaches the canonical Runtime
Platform, not merely some unrelated `jaos_platform` symbol.

**Test isolation note.** Every `test_run_jaos_launcher.py` test injects the
disposable `jaos_runtime_paths` fixture into the `PlatformRuntime` it
constructs, because `run()` now calls `configure_logging()`, which performs
a real `mkdir` under the resolved logs directory. Verified after the full
suite run: no directory was created under the real OS-default JAOS runtime
root (`%LOCALAPPDATA%\JAOS` on this host).

**Protected-tree evidence.** `git status --porcelain` inspected before
staging: only `run_jaos.py`, `test_canonical_import_boundary.py`, and the
new `test_run_jaos_launcher.py` were staged; `data/`, `config/`, `logs/`,
and `exports/` carried only the pre-existing modified/untracked state
already present before this workstream, with zero additional changes.

**Deferred items, each with its owner:**

| Deferred item | Owner |
|---|---|
| Composing AI/Tool/Executive/Memory platforms into `PlatformRuntime`'s own service container | FORTRESS-05 |
| `CommandDispatcher` construction moved out of the CLI into the composition root | FORTRESS-04/05 (recorded, unchanged from FORTRESS-03 closure) |
| `main.py` retirement and legacy stack disposition | FORTRESS-06 |
| Full top-level exception taxonomy / distinct exit codes per failure class | Not required by FORTRESS-04; current truthful 0/1 contract is sufficient |

**FORTRESS-04 — One launcher and one composition root — is COMPLETE AND
VERIFIED.**

This closes the FORTRESS-04 workstream only. It does not constitute
Fortress Program certification, does not complete Step 7, does not
authorize Step 8, does not resume Phase 8 expansion, and does not authorize
FORTRESS-05 to begin without separate authorization.

---

### 7.10 FORTRESS-05 Closure Evidence — COMPLETE AND VERIFIED

Date: 2026-08-24. Governing decision: ADR-0011. Environment: Python 3.14.6,
pytest 9.1.1, Windows, `.venv`. Required execution constraints are
`PYTHONDONTWRITEBYTECODE=1`, `-p no:cacheprovider`, and a unique external
disposable `--basetemp`.

FORTRESS-05 was delivered through separately authorized slices:

| Slice | Authorized scope | State / checkpoint |
|---|---|---|
| FORTRESS-05A | Canonical Tool Platform composition | IMPLEMENTED; included in `f9b054e` |
| FORTRESS-05B | Shared AIManager and Executive composition | IMPLEMENTED; included in `f9b054e` |
| FORTRESS-05C | Canonical SQLite-backed MemoryStore composition | IMPLEMENTED; `1df73e3` |
| FORTRESS-05D | Narrow MS-0025A-D Conversation Intelligence composition | IMPLEMENTED AND VERIFIED; `cf26693` |
| FORTRESS-05E | Executable canonical-composition invariants and closure evidence | IMPLEMENTED AND VERIFIED; uncommitted |
| Closure remediation | Independent-review lifecycle, failure, readiness, import, and governance corrections | IMPLEMENTED AND VERIFIED; uncommitted |

The Founder-approved graph is:

```text
PlatformRuntime
  -> PlatformComposition
     -> ToolManager
     -> AIManager
     -> ExecutiveController
     -> MemoryStore
     -> ConversationOrchestrator
```

The exact service names are `tool_manager_platform`, `ai_manager_platform`,
`executive_controller_platform`, `memory_store_platform`, and
`intelligence_orchestrator_platform`. The first four registry entries are
owned by Platform; the Conversation authority is owned by Intelligence. Every
composition property resolves the same object held by the Runtime container.

The Conversation carve-out composes and lifecycle-owns completed MS-0025A-D
components only. It uses `ConversationPolicy(policy_name="default")` with all
other dataclass defaults unchanged and explicitly pins the approved template as
`conversation@1.0`. `ConversationOrchestrator` shares the composed `AIManager`.
It is not routed from the production CLI. MS-0025X, advanced Intelligence,
planning, reasoning, decision, agents, execution proposals, autonomous
workflows, and Memory-context integration remain paused or deferred.

The composed `MemoryStore` is lifecycle-owned but is not used by live CLI
behavior. Its provider-neutral contract now declares `close()` and
`is_closed`, implemented by SQLite, PostgreSQL, and in-memory stores.

Composition-owned Memory, AI, and Intelligence lifecycle failures use one
retry-retention rule. A failed owner remains registered and reachable, its
service name and required lifecycle references remain with the composition,
independent safe cleanup continues, and all teardown failures are aggregated
in `CompositionTeardownError`. A later successful teardown retries the failed
lifecycle work before unregistering and clearing the retained owner. An
unregistered store or manager whose rollback cleanup fails is likewise retained
by its composition reference until a successful retry.

AI initialization and service registration are one guarded ownership window.
An initialization or registration failure shuts down the newly created
manager/provider, removes only attempt-owned services, preserves foreign
registrations, and propagates the original failure even when cleanup also
reports an error.

Functional readiness is executable rather than construction-only: the focused
suite completes one real Conversation turn through the composed deterministic
MockProvider and one real Memory create/get round trip under disposable
`RuntimePaths.memory`. It also proves that the real `JAOSShell` receives the
canonical injected dispatcher and cannot reach shell or dispatcher fallback
construction.

The lazy Intelligence facade is interim FORTRESS-06 containment. Public exports
and the prior `jaos.intelligence.context`, `.exceptions`, `.interfaces`,
`.models`, and `.prompt` submodule attributes are preserved lazily without
loading deferred capabilities during a clean launcher import or simple
submodule compatibility access. Explicit access to a deferred capability
remains observable by the executable module guard. The boundary covers
decision, planning, reasoning, agents, execution proposals, confidence and
explainability models, planning-policy models, `MemoryContextSource`,
`MemorySearchEngine`, and autonomous workflow code.

Current verification evidence:

| Suite | Result |
|---|---|
| Final review #2 focused remediation suite | 54 passed |
| Related composition / intelligence / memory / platform / integration ladder | 1,603 passed; 1 skipped |
| Full configured `tests/tests` suite | 2,002 passed; 1 skipped; 0 failed; 0 errors |

The one skip is the existing directory-symlink escape test. This Windows host
cannot create the required directory symlink without privilege (`WinError
1314`). The test remains intact and must run on a capable host before overall
Fortress certification.

Finding disposition under ADR-0011 is intentionally not full closure:

- RAA-002 is PARTIALLY RESOLVED. Composition and lifecycle ownership are
  resolved; production request-path routing remains deferred.
- RAA-007 is PARTIALLY RESOLVED. Canonical production composition is fixed;
  compatibility self-construction remains FORTRESS-06 debt.
- RAA-009 remains OPEN — DEFERRED. No Memory-context adapter was implemented.

**FORTRESS-05 — Canonical platform composition — is COMPLETE AND VERIFIED at
workstream level.** RAA-002 and RAA-007 remain partially resolved by explicit
Founder decision, and RAA-009 remains open. This does not certify the Fortress
Program, complete Step 7, authorize Step 8, resume Phase 8 expansion, or begin
FORTRESS-06.

---

### 7.11 FORTRESS-06A — Authoritative Legacy/Quarantine Manifest and Import Guards

Date: 2026-08-25. FORTRESS-06 implementation is authorized only for F06A.

F06A creates
`docs/architecture/FORTRESS_06_LEGACY_QUARANTINE_MANIFEST.md` as the
authoritative human/governance classification record and extends the existing
`tests/tests/platform/test_canonical_import_boundary.py` analyzer as the sole
executable canonical import-boundary owner.

The manifest records 33 source entries: eight canonical, three compatibility
debts, sixteen quarantine candidates, two archive-only candidates, and four
safe-to-delete-later candidates. It reserves the future top-level namespace
`legacy_quarantine` without creating it. The executable guard enforces 22
F06-owned top-level identities, including satellite roots previously protected
only by topology, archive/safe-later module identities, and the reserved future
namespace. Exact first-component matching preserves canonical `jaos.ai`,
`jaos.memory`, `jaos.executive`, `jaos.tools`, `jaos.composition`, completed
Conversation Intelligence scope, and `jaos_platform`.

F06A does not move or delete legacy code, change compatibility fallbacks,
migrate or rewrite runtime data, begin F06B, begin FORTRESS-07, resolve
RAA-003, or fully resolve RAA-007. RAA-003 remains OPEN and RAA-007 remains
PARTIALLY RESOLVED. Step 7 remains IN PROGRESS; Step 8 and Fortress
certification remain not started; major Phase 8 expansion remains paused.

F06A is IMPLEMENTED AND VERIFIED — COMMITTED AND PUSHED at checkpoint
`92aa9d7`. The focused import-boundary suite passed 55 tests; the platform
suite passed 363 tests with one skip; the affected composition suite passed 45 tests; and
the full configured `tests/tests` suite passed 2,037 tests with one skip. The
skip is the known Windows directory-symlink privilege limitation. This evidence
does not complete or certify FORTRESS-06.

### 7.12 FORTRESS-06B — Pytest Collection and Package-Collision Remediation

Date: 2026-08-25. F06B was separately authorized for two exact artifact moves,
one canonical pytest import-mode setting, containment tests, and minimum
governance synchronization.

Repository-root prepend collection previously imported the unsupported root
`phase14_integration_test.py` module-body script, preloading the application
`brain` package before pytest tried to collect
`tests/tests/brain/test_executive_brain.py` under the same package identity.
Root collection failed with `ModuleNotFoundError` while explicit importlib-mode
collection succeeded but still imported both root module-body scripts.

F06B used history-preserving, byte-identical moves to archive exactly:

- `phase14_integration_test.py` as
  `legacy_quarantine/tests/phase14_integration_test.py.legacy`; and
- `test_logger.py` as
  `legacy_quarantine/tests/test_logger.py.legacy`.

Neither archive directory has `__init__.py`, and `.py.legacy` is not a Python
import suffix or pytest `python_files` match. `pytest.ini` is still the sole
pytest configuration owner and now selects `--import-mode=importlib`. The
existing `tests/conftest.py` remains the sole owner of containment for the 428
direct `tests/*.py` legacy scripts. No broad ignore, import-path manipulation,
module-cache manipulation, duplicate configuration, or production change was
introduced.

Native pytest importlib mode gives deterministic, isolated test-module loading
while preserving root `brain/`, `tests/tests/brain/`, and canonical `jaos.*`
application imports. Renaming either package would expand migration scope, and
`sys.path` or `sys.modules` manipulation would create noncanonical import state.

Verified F06B evidence, all exit code 0:

- focused collection/import/composition invariants: 80 passed;
- platform suite: 364 passed, 1 skipped;
- composition suite: 45 passed;
- integration suite: 58 passed;
- full configured `tests/tests`: 2,038 passed, 1 skipped;
- configured, `tests/`, and repository-root collection: 2,039 collected each;
- Ruff on both changed Python test files: all checks passed.

Every pytest gate used `PYTHONDONTWRITEBYTECODE=1`,
`.venv/Scripts/python.exe -B -m pytest`, `-p no:cacheprovider`, and a unique
external `--basetemp` under
`C:/Users/vinay/AppData/Local/Temp/`. The exact targets were:

| Gate | Target and options after `pytest` | Result |
|---|---|---|
| Focused | `tests/tests/platform/test_collection_containment.py tests/tests/platform/test_canonical_import_boundary.py tests/tests/composition/test_canonical_composition_invariants.py -q` | 80 passed |
| Platform | `tests/tests/platform -q` | 364 passed, 1 skipped |
| Composition | `tests/tests/composition -q` | 45 passed |
| Integration | `tests/tests/integration -q` | 58 passed |
| Full configured | `tests/tests -q` | 2,038 passed, 1 skipped |
| Configured collection | `--collect-only -q` | 2,039 collected |
| `tests/` collection | `tests/ --collect-only -q` | 2,039 collected |
| Repository-root collection | `. --collect-only -q` | 2,039 collected |

Ruff ran as `.venv/Scripts/python.exe -m ruff check` against
`tests/tests/platform/test_collection_containment.py` and
`tests/tests/platform/test_canonical_import_boundary.py`.

The skip remains the Windows directory-symlink privilege limitation. No
importlib fixture, monkeypatch, relative/package import, cross-test import, or
duplicate-module-identity regression was observed. The F06A guard continues to
forbid canonical production dependency on `legacy_quarantine` and every other
F06 identity while allowing canonical `jaos.*` packages.

F06B is IMPLEMENTED AND VERIFIED — COMMITTED AND PUSHED at checkpoint
`eea8190`. At the F06B checkpoint, it did not resolve RAA-003 or fully resolve
RAA-007, perform broad legacy quarantine, start F06C or FORTRESS-07, complete
Step 7, enter Step 8, certify Fortress, or resume major Phase 8 expansion.

### 7.13 FORTRESS-06C — Hidden CLI Composition-Root Removal

Date: 2026-08-25. F06C was separately authorized to remove compatibility-only
self-composition and lifecycle ownership from the canonical CLI adapters.

`CommandDispatcher` now requires injected `ToolManager`, `AIManager`, and
`ExecutiveController` collaborators. It cannot instantiate `ToolManager`,
`ProviderManager`, `AIManager`, or `ExecutiveController`, and it owns no
provider shutdown. `JAOSShell` now requires an injected dispatcher and cannot
instantiate or shut down one. Exit remains a CLI control result only;
`PlatformComposition` owns composed platform teardown and `JAOSApplication`
owns the canonical launcher lifecycle.

Missing constructor collaborators fail immediately with normal Python
`TypeError` behavior. Repository caller evidence did not justify a standalone
compatibility factory, so no second composition or lifecycle owner was added.
Configured callers use explicit collaborators or canonical composition. The
428 direct `tests/*.py` legacy scripts, including excluded
`tests/test_cli_ai_integration.py`, remain untouched and contained.

Verified F06C evidence, all exit code 0:

| Gate | Result |
|---|---|
| Focused run across all seven changed test files | 125 passed in 9.05 seconds |
| Affected CLI, AI, composition, integration, and platform ladder | 583 passed, 1 skipped in 30.46 seconds |
| Disposable launcher/lifecycle normal exit, EOF, dispatch exception, and shell exception | 4 passed in 1.03 seconds |
| Full configured `tests/tests` | 2,047 passed, 1 skipped in 42.46 seconds |
| Repository-root collection | 2,048 collected in 3.73 seconds |
| Ruff 0.16.1 on changed Python files | All checks passed |

The pytest gates ran under Python 3.14.6 and pytest 9.1.1 with bytecode and
pytest cache disabled and a unique external base temporary directory. The one
skip is independently confirmed at
`tests/tests/platform/test_runtime_paths.py:312`: Windows denied the required
directory-symlink privilege with `WinError 1314`.

The architecture guards prove that `run_jaos.py` remains the sole canonical
composition root, the launcher injects the exact composed Tool, AI, and
Executive objects, the CLI adapters cannot construct platform collaborators,
and shutdown remains with canonical composition/runtime ownership. RAA-007 is
therefore RESOLVED WITH EVIDENCE.

F06C is IMPLEMENTED AND VERIFIED — COMMITTED AND PUSHED at checkpoint
`0a2ea60`.
It does not move legacy source, touch the 428 flat legacy tests, migrate runtime
data, route `ConversationOrchestrator`, implement `MemoryContextSource`, alter
provider resilience or permission policy, begin F06D or FORTRESS-07, complete
Step 7, enter Step 8, certify Fortress, or resume major Phase 8 expansion.

### 7.14 FORTRESS-06D1 — Quarantine Pure AI/Core Duplicate Configured Tests

Date: 2026-08-25. F06D1 implementation is authorized to quarantine eight
duplicate AI and Core configured tests under `tests/tests` that represent
retired shadow architecture already backed by equal-or-stronger canonical
evidence.

F06D1 executed history-preserving, byte-identical moves for exactly:

- `tests/tests/ai/test_ai_config.py` (4 tests) ->
  `legacy_quarantine/tests/ai/test_ai_config.py.legacy`
- `tests/tests/ai/test_ai_provider_interface.py` (4 tests) ->
  `legacy_quarantine/tests/ai/test_ai_provider_interface.py.legacy`
- `tests/tests/ai/test_ai_provider_manager.py` (14 tests) ->
  `legacy_quarantine/tests/ai/test_ai_provider_manager.py.legacy`
- `tests/tests/ai/test_ai_provider_models.py` (5 tests) ->
  `legacy_quarantine/tests/ai/test_ai_provider_models.py.legacy`
- `tests/tests/ai/test_llm_router.py` (7 tests) ->
  `legacy_quarantine/tests/ai/test_llm_router.py.legacy`
- `tests/tests/ai/test_prompt_engine.py` (8 tests) ->
  `legacy_quarantine/tests/ai/test_prompt_engine.py.legacy`
- `tests/tests/ai/test_prompt_models.py` (4 tests) ->
  `legacy_quarantine/tests/ai/test_prompt_models.py.legacy`
- `tests/tests/core/test_kernel.py` (4 tests) ->
  `legacy_quarantine/tests/core/test_kernel.py.legacy`

The 50 source test definitions are retired from configured execution. SHA256
hashes were verified byte-identical before and after the moves. Neither
archive directory contains `__init__.py`, and `.py.legacy` is unrecognized by
Python import machinery and pytest discovery. Configured legacy-importing
files decrease from 67 to 59.

The F06D audit observation of 5 configured legacy runtime-state writer tests
across 4 files (`test_executive_brain.py`, `test_executive_pipeline.py`,
`test_memory_manager.py`, `test_config_containment.py`) is verified and
reconciled.

Verified F06D1 evidence, all exit code 0:

| Gate | Target and options after `pytest` | Result |
|---|---|---|
| Focused containment | `tests/tests/platform/test_collection_containment.py -q` | 14 passed |
| Import boundary | `tests/tests/platform/test_canonical_import_boundary.py -q` | 55 passed |
| AI suite | `tests/tests/ai -q` | 33 passed |
| Intelligence suite | `tests/tests/intelligence -q` | 785 passed |
| Platform suite | `tests/tests/platform -q` | 365 passed, 1 skipped |
| Composition suite | `tests/tests/composition -q` | 49 passed |
| Integration suite | `tests/tests/integration -q` | 64 passed |
| Full configured | `tests/tests -q` | 1,998 passed, 1 skipped |
| Repository-root collection | `. --collect-only -q` | 1,999 collected |
| Ruff 0.16.1 | `tests/tests/platform/test_collection_containment.py` | All checks passed |

The skip remains the Windows directory-symlink privilege limitation (`WinError
1314`). F06D1 is IMPLEMENTED AND VERIFIED — COMMITTED AND PUSHED at checkpoint
`51818d2`. RAA-003 remains OPEN, Step 8 remains blocked, and major Phase 8
expansion remains paused.

### 7.15 FORTRESS-06D2A — Migrate Canonical Filesystem-Tool Requirements

Date: 2026-08-25. F06D2A implementation is authorized to remove configured-suite
dependence on the retired `executive_brain` filesystem tool implementations
while preserving every meaningful filesystem-tool requirement against canonical
`jaos.tools.filesystem`.

Unlike F06D1, these seven configured paths were not pure duplicates of stronger
canonical evidence: before F06D2A the configured suite contained **no** canonical
filesystem-tool behavior test. The only configured references to
`jaos.tools.filesystem` were the runtime-path literal guard and the
runtime-state-inventory exclusion check, neither of which exercises a tool. The
requirements existed only in the retired
`executive_brain` tests and in the excluded flat `tests/test_*_file_tool.py`
scripts. F06D2A therefore adjudicated each requirement against the current
production contract and re-established it inside the configured suite.

Seven legacy configured files carrying 56 source tests were adjudicated:

| Legacy configured file | Legacy tests | Canonical replacement tests |
|---|---:|---:|
| `tests/tests/tools/test_read_file_tool.py` | 7 | 12 |
| `tests/tests/tools/test_write_file_tool.py` | 8 | 14 |
| `tests/tests/tools/test_copy_file_tool.py` | 8 | 14 |
| `tests/tests/tools/test_delete_file_tool.py` | 7 | 10 |
| `tests/tests/tools/test_move_file_tool.py` | 8 | 14 |
| `tests/tests/tools/test_rename_file_tool.py` | 8 | 16 |
| `tests/tests/tools/test_search_file_tool.py` | 10 | 20 |
| Total | 56 | 100 |

Each configured path keeps its filename and now imports only `jaos.tools` and
`jaos.tools.filesystem`. The legacy payloads are preserved byte-identically as
non-Python archives under
`legacy_quarantine/tests/tools/filesystem/*.py.legacy`. Because the configured
paths survive with new canonical content, Git records these as seven modified
files plus seven added archives rather than as renames; SHA-256 equality between
each pre-change configured file and its archive is the preservation evidence.

Nine legacy requirements were intentionally not preserved:

- Seven `execute("invalid-request")` `TypeError` guards, one per tool. The
  canonical `ToolInterface` accepts a typed frozen `ToolRequest` and the
  canonical result model reports invalid input as `ToolResult(success=False)`
  instead of raising. No canonical contract promises request-type validation
  inside a tool.
- `test_search_requires_pattern`. `SearchFileTool.DEFAULT_PATTERN` is `"*"`, so
  an omitted pattern is valid. The canonical default and the blank-pattern
  rejection are both asserted instead.
- `test_rename_creates_destination_directory`. The canonical `RenameFileTool`
  takes a bare `new_name` and deliberately refuses any name containing a path,
  so a rename cannot relocate a file. Preserving the legacy behavior would have
  weakened canonical containment; the containment rule is asserted instead,
  including relative-path, absolute-path, and parent-traversal rejection.

Canonical requirements now proven for all seven tools include full metadata
contracts (name, version, permissions, capabilities, approval policy, risk
level, status), missing/blank/non-string payload handling, missing-path and
wrong-type path handling, directory-source and directory-destination rejection,
overwrite behavior for write, copy, and move, UTF-8 text and byte-length
semantics, `ToolManager` execution with audit records, permission denial with
`ToolPermissionError` plus its audit record, the `DANGEROUS` delete approval
gate in both blocked and approved states, permission-before-approval ordering,
search defaults, recursion, directory exclusion, and `max_results` bounding,
and a per-tool containment assertion that every effect stays inside the
pytest-owned `tmp_path` root.

Two production observations were recorded without changing production code,
because F06D2A forbids it and neither is a canonical defect:

- Only `DeleteFileTool` carries an approval policy. `WriteFileTool`,
  `CopyFileTool`, `MoveFileTool`, and `RenameFileTool` can overwrite or remove
  caller-named data at `ToolApprovalLevel.NONE`. The current contract is
  asserted as-is; any policy change belongs to a separately authorized slice.
- `RenameFileTool` rejects a `new_name` of `..` through its
  destination-already-exists check rather than its name-containment check, and
  `SearchFileTool` accepts a `bool` `max_results` because `bool` subclasses
  `int`. Containment and bounding still hold in both cases, so the configured
  tests assert the observable outcome rather than the incidental reason.

`tests/tests/platform/test_collection_containment.py` gained two checks: the
seven archives exist as non-Python `.py.legacy` payloads that carry the original
`executive_brain` source and are not importable from their archive directory,
and the seven configured replacements statically import `jaos` and no legacy
root. Configured legacy-importing files decrease from 59 to 52, recomputed
mechanically by AST inspection of every configured test file.

Verified F06D2A evidence, all exit code 0:

| Gate | Target and options after `pytest` | Result |
|---|---|---|
| Focused filesystem | the seven changed `tests/tests/tools` files `-q` | 100 passed |
| Focused containment and boundary | the seven files plus `tests/tests/platform/test_collection_containment.py tests/tests/platform/test_canonical_import_boundary.py -q` | 171 passed |
| Tools suite | `tests/tests/tools -q` | 226 passed |
| Platform suite | `tests/tests/platform -q` | 367 passed, 1 skipped |
| Composition suite | `tests/tests/composition -q` | 49 passed |
| Integration suite | `tests/tests/integration -q` | 64 passed |
| Full configured | `tests/tests -q` | 2,044 passed, 1 skipped |
| Configured collection | `tests/tests --collect-only -q` | 2,045 collected |
| `tests/` collection | `tests/ --collect-only -q` | 2,045 collected |
| Repository-root collection | `. --collect-only -q` | 2,045 collected |
| Ruff 0.16.1 | `ruff check` on the eight changed Python files | All checks passed |

Every pytest gate ran under Python 3.14.6 and pytest 9.1.1 as
`PYTHONDONTWRITEBYTECODE=1 .venv/Scripts/python.exe -B -m pytest` with
`-p no:cacheprovider` and a unique external `--basetemp`. The full configured
count moves from 1,998 to 2,044: 56 legacy tests retired, 100 canonical tests
added, and 2 containment checks added. The one skip remains the Windows
directory-symlink privilege limitation at
`tests/tests/platform/test_runtime_paths.py:312` (`WinError 1314`).

F06D2A is IMPLEMENTED AND VERIFIED — COMMITTED AND PUSHED at checkpoint
`95adce4`. It moves no production code, migrates no runtime data, and touches
none of the 428 flat `tests/*.py` legacy scripts. RAA-003 remains OPEN, RAA-007
remains RESOLVED WITH EVIDENCE, F06D is not complete, FORTRESS-07 has not
started, Step 8 remains blocked, Fortress certification has not started, and
major Phase 8 expansion remains paused.

---

### 7.16 FORTRESS-06D2B - Adjudicate and Migrate the Canonical Tool Platform Core

Date: 2026-08-30. F06D2B implementation is authorized to remove configured-suite
dependence on the retired `executive_brain.tools.core` Tool Platform while
preserving every architecturally valid requirement against canonical
`jaos.tools`.

Four legacy configured files carrying 25 source tests were adjudicated. The
baseline reconciled mechanically by AST inspection before any edit:

| Legacy configured file | Legacy tests | Canonical replacement tests |
|---|---:|---:|
| `tests/tests/tools/test_tool_interface.py` | 3 | 4 |
| `tests/tests/tools/test_tool_models.py` | 5 | 6 |
| `tests/tests/tools/test_tool_registry.py` | 9 | 5 |
| `tests/tests/tools/test_tool_manager.py` | 8 | 4 |
| Total | 25 | 19 |

Before F06D2B the configured suite contained no canonical Tool Platform core
behavior test. The canonical interface, model, registry, and manager contracts
were proven only by the excluded flat scripts `tests/test_tool_platform_core.py`,
`tests/test_tool_permission_audit.py`, `tests/test_tool_approval.py`,
`tests/test_tool_audit.py`, and `tests/test_tool_capabilities.py`, which
`tests/conftest.py` removes from every directory-based invocation. Those scripts
were used as requirement evidence only and were neither copied nor executed.
The configured coverage that did exist was indirect: the F06D2A filesystem-tool
tests exercise `ToolManager` with `ToolPermissionManager`, the `DANGEROUS`
delete approval gate, and `list_audit_records`, and
`tests/tests/composition/test_canonical_composition_invariants.py` proves the
composed `ToolManager` owns a `ToolPermissionManager`, a `ToolApprovalManager`,
and a `ToolAuditLogger`.

The canonical contract differs from the retired one in ways that decide the
adjudication:

- Tool identity moved from a `tool_name` property to `ToolInterface.metadata()`.
- `ToolResponse(status, message, data)` became
  `ToolResult(success, output, error, created_at)`.
- `ToolStatus` changed meaning. It was execution outcome
  (`SUCCESS`/`FAILURE`); it is now tool availability
  (`AVAILABLE`/`UNAVAILABLE`/`DISABLED`), and execution outcome moved to
  `ToolResult.success`.
- `ToolRequest.parameters` became `ToolRequest.payload`, the model is frozen,
  and it carries `approved`.
- Registry and manager errors are typed: `ToolAlreadyRegisteredError` and
  `ToolNotFoundError` replace bare `ValueError` and `KeyError`.
- Enumeration returns a sorted `tuple` rather than a `list`.
- The legacy manager executed a tool directly. The canonical `ToolManager`
  delegates to `ToolExecutionEngine`, which enforces availability, permissions,
  and approval before execution and records an audit entry on every path.

Ten legacy requirements were intentionally not preserved:

- `test_tool_status_values` in its legacy form. `ToolStatus.SUCCESS` and
  `ToolStatus.FAILURE` do not exist canonically. The requirement survives as
  stable canonical availability values, and execution outcome is asserted
  through `ToolResult.success`.
- `test_registry_property`. The canonical `ToolManager` deliberately does not
  expose its registry. Preserving that accessor would document an escape hatch
  around the execution engine's permission, approval, and audit chain, which
  FORTRESS-06D2B's safety boundary forbids. The underlying requirement - that
  the manager owns a registry - is proven through `register_tool`, `has_tool`,
  `list_tools`, and routed execution instead.
- `test_register_invalid_tool` and `test_execute_invalid_request`. The canonical
  registry and manager rely on the `ToolInterface` ABC and typed parameters
  rather than runtime `isinstance` guards, so neither raises `TypeError`.
- `test_unregister_tool`, `test_unregister_missing_tool`, and `test_clear` for
  the registry, and `test_unregister_tool` for the manager. Canonical
  `ToolRegistry` and `ToolManager` expose no deregistration or bulk-clear
  surface at all, so these requirements have no canonical owner.
- `test_count`. There is no canonical `count()`. The requirement survives as the
  length of the canonical `list_tools()` enumeration.

Canonical requirements now proven in the configured suite include the abstract
`ToolInterface` contract for both `metadata` and `execute`, metadata-declared
tool identity, the `ToolRequest`-to-`ToolResult` execution contract, canonical
`ToolStatus` values, `ToolRequest` and `ToolResult` defaults and payload/output
carriage, blank-`tool_name` rejection at request construction, registry
registration with instance-identity lookup, duplicate rejection, missing lookup,
empty-registry state, sorted tuple enumeration with its length, manager-owned
registration and enumeration, and manager execution routing.

The two execution requirements route through the real `ToolManager` rather than
`ToolExecutionEngine` or a tool instance, and assert the audit trail the
canonical chain produces: a routed success records exactly one successful audit
entry, and an unknown tool fails at registry lookup before execution and leaves
the audit log empty. No test reaches around `ToolManager`,
`ToolPermissionManager`, `ToolApprovalManager`, or `ToolAuditLogger` to
manufacture evidence for behavior production obtains through them. Interface,
model, and registry requirements are still tested directly against those
objects, which is their architecturally correct level.

No production code changed and no FORTRESS-07 policy was redesigned. Three
observations were recorded for a later separately authorized slice:

- `ToolRegistry.register` raises `AttributeError` rather than a typed
  `ToolRegistryError` when handed a non-tool object, and `ToolManager.execute`
  raises `AttributeError` when handed a non-`ToolRequest`. Both are input-typing
  robustness gaps, not permission, approval, or audit policy gaps.
- Canonical tool deregistration and registry reset have no owner. The registry
  is append-only for the lifetime of the process.
- The canonical `ToolRequest`, `ToolResult`, `ToolMetadata`, and
  `ToolApprovalPolicy` models are frozen dataclasses, and no configured test
  asserts that immutability. This is not a legacy requirement; it is a canonical
  coverage gap recorded without change.

`tests/tests/platform/test_collection_containment.py` gained three checks: the
four archives exist as non-Python `.py.legacy` payloads that carry the original
`executive_brain.tools.core` source and are not importable from their archive
directory; the four configured replacements statically import `jaos` and no
legacy root; and no configured test at the four adjudicated paths imports
`executive_brain.tools.core`, with the remaining sixteen configured importers
pinned by name as FORTRESS-06D2E prototype-tool test debt so the residue cannot
grow silently. No second quarantine framework was created and `legacy_quarantine`
still contains no `__init__.py`.

Configured legacy-importing files decrease from 52 to 48 and configured
`executive_brain` importers from 39 to 35, both recomputed mechanically by AST
inspection of every configured test file against the F06A guarded top-level
identity list.

Verified F06D2B evidence, all exit code 0:

| Gate | Target and options after `pytest` | Result |
|---|---|---|
| Focused Tool Platform | the four changed `tests/tests/tools` files `-q` | 19 passed |
| Containment and boundary | `tests/tests/platform/test_collection_containment.py tests/tests/platform/test_canonical_import_boundary.py -q` | 74 passed |
| Tools suite | `tests/tests/tools -q` | 220 passed |
| Platform suite | `tests/tests/platform -q` | 370 passed, 1 skipped |
| Composition suite | `tests/tests/composition -q` | 49 passed |
| Integration suite | `tests/tests/integration -q` | 64 passed |
| Full configured | `tests/tests -q` | 2,041 passed, 1 skipped |
| Configured collection | `--collect-only -q` | 2,042 collected |
| `tests/` collection | `tests/ --collect-only -q` | 2,042 collected |
| Repository-root collection | `. --collect-only -q` | 2,042 collected |
| Ruff 0.16.1 | `ruff check` on the five changed Python files | All checks passed |

Every pytest gate ran under Python 3.14.6 and pytest 9.1.1 as
`PYTHONDONTWRITEBYTECODE=1 .venv/Scripts/python.exe -B -m pytest` with
`-p no:cacheprovider` and a unique external `--basetemp`. The full configured
count moves from 2,044 to 2,041: 25 legacy tests retired, 19 canonical tests
added, and 3 containment checks added. The one skip remains the Windows
directory-symlink privilege limitation at
`tests/tests/platform/test_runtime_paths.py:312` (`WinError 1314`).

F06D2B is IMPLEMENTED AND VERIFIED. It moves no production code, migrates no
runtime data, and touches none of
the 428 flat `tests/*.py` legacy scripts. RAA-003 remains OPEN, RAA-007 remains
RESOLVED WITH EVIDENCE, F06D is not complete, F06D2C and later slices have not
started, FORTRESS-07 has not started, Step 8 remains blocked, Fortress
certification has not started, and major Phase 8 expansion remains paused.

---

### 7.17 FORTRESS-06D2C - Retire ExecutiveBrain and Executive Pipeline Tests

Date: 2026-08-30. Founder authorization limits F06D2C to four configured legacy
test files and two missing canonical requirements. The baseline reconciled
mechanically before any edit:

| Retired configured file | Source tests | Archive destination |
|---|---:|---|
| `tests/tests/brain/test_executive_brain.py` | 9 | `legacy_quarantine/tests/executive/brain/test_executive_brain.py.legacy` |
| `tests/tests/integration/test_executive_pipeline.py` | 5 | `legacy_quarantine/tests/executive/pipeline/test_executive_pipeline.py.legacy` |
| `tests/tests/integration/test_executive_pipeline_v2.py` | 4 | `legacy_quarantine/tests/executive/pipeline/test_executive_pipeline_v2.py.legacy` |
| `tests/tests/integration/test_executive_runtime.py` | 4 | `legacy_quarantine/tests/executive/runtime/test_executive_runtime.py.legacy` |
| Total | 22 | 4 non-Python archives |

All four legacy payloads were copied before their configured sources were
retired. SHA-256 and Git blob identities match byte-for-byte; the exact hashes
are recorded in
`docs/architecture/FORTRESS_06_LEGACY_QUARANTINE_MANIFEST.md` section 11.
Every archive ends in `.py.legacy`, no archive directory contains
`__init__.py`, Python import machinery cannot resolve the archived module
names, and pytest's configured filename patterns do not collect them.

`tests/tests/executive/test_canonical_executive_controller.py` supplies the
minimum canonical coverage through two source tests collected as three cases:

- A deterministic read request enters `ExecutiveController.process`, is
  planned and delegated through `ExecutionCoordinator`, reaches the real
  canonical `ToolManager` and `ReadFileTool`, and returns an
  `ExecutiveResponse` whose success, message, path, content, and Tool audit
  record all reflect the actual test-owned file operation.
- Empty and whitespace-only requests follow the existing canonical unknown
  intent/failure contract. They do not call `ToolManager.execute`, do not
  execute or audit a tool, and do not claim success. Production was not changed
  to reproduce the retired `ValueError` behavior.

No test was recreated for ExecutiveBrain ownership of RegistryManager or
MemoryManager, hard-coded manager/registry counts, legacy WorkingMemory fields,
mission/decision/result identifiers or counts, automatic approval, legacy
runtime registration/status keys, literal `PIPELINE_EXECUTED`, shadow
WorkflowEngine readiness, or monolithic initialization/readiness. Those are
retired shadow semantics or separately governed later requirements, not
canonical F06D2C contracts.

The existing F06 containment authority gained three checks for the exact four
former paths and archives, canonical-only replacement imports, and explicit
preservation of
`tests/tests/integration/test_memory_runtime_integration.py` for later legacy
Memory adjudication. The existing F06D2E inventory continues to pin the same
sixteen prototype browser, Windows, and development
`executive_brain.tools.core` importers. Manager/registry tests, legacy Memory
tests, provider tests, satellite integration tests, production
`executive_brain`, and `main.py` remain untouched.

AST analysis of all configured test imports mechanically recomputed:

- configured legacy-facing files: 48 -> 44;
- configured `executive_brain` importers: 35 -> 31; and
- configured `executive_brain.tools.core` prototype importers: 16 unchanged.

The F06D runtime-state writer description is corrected for these four files.
Their legacy execution mutates only in-memory registries, WorkingMemory,
ServiceContainer, RuntimeContext, and transient EventBus state. No persistent
runtime-state writer, repository-data path, file API, or runtime logging
configuration is called. F06D2C moved no runtime data and changed none of the
protected JSON evidence inputs.

Verified F06D2C evidence, all recorded successful gates exit code 0:

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
| Ruff 0.16.1 | All checks passed on both changed Python files |

Every gate used Python 3.14.6, pytest 9.1.1,
`PYTHONDONTWRITEBYTECODE=1`, `.venv/Scripts/python.exe -B -m pytest`,
`-p no:cacheprovider`, and a unique external `--basetemp`. Python 3.14's
Windows `0o700` ACL behavior denied pytest access to its own basetemp under the
managed sandbox, so the commands loaded a temporary Windows-only runner shim
that changed only pytest's directory mode to inherit the parent ACL. The shim
did not alter JAOS code, fixtures, or test behavior and was removed before the
final diff. The one skip remains the known Windows directory-symlink privilege
limitation at `tests/tests/platform/test_runtime_paths.py:312`.

F07 permission/approval/audit/risk policy, F08 persistence/recovery/replay,
F09 provider resilience, F10 aggregate health/degradation/readiness semantics,
F11 abuse/security/chaos/CI, and resumed Phase 8 intelligence routing,
conversation-memory context, multi-turn continuity, and expanded
reasoning/planning remain deferred and unchanged.

FORTRESS-06D2C — IMPLEMENTED AND VERIFIED. It moves no production code and
completes neither F06D nor FORTRESS-06. At the F06D2C checkpoint, RAA-003
remained OPEN, RAA-007 remained RESOLVED WITH EVIDENCE, and F06D2D was
ADJUDICATED with its governance decision approved but implementation NOT
STARTED. F06D2E+ and FORTRESS-07 remained NOT STARTED, Step 8 remained NOT
STARTED — BLOCKED BY STEP 7, Fortress certification remained NOT STARTED, and
major Phase 8 expansion remained PAUSED.

---

### 7.18 FORTRESS-06D2D — Retire Manager and Registry Shadow Tests

Date: 2026-08-30. ADR-0012 remains authoritative: older Phase 8 manager and
registry names are logical responsibility labels and historical integration
boundaries. They do not grant canonical runtime authority to the exact
`executive_brain.managers.*` or `executive_brain.registries.*`
implementations. Those exact implementations remain shadow architecture and
controlled FORTRESS-06 quarantine candidates.

The baseline reconciled mechanically to 44 configured legacy-facing files, 31
configured `executive_brain` importers, and exactly nine D2D files carrying 94
source tests. F06D2D retired those exact files into these non-Python archives:

| Retired configured file | Source tests | Archive destination |
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

Before retirement, configured canonical coverage was added to
`tests/tests/executive/test_canonical_executive_controller.py` for aggregate
`ExecutiveController` execution metrics. The test executes one successful read
and one missing-file failure through `ExecutiveController`,
`ExecutionCoordinator`, `ToolManager`, and real canonical `ReadFileTool`. It
verifies truthful responses and audit records, then proves the existing
`ExecutiveMetrics` contract: two plans executed, one succeeded, one failed,
one last-plan step, and a success rate of 0.5. Production behavior required no
change.

All nine archived payloads match their former configured sources by SHA-256 and
Git blob identity. Every archive ends in `.py.legacy`, is outside Python import
and pytest collection suffixes, and no directory under `legacy_quarantine/`
contains `__init__.py`.

The retired literal manager readiness states and health dictionaries, generic
RegistryManager ownership, hard-coded registry graph and count semantics,
automatic approval and confidence behavior, simulated execution success,
fabricated results, legacy IDs and lookup exceptions, persistence assumptions,
direct platform/service binding, and global cross-registry authority were
intentionally not ported. They are obsolete shadow semantics or explicitly
deferred responsibilities, not current canonical requirements.

The existing F06 containment authority gained two D2D checks. They prove the
nine former paths are absent, the nine exact archives are non-Python and
non-collectable with pinned SHA-256 identities, no legacy package exists under
the archive tree, and the remaining configured `executive_brain` inventory is
exactly 22 files: 16 F06D2E prototype-tool importers, four deferred Memory
importers, and two deferred provider importers. The canonical Executive test
continues to import only canonical `jaos.*` plus standard test dependencies.

AST analysis of every configured test file mechanically recomputed the achieved
counts:

- configured legacy-facing files: 44 -> 35;
- configured `executive_brain` importers: 31 -> 22;
- F06D2E prototype-tool importers: 16 unchanged;
- deferred legacy Memory importers: 4 unchanged; and
- deferred provider-test importers: 2 unchanged.

The retired manager/registry implementations and tests use in-memory registry
dictionaries only. They execute no persistent repository runtime-state writer.
F06D2D performed no runtime-data migration and changed none of the protected
JSON evidence inputs.

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
| Combined Executive/Tools/Composition/Platform/Integration | 702 passed, 1 skipped |
| Full configured `tests/tests` | 1,934 passed, 1 skipped |
| Repository-root collection | 1,935 collected |
| Ruff on both changed Python files | All checks passed |

Every successful pytest gate used repository Python,
`PYTHONDONTWRITEBYTECODE=1`, `-B`, `-p no:cacheprovider`, and a unique external
`--basetemp`. An initial direct metrics invocation exited 1 before executing the
test because Python 3.14's Windows `0o700` ACL behavior denied pytest access to
its basetemp. The successful gates used the already established temporary
Windows runner shim that changes only pytest's temporary-directory mode to
inherit the parent ACL. The shim changed no repository file or test behavior.
The one skip remains the known Windows directory-symlink privilege limitation.

F07 permission/approval/audit/risk policy, F08 durable mission/decision/plan/
result persistence and recovery/replay, F09 provider resilience, F10 aggregate
health/degradation/readiness, F11 security/chaos/CI, and resumed Phase 8
mission/planning/decision/reasoning/autonomy work remain deferred and unchanged.

FORTRESS-06D2D — IMPLEMENTED AND VERIFIED. It completes neither F06D nor
FORTRESS-06. RAA-003 remains OPEN, RAA-007 remains RESOLVED WITH EVIDENCE,
F06D2E+ and FORTRESS-07 remain NOT STARTED, Step 8 remains NOT STARTED — BLOCKED
BY STEP 7, Fortress certification remains NOT STARTED, and major Phase 8
expansion remains PAUSED.

---

### 7.19 FORTRESS-06D2E — Retire Prototype Tool Shadow Tests

Date: 2026-08-31. FORTRESS-06D2E — IMPLEMENTED AND VERIFIED. The mechanically
reconciled baseline was 35 configured legacy-facing files, 22 configured
`executive_brain` importers, and exactly 16 prototype-tool files carrying 101
source tests:

| Family | Retired files | Retired source tests | Archive family |
|---|---:|---:|---|
| Browser | 5 | 32 | `legacy_quarantine/tests/tools/browser/` |
| Windows/Desktop | 6 | 39 | `legacy_quarantine/tests/tools/windows/` |
| Development/VS Code | 5 | 30 | `legacy_quarantine/tests/tools/development/` |
| Total | 16 | 101 | 16 `.py.legacy` archives |

All 101 source test definitions were top-level, synchronous, pytest-collectable
cases. F06D2E also added two net-new containment tests, contributing two
collected cases. The collection evidence therefore reconciles exactly:

```text
1,935 pre-D2E collected cases
- 101 retired collected cases
+   2 new containment cases
= 1,836 post-D2E collected cases
```

No canonical replacement capability test was required. The reusable Tool
Platform invariants are already configured against canonical `jaos.tools`
contracts and authorities: `ToolInterface`, `ToolMetadata`, `ToolRequest`,
`ToolResult`, `ToolStatus`, `ToolRegistry`, `ToolManager`,
`ToolExecutionEngine`, and the existing permission, approval, and audit
boundaries. F06D2E therefore added no browser, desktop, Developer Platform,
F07, F11, or autonomous behavior.

All 16 former configured payloads were moved byte-identically to these
non-Python archive destinations, and SHA-256 plus Git-blob equality was
verified against each former source:

| Former configured file | Source tests | Archive destination |
|---|---:|---|
| `tests/tests/tools/test_browser_automation_tool.py` | 6 | `legacy_quarantine/tests/tools/browser/test_browser_automation_tool.py.legacy` |
| `tests/tests/tools/test_cookies_tool.py` | 3 | `legacy_quarantine/tests/tools/browser/test_cookies_tool.py.legacy` |
| `tests/tests/tools/test_downloads_tool.py` | 8 | `legacy_quarantine/tests/tools/browser/test_downloads_tool.py.legacy` |
| `tests/tests/tools/test_tabs_tool.py` | 6 | `legacy_quarantine/tests/tools/browser/test_tabs_tool.py.legacy` |
| `tests/tests/tools/test_web_search_tool.py` | 9 | `legacy_quarantine/tests/tools/browser/test_web_search_tool.py.legacy` |
| `tests/tests/tools/test_clipboard_tool.py` | 4 | `legacy_quarantine/tests/tools/windows/test_clipboard_tool.py.legacy` |
| `tests/tests/tools/test_close_application_tool.py` | 6 | `legacy_quarantine/tests/tools/windows/test_close_application_tool.py.legacy` |
| `tests/tests/tools/test_launch_application_tool.py` | 9 | `legacy_quarantine/tests/tools/windows/test_launch_application_tool.py.legacy` |
| `tests/tests/tools/test_notification_tool.py` | 7 | `legacy_quarantine/tests/tools/windows/test_notification_tool.py.legacy` |
| `tests/tests/tools/test_process_manager_tool.py` | 6 | `legacy_quarantine/tests/tools/windows/test_process_manager_tool.py.legacy` |
| `tests/tests/tools/test_services_tool.py` | 7 | `legacy_quarantine/tests/tools/windows/test_services_tool.py.legacy` |
| `tests/tests/tools/test_build_tool.py` | 8 | `legacy_quarantine/tests/tools/development/test_build_tool.py.legacy` |
| `tests/tests/tools/test_debug_tool.py` | 5 | `legacy_quarantine/tests/tools/development/test_debug_tool.py.legacy` |
| `tests/tests/tools/test_git_tool.py` | 5 | `legacy_quarantine/tests/tools/development/test_git_tool.py.legacy` |
| `tests/tests/tools/test_project_tool.py` | 7 | `legacy_quarantine/tests/tools/development/test_project_tool.py.legacy` |
| `tests/tests/tools/test_run_tool.py` | 5 | `legacy_quarantine/tests/tools/development/test_run_tool.py.legacy` |
| Total | 101 | 16 archives |

Every archive ends in `.py.legacy`, is outside Python import and pytest
collection suffixes, and no directory under `legacy_quarantine/` contains an
`__init__.py`. The old tool-name and `ToolResponse`/`ToolStatus` shapes,
hard-coded browser paths and download internals, direct browser and clipboard
behavior, forceful process termination, `shell=True` launch behavior, Windows
parser details, arbitrary build/debug/run commands, VS Code launcher coupling,
and prototype Git plumbing were intentionally not ported.

Browser navigation/tabs/cookies/downloads/search, desktop and PC-control
capabilities, and Developer Platform capabilities remain deferred to their
future approved owning workstreams. F07 retains permission, approval, risk,
audit, and destructive-action policy. F11 retains injection, malicious-input,
path-traversal, symlink-escape, and platform-abuse verification. No such future
capability or policy work began in F06D2E.

The existing F06 containment authority now proves that all 16 former configured
paths are absent, all 16 pinned archives exist and remain non-importable and
non-collectable, no configured prototype-tool importer remains, the six
remaining `executive_brain` importers are exactly four Memory tests and two
provider tests, and the corresponding 16 production prototype modules remain
untouched for F06E. Those production prototypes remain importable legacy source
but are not registered or loaded by canonical `ToolManager`, referenced by
`PlatformComposition`, or imported by canonical production code.

AST inspection of every configured test mechanically verified the achieved
counts:

- configured legacy-facing files: 35 -> 19;
- configured `executive_brain` importers: 22 -> 6;
- remaining Memory importers: 4; and
- remaining provider-test importers: 2.

The exact 19-file configured legacy-facing residue is:

| Family | Count | Configured files |
|---|---:|---|
| Memory/provider `executive_brain` importers | 6 | `tests/tests/ai/test_ollama_provider.py`; `tests/tests/ai/test_openai_provider.py`; `tests/tests/integration/test_memory_runtime_integration.py`; `tests/tests/memory/test_memory_manager.py`; `tests/tests/memory/test_memory_registry.py`; `tests/tests/memory/test_working_memory.py` |
| Satellite/runtime integrations | 10 | `tests/tests/integration/test_communication_runtime_integration.py`; `test_dashboard_runtime_integration.py`; `test_development_runtime_integration.py`; `test_engineering_runtime_integration.py`; `test_infrastructure_runtime_integration.py`; `test_knowledge_runtime_integration.py`; `test_pc_control_runtime_integration.py`; `test_security_runtime_integration.py`; `test_system_services_runtime_integration.py`; `test_workflow_runtime_integration.py` |
| Platform/core/kernel/config containment | 3 | `tests/tests/platform/test_config_containment.py`; `tests/tests/platform/test_core_runtime_integration.py`; `tests/tests/platform/test_kernel_runtime_integration.py` |

The retired configured tests used mocks, fakes, or test-owned temporary paths.
They performed no real browser or network operation, process launch or
termination, service or clipboard mutation, Git/build/run command, download,
repository runtime-data write, or persistent runtime-state write. F06D2E
performed no runtime-data migration and changed no protected JSON evidence.

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

Every successful pytest gate used repository Python,
`PYTHONDONTWRITEBYTECODE=1`, `-B`, `-p no:cacheprovider`, and a unique external
`--basetemp` with the already established temporary Windows ACL runner shim.
The shim changed no production or test behavior and is not part of the task
diff. The one skip remains the known Windows directory-symlink privilege
limitation.

FORTRESS-06D2E — IMPLEMENTED AND VERIFIED. It completes neither F06D nor
FORTRESS-06. RAA-003 remains OPEN, RAA-007 remains RESOLVED WITH EVIDENCE,
FORTRESS-07 remains NOT STARTED, Step 7 remains IN PROGRESS, Step 8 remains NOT
STARTED — BLOCKED BY STEP 7, Fortress certification remains NOT STARTED, and
major Phase 8 expansion remains PAUSED.

---

### 7.20 FORTRESS-06D Memory Adjudication Governance — ADR-0013

Date: 2026-08-31. The read-only Memory adjudication is COMPLETE. It reconciled
the exact four remaining configured legacy Memory importers and 30 source tests:

| Configured file | Source tests | Read-only disposition before ADR-0013 |
|---|---:|---|
| `tests/tests/integration/test_memory_runtime_integration.py` | 4 | Clear quarantine candidate |
| `tests/tests/memory/test_memory_manager.py` | 9 | Founder decision required |
| `tests/tests/memory/test_memory_registry.py` | 7 | Clear quarantine candidate |
| `tests/tests/memory/test_working_memory.py` | 10 | Founder decision required |
| Total | 30 | Four configured files |

The conflict was the active Phase 7 statement that the current Executive
`WorkingMemory` API must remain stable. ADR-0013 records the Founder-approved
supersession of that exact implementation/API compatibility requirement. The
concrete `executive_brain.memory.WorkingMemory`, `MemoryManager`, and
`MemoryRegistry` implementations are shadow architecture rather than canonical
runtime authorities. This governance clarification makes all four configured
Memory files approved quarantine candidates for a later controlled
implementation.

Their logical responsibilities remain preserved without creating a replacement
Working Memory authority:

- persistent Memory remains owned by canonical `MemoryStore`/`SQLiteStore`;
- active request and transient session/context state await an approved Context
  Platform or task-session-context owner;
- mission, plan, decision, and result references await explicit owners when
  Phase 8 resumes, with durable forms assigned to FORTRESS-08 where applicable;
- health, readiness, and degradation semantics belong to FORTRESS-10;
- Experience Memory remains a separate future Experience Memory Platform; and
- `MemoryContextSource`/`MemorySearchEngine` coupling remains governed by
  RAA-009, which remains OPEN — DEFERRED.

Memory-test quarantine implementation has NOT STARTED. Current mechanically
verified counts remain 19 configured legacy-facing files and six configured
`executive_brain` importers. Only after separately authorized and verified
implementation are the projected changes:

- configured legacy-facing files: 19 -> 15; and
- configured `executive_brain` importers: 6 -> 2.

The projected two remaining importers are
`tests/tests/ai/test_openai_provider.py` and
`tests/tests/ai/test_ollama_provider.py`. These projections are not current
results. No test or production source moved, no quarantine artifact changed, no
runtime data migrated, and no new Memory, Context, Experience, F08, F10, or
Phase 8 capability began in this governance task.

Recording ADR-0013 makes the four-file Memory slice READY FOR CONTROLLED
IMPLEMENTATION only after this governance change is checkpointed and separate
implementation authorization is given. F06D and FORTRESS-06 remain IN PROGRESS,
RAA-003 remains OPEN, RAA-009 remains OPEN — DEFERRED, Step 8 and Fortress
certification remain NOT STARTED, and major Phase 8 expansion remains PAUSED.

---

## 8. Relationship to Stabilization and Certified Phases

The Step 7 record is preserved:

- Step 7 remains in progress.
- RAA-002 is partially resolved; production request routing remains deferred.
- RAA-005 is resolved with evidence.
- RAA-007 is resolved with evidence by F06C's removal of hidden CLI
  composition and lifecycle ownership.
- RAA-008 is resolved with evidence.
- RAA-009 remains open and deferred.
- unresolved RAA findings remain unresolved.
- Step 8 Stabilization Certification has not begun.
- Phase 8 major expansion remains paused.

The Runtime Architecture Audit and Bug Fixing and Regression Report retain the
terminology, findings, dates, and evidence applicable when they were written.
Fortress is recorded as a later governance decision and must not be inserted
retroactively into those reports.

Phase 6 AI Platform and Phase 7 Memory Platform certification remain valid for
their approved provider-independent Alpha baselines. Fortress does not revoke
those certifications. It governs unification, production reachability, runtime
hardening, and the evidence required before further capability expansion.

---

## 9. Fortress Certification Rule

Fortress certification may be claimed only after FORTRESS-01 through
FORTRESS-12 are complete and current evidence demonstrates that the canonical
production path and every production capability in scope are:

- reachable through the approved launcher and composition root;
- tested at the required unit, integration, architecture, runtime, security,
  and failure-injection levels;
- permission- and approval-controlled according to risk;
- observable through truthful central health, lifecycle, and action telemetry;
- recoverable through crash-safe persistence and applicable rollback;
- replaceable behind stable contracts without creating a shadow authority; and
- auditable from intent and proposal through approval, execution, result, and
  failure.

Certification must identify exact commands, results, failures, skips, runtime
configuration, audit evidence, unresolved exceptions, documentation state, and
the approving authority. Historical test counts are not current Fortress
certification evidence.

---

## 10. Update History

| Date | Version | Change |
|---|---|---|
| 2026-08-31 | 1.20 | Added Founder-approved ADR-0013, reconciled the active Phase 7 Executive WorkingMemory compatibility conflict, and recorded the completed read-only Memory adjudication: 4 configured files / 30 source tests, all four governance-approved quarantine candidates, implementation not started, current counts unchanged at 19 legacy-facing files and 6 `executive_brain` importers, and projected post-implementation counts of 15 and 2. Preserved canonical persistent-Memory ownership, deferred Context/Experience/F08/F10 responsibilities, RAA-003 OPEN, RAA-009 OPEN — DEFERRED, and the Phase 8 pause. |
| 2026-08-31 | 1.19 | Recorded F06D2E as IMPLEMENTED AND VERIFIED: retired 16 prototype-tool files carrying 101 pytest-collectable source tests into byte/blob-identical `.py.legacy` archives without replacement capability tests; added two containment tests, reconciling root collection as 1,935 - 101 + 2 = 1,836; verified 35 -> 19 legacy-facing and 22 -> 6 `executive_brain` importer reductions; preserved four Memory and two provider importers plus all 16 production prototypes for later work; and recorded no production change, external side effect, runtime writer, or data migration. Full configured suite passed 1,835 with 1 skip and Ruff passed. F06D and FORTRESS-06 remain in progress; RAA-003 remains open. |
| 2026-08-30 | 1.18 | Recorded F06D2D as IMPLEMENTED AND VERIFIED: added aggregate canonical Executive metrics coverage before retiring 9 manager/registry files carrying 94 source tests into byte/blob-identical `.py.legacy` archives; verified 44 -> 35 legacy-facing and 31 -> 22 `executive_brain` importer reductions; preserved the 16 F06D2E, 4 Memory, and 2 provider importers; recorded no production change or runtime-data migration. Full configured suite passed 1,934 with 1 skip, root collection found 1,935 tests, and Ruff passed. F06D and FORTRESS-06 remain in progress; RAA-003 remains open. |
| 2026-08-30 | 1.17 | Added Founder-approved ADR-0012 and recorded F06D2D's adjudicated 9-file / 94-source-test manager/registry inventory, approved technical retirement plan, required aggregate Executive metrics coverage, unchanged current counts of 44 legacy-facing files and 31 `executive_brain` importers, projected 44 -> 35 and 31 -> 22 impact, and implementation-not-started boundary. F06D and FORTRESS-06 remain in progress; RAA-003 remains open; F07, Step 8, Fortress certification, and major Phase 8 expansion remain unstarted, blocked, or paused. |
| 2026-08-30 | 1.16 | Recorded F06D2C's exact 4-file / 22-source-test ExecutiveBrain and pipeline retirement, four byte/blob-identical non-Python archives, two canonical Executive source tests, three containment checks, corrected in-memory writer finding, 48 -> 44 legacy-facing reduction, and 35 -> 31 `executive_brain` importer reduction. Full configured suite 2,025 passed, 1 skipped; repository-root collection found 2,026 tests; Ruff passed. F06D2C is IMPLEMENTED AND VERIFIED; F06D and FORTRESS-06 remain in progress, and later slices remain unstarted. |
| 2026-08-30 | 1.15 | Recorded F06D2B's adjudication of 4 configured Tool Platform test files carrying 25 legacy tests, their byte-identical `.py.legacy` archives under `legacy_quarantine/tests/tools/core/`, 19 canonical `jaos.tools` replacement tests, 10 dropped legacy requirements, 3 recorded non-FORTRESS-07 observations, and the 52 -> 48 legacy-facing reduction (39 -> 35 `executive_brain` importers). Full configured suite 2,041 passed, 1 skipped; all three collection shapes 2,042 collected; Ruff clean. F06D2B is IMPLEMENTED AND VERIFIED. Synchronized F06D2A to its committed checkpoint `95adce4`. FORTRESS-06 remains in progress, F06D is not complete, and F06D2C+ remains not started. |
| 2026-08-25 | 1.14 | Recorded F06D1's exact quarantine of 8 duplicate AI/Core configured tests (50 tests retired) to `legacy_quarantine/tests/` as `.py.legacy` artifacts; verified 59 legacy-importing files remaining; full configured suite 1,998 passed, 1 skipped; root collection 1,999 collected; F06D1 is IMPLEMENTED AND VERIFIED CANDIDATE. |
| 2026-08-25 | 1.13 | Synchronized F06C current-state wording with committed and pushed checkpoint `0a2ea60`; FORTRESS-06 remains in progress through F06C, while F06D+, FORTRESS-07, Step 8, certification, and Phase 8 resumption remain unstarted or blocked. |
| 2026-08-25 | 1.12 | Recorded F06C's mandatory injected CLI adapters, canonical lifecycle ownership, exact green verification evidence, and RAA-007 resolution. FORTRESS-06 remains in progress through F06C; F06D+, FORTRESS-07, Step 8, certification, and Phase 8 resumption remain unstarted or blocked. |
| 2026-08-25 | 1.11 | Recorded F06B's exact two-file byte-identical non-Python archive move and canonical pytest importlib mode. All three supported collection forms now collect the same 2,039 tests with exit code 0; focused 80, platform 364 with 1 skip, composition 45, integration 58, and full configured 2,038 with 1 skip passed. FORTRESS-06 remains in progress; F06C+, FORTRESS-07, Step 8, certification, and Phase 8 resumption remain unstarted or blocked. |
| 2026-08-25 | 1.10 | Started FORTRESS-06 through the separately authorized F06A slice. Added the authoritative 33-entry legacy/quarantine manifest, reserved `legacy_quarantine`, and extended the existing canonical import guard to 22 F06-owned top-level identities while preserving canonical `jaos.*` roots. F06A is an implemented and verified candidate in the uncommitted working tree: focused 55 passed; platform 363 passed, 1 skipped; composition 45 passed; full configured suite 2,037 passed, 1 skipped. No source moved or was deleted, no runtime data migrated, F06B and FORTRESS-07 have not started, RAA-003 remains open, and RAA-007 remains partially resolved. |
| 2026-08-24 | 1.9 | Recorded ADR-0011 and the FORTRESS-05A-E slice-state table; verified AI registration rollback, provider-neutral Memory lifecycle and retryable close failure, explicit `conversation@1.0`, functional Conversation/Memory readiness, real-shell fallback non-reachability, decision/deferred import guards, and lazy submodule compatibility. Focused, affected-subsystem, and full configured suites passed with zero failures/errors. FORTRESS-05 is COMPLETE AND VERIFIED at workstream level. RAA-002 and RAA-007 remain partially resolved; RAA-009 remains open. Fortress certification, Step 7 completion, Step 8, Phase 8 resumption, and FORTRESS-06 remain unauthorized. |
| 2026-08-22 | 1.8 | Recorded FORTRESS-04 closure evidence: `run_jaos.py` now instantiates and drives `PlatformRuntime`/`BootManager` (lifecycle/reachability half of RAA-001 resolved), with truthful exit codes, controlled shutdown on both boot failure and unexpected shell exceptions, and no fabricated status claim. FORTRESS-04 is COMPLETE AND VERIFIED at workstream level. Composing AI/Tool/Executive/Memory into the Runtime Platform remains FORTRESS-05, unauthorized. |
| 2026-08-22 | 1.7 | Recorded FORTRESS-03 closure evidence for slices 03A through 03J: truthful readiness, partial-start rollback and subscriber isolation, coordinated shutdown with narrow AI/Memory hardening, truthful health across Runtime/AI/Memory/Executive, repeat lifecycle semantics, production status honesty (SHT-003), construction/initialization separation (lifecycle half of RAA-007), and the consolidated lifecycle invariant closure suite. RAA-004 and RAA-006 resolved with evidence. FORTRESS-03 is COMPLETE AND VERIFIED at workstream level. Fortress certification, Step 7, Step 8, Phase 8 resumption, and FORTRESS-04 are all unaffected and unauthorized. |
| 2026-08-21 | 1.6 | Recorded the FORTRESS-02K re-run after the junction blocker was remediated by test-only change. All ADR-0010 acceptance criteria now pass and FORTRESS-02 is COMPLETE AND VERIFIED at workstream level. Fortress certification, Step 7, Step 8, Phase 8 resumption, and FORTRESS-03 are all unaffected and unauthorized. |
| 2026-08-21 | 1.5 | Recorded the FORTRESS-02K closure evidence run. FORTRESS-02 is NOT closed and remains IN PROGRESS, blocked by one ADR-0010 acceptance-criterion gap: the missing junction rejection test. Symlink skip, `pytest .` exit code, explicit legacy-path import, and the launcher composition gap are each recorded as non-blocking with an assigned owner. |
| 2026-08-21 | 1.4 | Recorded the verified FORTRESS-02J inventory writer, reachability, disposition, and canonical-containment enrichment. FORTRESS-02K is next and not started. FORTRESS-02 remains in progress and is not certified. |
| 2026-08-21 | 1.3 | Recorded FORTRESS-02G audit completion and the verified FORTRESS-02H and FORTRESS-02I slices, with evidence and two recorded limitations. FORTRESS-02J is next and not started. FORTRESS-02 remains in progress and is not certified. |
| 2026-08-21 | 1.2 | Recorded the FORTRESS-02 checkpoint reconciliation: FORTRESS-02 IN PROGRESS, slices 02A through 02F implemented and verified with evidence, 02G next and not started, FORTRESS-03 not started. Preserved Step 7, Step 8, Phase 8 pause, and certification state. |
| 2026-08-21 | 1.1 | Recorded the Founder-approved FORTRESS-02 runtime-path architecture decision and preserved the implementation, migration, and phase boundaries. |
| 2026-08-21 | 1.0 | Recorded Founder-approved Fortress governance baseline, canonical target, hard gate, and ordered workstreams. |
