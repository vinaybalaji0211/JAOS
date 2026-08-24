# JAOS Next Actions

Version: 4.2
Status: ACTIVE
Owner: Vinay B
Maintainer: JAOS Engineering
Last Synchronized: 2026-08-24
Certified Release: v0.9.0-alpha
Development Target: v0.10.0-alpha
Current Phase: Phase 8 — AI Intelligence Platform
Current Milestone: MS-0025E — Reasoning and Planning Intelligence
Execution State: Major Phase 8 expansion paused for stabilization and Fortress certification
Current Stabilization Activity: Step 7 — Bug Fixing and Regression
Current Fortress State: FORTRESS-01 governance baseline recorded; FORTRESS-02 through FORTRESS-05 COMPLETE AND VERIFIED at workstream level; FORTRESS-06 not started
Exact Next Action: Preserve FORTRESS-05 closure and continue only separately authorized Step 7 work without beginning FORTRESS-06

---

## 1. Purpose

This document defines the exact next authorized engineering actions for JAOS.

It must identify:

- The certified release baseline
- The active development target
- The current phase and milestone
- The current repository-stabilization checkpoint
- The work that has already been completed
- The work that remains pending
- The actions currently authorized
- The actions currently prohibited
- The exact point from which Phase 8 will resume

This document must describe the real repository state.

It must not direct engineers to repeat completed planning or implementation.

---

## 2. Authoritative Current State

| Item | Current state |
|---|---|
| Certified release | v0.9.0-alpha |
| Development target | v0.10.0-alpha |
| Current phase | Phase 8 — AI Intelligence Platform |
| Milestone family | MS-0025 |
| Active milestone | MS-0025E — Reasoning and Planning Intelligence |
| Phase 8 execution | Major expansion paused — Fortress hard gate |
| Stabilization step | Step 7 of 9 — IN PROGRESS |
| Current activity | Step 7 — Bug Fixing and Regression |
| Step 7 entry | APPROVED — IN PROGRESS |
| Step 8 entry | PENDING — BLOCKED BY STEP 7 |
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
| FORTRESS-05 | COMPLETE AND VERIFIED — ADR-0011 |
| Repository health | STABILIZATION IN PROGRESS |
| Architecture health | FORTRESS HARDENING REQUIRED |
| Full regression certification | PENDING |
| Stabilization certification | PENDING |
| Fortress certification | NOT STARTED |
| Phase 8 release readiness | NOT YET CERTIFIED |

Phase 7 — Memory Platform is complete, certified, released, tagged, and pushed as:

`v0.9.0-alpha`

Phase 8 is the active development phase.

The Phase 8 release target is:

`v0.10.0-alpha`

Phase 8 implementation is temporarily paused for the approved repository
stabilization sequence.

This pause is not:

- A rollback
- A phase restart
- A roadmap redesign
- An implementation failure
- Authorization to discard completed work
- Authorization to begin a different milestone

---

## 3. Immediate Priority

The immediate priority is to preserve the FORTRESS-01 governance checkpoint and
the verified FORTRESS-02 through FORTRESS-05 state, continue only separately
authorized Step 7 work, and avoid beginning FORTRESS-06 without separate
authorization.

Founder/reviewer Vinay B approved entry into Step 7 on 2026-08-12.

The documentation checkpoint is:

`786abb3` docs(stabilization): certify Steps 4 through 6

Step 6 — JAOS Shell Testing remains COMPLETED WITH FINDINGS and recorded in:

`docs/engineering/JAOS_SHELL_TEST_REPORT.md`

Step 6 completion documentation synchronization is COMPLETE.

Step 5 — Full Automated Testing remains COMPLETED and recorded in:

`docs/engineering/FULL_AUTOMATED_TEST_REPORT.md`

RAA-001 through RAA-009 and SHT-001 through SHT-006 are authorized for
controlled remediation.

RAA-005 and RAA-008 are resolved with evidence. RAA-002 and RAA-007 are
partially resolved under ADR-0011: request routing remains deferred for
RAA-002, and compatibility self-construction remains FORTRESS-06 debt for
RAA-007. RAA-009 remains open and deferred; other unresolved RAA findings
remain unresolved. Step 7 remains in progress; neither Step 8 nor Fortress
certification has begun.

The controlled Step 7 workflow is:

1. Build a finding-remediation matrix for RAA-001 through RAA-009 and
   SHT-001 through SHT-006.
2. Identify overlaps and dependencies.
3. Classify each finding as fix, documentation correction, or approved
   deferral.
4. Define acceptance tests before implementation.
5. Apply one controlled fix cluster at a time.
6. Run targeted tests after every cluster.
7. Run the complete automated and JAOS Shell regression suites.
8. Produce the Step 7 report for Founder review.

Step 8 — Stabilization Certification remains PENDING — BLOCKED BY STEP 7.

MS-0025E and Phase 8 implementation remain paused.

---

## 4. Completed Engineering Baseline

The certified platform baseline includes:

- Runtime Platform
- Kernel and application composition
- Executive Platform
- Manager boundaries
- Tool Platform
- AI Platform
- Memory Platform
- Provider registries and factories
- Provider-independent platform contracts
- Permission-controlled execution
- Runtime lifecycle management
- CLI and JAOS Shell foundations
- Architecture governance
- Testing and certification workflows
- Repository continuation documentation

The certified baseline must remain recoverable.

The current stabilization activity must not rewrite, invalidate, or silently
expand the scope of the `v0.9.0-alpha` release.

---

## 5. Phase 7 — Memory Platform State

Phase 7 is complete and certified.

Its established scope includes:

### Memory Contracts

- Memory identity
- Memory type
- Memory scope
- Memory record
- Memory metadata
- Memory lifecycle
- Memory query
- Memory statistics
- Provider contracts

### Provider Implementations

- In-memory foundations
- SQLite provider
- PostgreSQL provider foundations
- Provider serialization
- Provider transactions
- Provider health checks
- Provider registration
- Provider construction
- Runtime provider selection

### Architecture Rules

- Higher-level platforms depend on Memory Platform contracts.
- Higher-level platforms must not depend directly on SQLite.
- Higher-level platforms must not depend directly on PostgreSQL.
- Future providers must integrate behind stable Memory Platform interfaces.
- Provider choice must remain controlled by the Memory Platform.
- Storage-specific behavior must not leak into the Intelligence Platform.

Additional production-oriented Memory Platform work remains scheduled after
Phase 8.

That deferred work does not invalidate the certified Phase 7 baseline.

---

## 6. Phase 8 Milestone State

The authoritative Phase 8 milestone definitions are maintained in:

`docs/project/PHASE8_MILESTONES.md`

Current milestone status:

| Milestone | Scope | Current status |
|---|---|---|
| MS-0025A | Intelligence Foundation | COMPLETED |
| MS-0025B | Context Management | COMPLETED |
| MS-0025C | Prompt Composition | COMPLETED |
| MS-0025D | Conversation Intelligence | COMPLETED |
| MS-0025E | Reasoning and Planning Intelligence | ACTIVE — MAJOR EXPANSION PAUSED BY FORTRESS GATE |
| MS-0025G | Agent and Execution Proposal Foundations | PENDING |
| MS-0025X | AI Intelligence Platform Composition | PENDING |
| MS-0025F | AI Intelligence End-to-End Certification | PENDING CERTIFICATION |

The active implementation milestone is:

`MS-0025E — Reasoning and Planning Intelligence`

After Step 8 and Fortress certification are complete and explicit Founder
authorization is recorded, Phase 8 resumes from MS-0025E.

MS-0025A through MS-0025D must not be restarted or reimplemented without an
approved engineering decision supported by repository evidence.

---

## 7. Preserved Phase 8 Work

Existing Phase 8 work must remain preserved throughout stabilization.

Established or implemented areas include:

- Intelligence identities
- Intelligence request types
- Intelligence requests
- Intelligence results
- Intelligence component contracts
- Context models
- Context-management foundations
- Prompt models
- Prompt-composition foundations
- Conversation models
- Conversation sessions
- Conversation turns
- Conversation orchestration
- Conversation-engine foundations
- Initial Intelligence Platform tests
- Provider-independent component boundaries
- Runtime-facing integration foundations

Current MS-0025E scope includes:

- Reasoning contracts
- Reasoning requests
- Reasoning results
- Reasoning behavior
- Planning contracts
- Planning requests
- Planning proposals
- Planning behavior
- Reasoning and planning coordination
- Validation and failure behavior
- Unit testing
- Integration testing

The exact implementation state must be verified during the applicable audit and
testing steps.

Documentation must not claim that incomplete behavior is certified.

---

## 8. Repository-Stabilization Sequence

The approved repository-stabilization sequence is mandatory:

| Step | Activity | Status |
|---|---|---|
| 1 | Repository State Audit | COMPLETED |
| 2 | Backup Checkpoint | COMPLETED |
| 3 | Documentation Synchronization | COMPLETED |
| 4 | Runtime Architecture Audit | COMPLETED |
| 5 | Full Automated Testing | COMPLETED |
| 6 | JAOS Shell Testing | COMPLETED WITH FINDINGS |
| 7 | Bug Fixing and Regression | IN PROGRESS |
| 8 | Stabilization Certification | PENDING — BLOCKED BY STEP 7 |
| 9 | Resume Phase 8 | PENDING |

The sequence must not be skipped or reordered without an approved engineering
decision.

Major Phase 8 expansion must remain paused until Step 8 and Fortress
certification pass and explicit Founder authorization is recorded.

---

## 9. Documentation Synchronization State

Step 3 — Documentation Synchronization is complete.

Step 6 completion documentation synchronization is COMPLETE.

The documentation checkpoint is:

`786abb3` docs(stabilization): certify Steps 4 through 6

The synchronized authoritative documentation checkpoint contains:

- `JAOS_MANIFEST.md`
- `docs/bootstrap/PROJECT_BOOTSTRAP.md`
- `docs/bootstrap/CONTINUATION_CONTEXT.md`
- `docs/project/ROADMAP.md`
- `docs/project/MILESTONES.md`
- `docs/project/PROJECT_STATE.md`
- `docs/project/CURRENT_SPRINT.md`
- `docs/project/NEXT_ACTIONS.md`

The transition evidence confirms:

- The locked 20-phase roadmap is preserved.
- The certified release remains `v0.9.0-alpha`.
- The development target remains `v0.10.0-alpha`.
- Phase 8 and MS-0025E remain active but temporarily paused.
- Steps 4 through 6 are certified in the documentation checkpoint.
- `git diff --check` passes for the reviewed documentation checkpoint.

---

## 10. Required Architecture Boundaries

All work must preserve the approved JAOS platform authority.

### Runtime Platform

The Runtime Platform controls:

- Application lifecycle
- Platform composition
- Startup and shutdown
- Component initialization
- Runtime health
- Runtime diagnostics

### Executive Platform

The Executive Platform remains authoritative for:

- System actions
- Task execution
- Action governance
- Approval coordination
- Execution outcomes

### Tool Platform

The Tool Platform remains authoritative for:

- Tool discovery
- Tool registration
- Tool permissions
- Tool authorization
- Tool invocation
- Tool results
- Tool execution auditing

### AI Platform

The AI Platform controls:

- AI provider access
- AI provider registration
- Provider selection
- Provider health
- Provider-independent AI execution

### Memory Platform

The Memory Platform controls:

- Persistent-memory access
- Memory-provider selection
- Memory transactions
- Memory serialization
- Memory lifecycle
- Memory storage and retrieval

### AI Intelligence Platform

The AI Intelligence Platform may:

- Interpret requests
- Build context
- Compose prompts
- Manage conversations
- Reason
- Generate plans
- Rank alternatives
- Produce structured proposals
- Coordinate intelligence components

The AI Intelligence Platform must not:

- Invoke tools directly
- Authorize protected actions
- Bypass the Executive Platform
- Bypass the Tool Platform
- Depend directly on concrete AI providers
- Depend directly on concrete memory providers
- Treat unvalidated model output as trusted system state
- Store hidden chain-of-thought as JAOS memory

Operational execution must pass through approved Executive and Tool Platform
authority.

---

## 11. Testing and Certification State

Historical test results do not constitute current stabilization certification.

Current authoritative states:

| Verification area | Status |
|---|---|
| Runtime Architecture Audit | COMPLETE |
| Full Automated Testing | COMPLETE |
| JAOS Shell Testing | COMPLETE WITH FINDINGS |
| Step 6 completion synchronization | COMPLETE |
| Bug Fixing and Regression | IN PROGRESS |
| Stabilization Certification | PENDING — BLOCKED BY STEP 7 |
| Phase 8 Certification | PENDING |

The current full regression count must be established during:

Step 5 — Full Automated Testing.

Testing must include all applicable:

- Syntax checks
- Import checks
- Static validation
- Unit tests
- Integration tests
- Full regression tests
- Runtime startup
- Runtime shutdown
- Platform composition
- Provider behavior
- Failure behavior
- JAOS Shell behavior
- Intelligence behavior
- Architecture-boundary validation

Warnings, skipped tests, expected failures, and confirmed defects must be
reviewed and documented.

No current certification claim may be based solely on an older test count.

---

## 12. Actions Authorized at the Current Fortress Checkpoint

The following actions are authorized:

- Read and compare authoritative repository documentation and audit evidence.
- Preserve the current RAA/SHT resolution evidence and unresolved finding state.
- Use `docs/architecture/FORTRESS_PROGRAM.md` as the governing Fortress record.
- Continue only Step 7 work that receives separate authorization.
- Record the Founder-approved Step 7 entry and checkpoint `786abb3`.
- Preserve Step 4, Step 5, and Step 6 completion evidence.
- Run non-mutating documentation and repository checks.
- Run `git diff --check`.

FORTRESS-01 authorized only the governance and documentation baseline it
recorded. It did not authorize later implementation. FORTRESS-02 slices 02A
through 02K, FORTRESS-03 slices 03A through 03J, FORTRESS-04, and FORTRESS-05
slices 05A through 05E were each implemented under separate authorization.
FORTRESS-02 through FORTRESS-04 are verified by sections 7.7 through 7.9;
FORTRESS-05 is verified under ADR-0011 by the closure evidence in section 7.10.
No authorization for FORTRESS-06, Step 8, or major Phase 8 expansion exists.

Each change must remain reviewable and recoverable.

---

## 13. Actions Not Authorized at the Current Fortress Checkpoint

Do not:

- Begin FORTRESS-06.
- Claim the Fortress Program certified.
- Modify production code, tests, or runtime data without separate
  authorization.
- Mark any finding resolved without evidence.
- Enter Step 8.
- Resume MS-0025E or major Phase 8 expansion.
- Add advanced reasoning, autonomous workflow, multi-agent runtime, advanced
  memory-driven action, PC control, voice, vision, IoT, robotics, or future
  cloud-GPU capability expansion.
- Start MS-0025G.
- Start MS-0025X.
- Claim MS-0025F certification.
- Rewrite Git history.
- Force-push.
- Reset the branch.
- Rebase.
- Merge.
- Pull.
- Stage partially reviewed files.
- Commit before the planning checkpoint is reviewed.
- Tag a release.
- Claim stabilization is complete.
- Change the locked roadmap structure.
- Create the reserved Technology Bible during this checkpoint.

Any unexpected repository discrepancy must be audited before proceeding.

---

## 14. Step 5 Completion Record

Step 5 — Full Automated Testing is complete.

The verified Step 5 evidence is:

- Python 3.14.6
- Pytest 9.1.1
- 1,590 tests collected in 5.66 seconds
- 1,590 tests passed in 9.78 seconds
- Zero failures, errors, skips, expected failures, unexpected passes, or warnings
- Syntax compilation exit code 0
- Dependency validation exit code 0
- No broken requirements
- Repository safety passed
- No implementation or test changes

The evidence is recorded in:

`docs/engineering/FULL_AUTOMATED_TEST_REPORT.md`

Founder/reviewer Vinay B approved Step 5 on 2026-08-12.

RAA-001 through RAA-009 remain assigned to controlled Step 7 remediation.

Step 5 remains complete. Step 6 evidence and findings are recorded in
Section 15.

---

## 15. Step 6 Completion Record

Step 6 — JAOS Shell Testing is complete with findings.

The verified Step 6 evidence is:

- Core shell workflow exit code: 0
- Filesystem workflow exit code: 0
- Cleanup workflow exit code: 0
- Edge-case workflow exit code: 0
- Lifecycle inspection exit code: 0
- EOF workflow exit code: 1
- Filesystem approval enforcement passed
- Sandbox cleanup confirmed
- Provider remained initialized after shell exit
- Immediate EOF produced an uncaught `EOFError`
- SHT-001 through SHT-006 were recorded and accepted for Step 7 remediation

The evidence is recorded in:

`docs/engineering/JAOS_SHELL_TEST_REPORT.md`

Founder/reviewer Vinay B approved Step 6 on 2026-08-12.

SHT-001 through SHT-006 are accepted for controlled Step 7 remediation alongside
RAA-001 through RAA-009.

Step 6 completion documentation synchronization is COMPLETE.

Founder/reviewer Vinay B approved entry into Step 7 on 2026-08-12.

The documentation checkpoint is:

`786abb3` docs(stabilization): certify Steps 4 through 6

---

## 16. Current Stabilization Activity

The current activity is:

Step 7 — Bug Fixing and Regression

Founder/reviewer Vinay B approved entry into Step 7 on 2026-08-12.

The documentation checkpoint is:

`786abb3` docs(stabilization): certify Steps 4 through 6

Step 6 completion documentation synchronization is COMPLETE.

RAA-001 through RAA-009 and SHT-001 through SHT-006 are authorized for
controlled remediation.

RAA-005 and RAA-008 are resolved with evidence. RAA-002 and RAA-007 are
partially resolved; RAA-009 remains open and deferred; other unresolved RAA
findings remain unresolved. Step 7 remains in progress; neither Step 8 nor
Fortress certification has begun.

The controlled Step 7 workflow is:

1. Build a finding-remediation matrix for RAA-001 through RAA-009 and
   SHT-001 through SHT-006.
2. Identify overlaps and dependencies.
3. Classify each finding as fix, documentation correction, or approved
   deferral.
4. Define acceptance tests before implementation.
5. Apply one controlled fix cluster at a time.
6. Run targeted tests after every cluster.
7. Run the complete automated and JAOS Shell regression suites.
8. Produce the Step 7 report for Founder review.

Step 8 — Stabilization Certification remains PENDING — BLOCKED BY STEP 7.

MS-0025E and Phase 8 implementation remain paused.

---

## 17. Phase 8 Resume Order

Major Phase 8 expansion resumes only after Step 8 and Fortress certification
pass and explicit Founder authorization is recorded.

The approved resume order is:

1. Resume MS-0025E — Reasoning and Planning Intelligence.
2. Complete reasoning contracts and behavior.
3. Complete planning contracts and behavior.
4. Complete reasoning and planning coordination.
5. Complete MS-0025E unit tests.
6. Complete MS-0025E integration tests.
7. Run the applicable regression suite.
8. Complete MS-0025G — Agent and Execution Proposal Foundations.
9. Complete MS-0025X — AI Intelligence Platform Composition.
10. Complete runtime integration.
11. Complete JAOS Shell integration.
12. Complete MS-0025F — AI Intelligence End-to-End Certification.
13. Synchronize Phase 8 documentation.
14. Certify and release `v0.10.0-alpha`.
15. Complete remaining Memory Platform production work.
16. Begin Phase 9 — Workflow & Automation Platform.

Completed Phase 8 work must not be repeated.

---

## 18. Remaining Memory Platform Production Work

After Phase 8, approved production-oriented Memory Platform work may include:

- Cloud-ready PostgreSQL deployment
- `pgvector` integration
- Semantic retrieval
- Vector retrieval
- S3-compatible object storage
- MinIO deployment
- Local and cloud synchronization
- Backup and recovery
- Retention policies
- Encryption
- Privacy controls
- Provider migration
- Production observability
- Performance validation
- Failure recovery
- Cost-aware storage selection

This work must extend the certified Memory Platform behind its approved
contracts.

It must not create higher-level dependencies on concrete storage providers.

---

## 19. Locked Roadmap Direction

The JAOS roadmap contains 20 phases and remains locked.

Current roadmap anchors include:

- Phase 7 — Memory Platform
- Phase 8 — AI Intelligence Platform
- Phase 9 — Workflow & Automation Platform
- Phase 19 — JAOS Experience Platform
- Phase 20 — Production Certification & Public Release

Phase 7 is complete.

Phase 8 is active and temporarily paused for stabilization.

Phase 9 and all later phases remain planned.

JAOS must not publish `v1.0` before Phase 20 certification.

The roadmap must not be redesigned, renumbered, or structurally changed without
explicit Founder approval and synchronized engineering documentation.

---

## 20. Permanent Product Principles

JAOS development must preserve:

### Single-PC-First Engineering

JAOS is currently developed and stabilized on one primary PC.

Future distributed capabilities must not destabilize this baseline.

### Adaptive Resource Management

Hardware differences should change execution strategy, performance, quality,
latency, concurrency, model size, batching, caching, scheduling, and placement.

Core capabilities must not be removed merely because a system has lower
specifications when another practical execution strategy exists.

### Monitoring and Observability

JAOS must provide visibility into hardware, runtime, providers, platforms,
failures, performance, and health.

### Cost Efficiency

JAOS must prefer suitable open-source, local-first, provider-independent,
self-hostable, and free-tier components.

Paid services must remain optional, justified, and controlled by user-defined
budgets.

### Provider Independence

AI, memory, storage, tools, workflows, and infrastructure must depend on stable
contracts wherever practical.

### Security and Auditability

JAOS actions must remain permission-controlled, explainable, traceable,
auditable, and recoverable where practical.

---

## 21. Reserved Technology Documentation

The reserved document is:

`docs/architecture/JAOS_TECHNOLOGY_BIBLE.md`

It must not be created during the current repository-stabilization checkpoint.

It should be created after the Memory and AI Intelligence Platforms are mature
and before:

- Phase 19 — JAOS Experience Platform
- Phase 20 — Production Certification & Public Release

The Technology Bible must describe stable and certified architecture rather
than rapidly changing implementation.

---

## 22. Exact Next Actions

1. Preserve the FORTRESS-01 governance baseline and canonical target.
2. Preserve the verified FORTRESS-02 slice state for 02A through 02K, the
   verified FORTRESS-03 slice state for 03A through 03J, and the verified
   FORTRESS-04 and FORTRESS-05 state.
3. Preserve RAA-005 and RAA-008 resolution evidence, the RAA-004 and RAA-006
   evidence recorded under FORTRESS-03, and the RAA-001 lifecycle/reachability
   evidence recorded under FORTRESS-04. Keep RAA-002 and RAA-007 partial,
   RAA-009 open/deferred, and other unresolved findings open.
4. Continue only separately authorized Step 7 remediation.
5. Keep Step 8 — Stabilization Certification PENDING — BLOCKED BY STEP 7 until
   Step 7 is complete and approved.
6. Do not begin FORTRESS-06 without separate authorization.
7. Execute the skipped directory-symlink escape rejection check in an elevated
   or capable environment before Fortress certification.
8. Keep major Phase 8 expansion paused until Step 8 and Fortress certification
   pass and explicit Founder authorization is recorded.

Do not modify production code, tests, or runtime data under FORTRESS-01.

Do not mark any finding resolved without evidence.

Do not enter Step 8 or resume major Phase 8 expansion before the complete
Fortress gate passes.

---

## 23. Current Command-Level Action

FORTRESS-02 through FORTRESS-05 are COMPLETE AND VERIFIED at workstream level,
with closure evidence recorded in `docs/architecture/FORTRESS_PROGRAM.md`
sections 7.7 through 7.10. RAA-002 and RAA-007 remain partially resolved, and
RAA-009 remains open. Continue only separately authorized Step 7 work. Do not
begin FORTRESS-06, claim Fortress Program certification, enter Step 8, resume
MS-0025E, or resume major Phase 8 expansion.

The following remain explicitly open and unchanged: the directory-symlink
escape validation is unverified on this host; composed Memory is not used by
live CLI behavior; composed Conversation Intelligence is not production
request-routed; RAA-009 and the
`MemoryContextSource`/`MemorySearchEngine` adapter remain deferred; `main.py`
retirement and legacy quarantine belong to FORTRESS-06;
the lazy Intelligence facade and compatibility self-construction fallbacks are
interim FORTRESS-06 debt;
permission/approval/audit policy hardening belongs to FORTRESS-07;
`config/providers.json` ownership remains deferred; the operational policy for
`PlatformRuntime.mark_degraded()` remains FORTRESS-10; advanced reasoning,
planning, agents, execution proposals, and autonomy remain paused; Fortress
certification has not started; Step 7 remains in progress; and Step 8 remains
blocked by Step 7.
