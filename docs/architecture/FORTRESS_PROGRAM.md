# JAOS Architectural Unification & Runtime Hardening

Document ID: GOV-FORTRESS-01

Program Name: JAOS Architectural Unification & Runtime Hardening ("Fortress Program")

Document Version: 1.8

Certified Repository Baseline: v0.9.0-alpha

Development Target: v0.10.0-alpha

Status: In Progress

Owner and Approval Authority: Founder Vinay B

Maintainer: JAOS Engineering

Founder Direction Recorded: 2026-08-21

Last Updated: 2026-08-22

Related Documents:

- `JAOS_MANIFEST.md`
- `docs/architecture/ARCHITECTURE_DECISIONS.md`
- `docs/architecture/ARCHITECTURE_GOVERNANCE.md`
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
| Step 7 — Bug Fixing and Regression | IN PROGRESS |
| RAA-005 | RESOLVED WITH EVIDENCE |
| RAA-008 | RESOLVED WITH EVIDENCE |
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

Implementation of the first FORTRESS-02 slices proceeded after that decision
under separate authorization. Their verified state is recorded in section 7.2.
FORTRESS-02 is COMPLETE AND VERIFIED at workstream level. The overall
Fortress Program is not certified, and FORTRESS-03 has not started.

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
| 5 | FORTRESS-05 — Canonical platform composition | PLANNED |
| 6 | FORTRESS-06 — Legacy migration and quarantine | PLANNED |
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

## 8. Relationship to Stabilization and Certified Phases

The Step 7 record is preserved:

- Step 7 remains in progress.
- RAA-005 is resolved with evidence.
- RAA-008 is resolved with evidence.
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
| 2026-08-22 | 1.8 | Recorded FORTRESS-04 closure evidence: `run_jaos.py` now instantiates and drives `PlatformRuntime`/`BootManager` (lifecycle/reachability half of RAA-001 resolved), with truthful exit codes, controlled shutdown on both boot failure and unexpected shell exceptions, and no fabricated status claim. FORTRESS-04 is COMPLETE AND VERIFIED at workstream level. Composing AI/Tool/Executive/Memory into the Runtime Platform remains FORTRESS-05, unauthorized. |
| 2026-08-22 | 1.7 | Recorded FORTRESS-03 closure evidence for slices 03A through 03J: truthful readiness, partial-start rollback and subscriber isolation, coordinated shutdown with narrow AI/Memory hardening, truthful health across Runtime/AI/Memory/Executive, repeat lifecycle semantics, production status honesty (SHT-003), construction/initialization separation (lifecycle half of RAA-007), and the consolidated lifecycle invariant closure suite. RAA-004 and RAA-006 resolved with evidence. FORTRESS-03 is COMPLETE AND VERIFIED at workstream level. Fortress certification, Step 7, Step 8, Phase 8 resumption, and FORTRESS-04 are all unaffected and unauthorized. |
| 2026-08-21 | 1.6 | Recorded the FORTRESS-02K re-run after the junction blocker was remediated by test-only change. All ADR-0010 acceptance criteria now pass and FORTRESS-02 is COMPLETE AND VERIFIED at workstream level. Fortress certification, Step 7, Step 8, Phase 8 resumption, and FORTRESS-03 are all unaffected and unauthorized. |
| 2026-08-21 | 1.5 | Recorded the FORTRESS-02K closure evidence run. FORTRESS-02 is NOT closed and remains IN PROGRESS, blocked by one ADR-0010 acceptance-criterion gap: the missing junction rejection test. Symlink skip, `pytest .` exit code, explicit legacy-path import, and the launcher composition gap are each recorded as non-blocking with an assigned owner. |
| 2026-08-21 | 1.4 | Recorded the verified FORTRESS-02J inventory writer, reachability, disposition, and canonical-containment enrichment. FORTRESS-02K is next and not started. FORTRESS-02 remains in progress and is not certified. |
| 2026-08-21 | 1.3 | Recorded FORTRESS-02G audit completion and the verified FORTRESS-02H and FORTRESS-02I slices, with evidence and two recorded limitations. FORTRESS-02J is next and not started. FORTRESS-02 remains in progress and is not certified. |
| 2026-08-21 | 1.2 | Recorded the FORTRESS-02 checkpoint reconciliation: FORTRESS-02 IN PROGRESS, slices 02A through 02F implemented and verified with evidence, 02G next and not started, FORTRESS-03 not started. Preserved Step 7, Step 8, Phase 8 pause, and certification state. |
| 2026-08-21 | 1.1 | Recorded the Founder-approved FORTRESS-02 runtime-path architecture decision and preserved the implementation, migration, and phase boundaries. |
| 2026-08-21 | 1.0 | Recorded Founder-approved Fortress governance baseline, canonical target, hard gate, and ordered workstreams. |
