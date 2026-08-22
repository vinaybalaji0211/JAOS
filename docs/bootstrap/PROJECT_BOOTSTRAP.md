# Project Bootstrap

Version: 3.1

Status: ACTIVE

Owner: Vinay B

Maintainer: JAOS Engineering

Document Role: Permanent Engineering Session Bootstrap

Roadmap Scope: 20 Phases

Certified Release: v0.9.0-alpha

Development Target: v0.10.0-alpha

Current Phase: Phase 8 — AI Intelligence Platform

Current Milestone: MS-0025E — Reasoning and Planning Intelligence

Execution State: Major Phase 8 expansion paused for stabilization and Fortress certification

---

## 1. Purpose

This document defines how every JAOS engineering session begins, operates, and

continues.

It establishes:

- Repository authority

- Mandatory repository entry order

- Current engineering checkpoint

- Development lifecycle

- Stabilization requirements

- Testing and certification gates

- Documentation workflow

- Git safety rules

- Architecture-preservation rules

- Continuation protocol

Every human or AI contributor must follow this bootstrap before modifying JAOS.

The repository must always contain enough accurate information for a new

engineering session to resume without depending on conversational history.

---

## 2. Repository Authority

The Git repository is the permanent engineering source of truth for JAOS.

Repository documentation takes precedence over conversational history unless the

Founder explicitly approves a new decision and that decision is synchronized

into the repository.

The locked master roadmap is maintained in:

`docs/project/ROADMAP.md`

The roadmap contains 20 phases.

Its phase numbering, phase boundaries, and approved long-term structure must not

be redesigned, renumbered, or replaced without explicit Founder approval and a

documented engineering decision.

If implementation, documentation, Git history, and conversational context

disagree, development must pause until the discrepancy is audited.

Completed and certified work must not be repeated or discarded without an

approved reason.

---

## 3. Current Engineering Checkpoint

| Item | Current state |

|---|---|

| Certified release | v0.9.0-alpha |

| Development target | v0.10.0-alpha |

| Current phase | Phase 8 — AI Intelligence Platform |

| Milestone family | MS-0025 |

| Active milestone | MS-0025E — Reasoning and Planning Intelligence |

| Phase 8 execution | Major expansion paused — Fortress hard gate |

| Stabilization activity | Step 7 — Bug Fixing and Regression |

| Stabilization step | Step 7 of 9 — IN PROGRESS |

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

| FORTRESS-03 | NOT STARTED - AWAITING EXPLICIT FOUNDER AUTHORIZATION |

| Repository health | STABILIZATION IN PROGRESS |

| Architecture health | FORTRESS HARDENING REQUIRED |

| Full regression certification | PENDING |

| Fortress certification | NOT STARTED |

| Phase 8 release readiness | NOT YET CERTIFIED |

Phase 7 — Memory Platform is complete, certified, released, tagged, and pushed

as:

`v0.9.0-alpha`

Phase 8 implementation remains preserved.

The Phase 8 pause is a controlled repository-stabilization checkpoint.

It is not:

- A rollback

- A phase restart

- An implementation failure

- A roadmap revision

- Authorization to discard completed work

Major Phase 8 expansion may resume only after Step 8 and Fortress certification
are complete and explicit Founder authorization is recorded.

---

## 4. Mandatory Repository Entry Order

Every JAOS engineering session must begin by reading these documents in order:

1. `JAOS_MANIFEST.md`

2. `docs/bootstrap/PROJECT_BOOTSTRAP.md`

3. `docs/bootstrap/CONTINUATION_CONTEXT.md`

4. `docs/project/PROJECT_STATE.md`

5. `docs/project/CURRENT_SPRINT.md`

6. `docs/project/NEXT_ACTIONS.md`

7. `docs/architecture/FORTRESS_PROGRAM.md`

After the primary entry documents, read the documents governing the active work,

including:

- `docs/project/ROADMAP.md`

- `docs/project/MILESTONES.md`

- `docs/project/PHASE8_MILESTONES.md`

- Relevant requirements documents

- Relevant architecture documents

- Relevant governance documents

- Relevant technical-debt documents

- Relevant audit and certification documents

After reading the repository documentation:

- Confirm the active branch.

- Confirm the certified release.

- Confirm the development target.

- Confirm the current phase.

- Confirm the current milestone.

- Confirm the active checkpoint.

- Inspect modified, staged, and untracked files.

- Continue directly from the documented next action.

- Do not repeat completed work.

- Do not redesign approved architecture.

---

## 5. Session Bootstrap Procedure

At the beginning of every engineering session:

1. Activate the approved Python virtual environment.

2. Enter the JAOS repository root.

3. Confirm the active Git branch.

4. Inspect the repository status.

5. Inspect modified, staged, and untracked files.

6. Read the mandatory repository entry documents.

7. Confirm the current engineering checkpoint.

8. Review the relevant milestone, requirements, and architecture documents.

9. Preserve all existing work.

10. Execute only the approved next action.

11. Validate the completed action.

12. Update documentation when required.

13. Leave the repository resumable.

For the current Windows development environment, commands must be provided for

CMD unless the Founder explicitly requests another shell.

During controlled workflows:

- Provide complete commands.

- Perform one approved step at a time.

- Wait for command output before advancing.

- Do not assume that a command passed without reviewing its output.

- Do not stage or commit partially reviewed work.

---

## 6. Locked Roadmap Rules

The JAOS master roadmap contains 20 phases and is locked.

Current roadmap anchors include:

- Phase 7 — Memory Platform

- Phase 8 — AI Intelligence Platform

- Phase 9 — Workflow & Automation Platform

- Phase 19 — JAOS Experience Platform

- Phase 20 — Production Certification & Public Release

The following rules are permanent:

- Do not renumber approved phases.

- Do not redesign completed phases.

- Do not silently move capabilities between phases.

- Do not remove approved long-term requirements.

- Do not start later phases before their required predecessors.

- Do not publish `v1.0` before Phase 20 certification.

- Record every approved roadmap revision in repository documentation.

Phase 7 is complete.

Phase 8 is active and temporarily paused for stabilization.

Phase 9 and all later phases remain planned.

---

## 7. Permanent End-to-End Engineering Lifecycle

Every JAOS phase and implementation milestone follows this lifecycle:

1. Requirements

2. Architecture Design

3. Implementation Planning

4. Implementation

5. Unit Testing

6. Integration Testing

7. Runtime Verification

8. JAOS Shell Verification

9. Bug Fixing

10. Regression Testing

11. Architecture Audit

12. Code-Quality Audit

13. Dependency Audit

14. Technical-Debt Review

15. Security and Performance Review

16. Documentation Synchronization

17. Certification

18. Git Commit, Tag, and Push

19. Next-Phase Planning

No milestone or phase is complete merely because its implementation has been

written.

Completion requires all applicable architecture, testing, integration, runtime,

documentation, audit, certification, and release gates to pass.

Engineering quality takes precedence over development speed.

---

## 8. Stabilization Sprint

Every implementation phase concludes with a mandatory Stabilization Sprint.

Required activities include:

- Repository-state audit

- Architecture audit

- Code-quality audit

- Dependency audit

- Technical-debt review

- Security review

- Performance review

- Test and coverage audit

- Runtime verification

- JAOS Shell verification

- Bug fixing

- Regression testing

- Documentation synchronization

- Stabilization certification

A failed gate must be investigated and resolved before release.

Warnings, skipped tests, expected failures, and deferred defects must be reviewed

and documented rather than silently ignored.

Only after the applicable certification gates pass may the release process

continue.

---

## 9. Current Repository-Stabilization Sequence

The current repository-stabilization sequence is mandatory:

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

This sequence must not be skipped or reordered without an approved engineering

decision.

Latest completed activity:

Step 6 — JAOS Shell Testing

Step 6 was completed with findings. The approved shell-test report is recorded
in:

`docs/engineering/JAOS_SHELL_TEST_REPORT.md`

Founder/reviewer Vinay B approved Step 6 on 2026-08-12.

The verified Step 6 evidence is:

- Core shell workflow exit code: 0

- Filesystem workflow exit code: 0

- Cleanup workflow exit code: 0

- Edge-case workflow exit code: 0

- Lifecycle inspection exit code: 0

- EOF workflow exit code: 1

- Filesystem approval enforcement passed

- Sandbox cleanup was confirmed

- Provider remained initialized after shell exit

- Immediate EOF produced an uncaught `EOFError`

- SHT-001 through SHT-006 are accepted for Step 7 remediation

Step 5 — Full Automated Testing remains COMPLETED and recorded in:

`docs/engineering/FULL_AUTOMATED_TEST_REPORT.md`

RAA-001 through RAA-009 and SHT-001 through SHT-006 remain assigned to Step 7
remediation.

Step 6 completion synchronization is COMPLETE.

The documentation checkpoint is:

`786abb3` docs(stabilization): certify Steps 4 through 6

Founder/reviewer Vinay B approved Step 7 entry on 2026-08-12.

Current stabilization activity:

Step 7 — Bug Fixing and Regression

RAA-001 through RAA-009 and SHT-001 through SHT-006 are authorized for

controlled Step 7 remediation.

RAA-005 and RAA-008 are resolved with evidence. Other unresolved RAA findings
remain unresolved. Step 7 remains in progress; neither Step 8 nor Fortress
certification has begun.

The controlled Step 7 continuation instructions are:

1. Preserve completed Step 7 remediation evidence and unresolved finding state.

2. Use the Fortress Program as the mandatory architecture and hardening gate.

3. Do not begin FORTRESS-02K or FORTRESS-03 without separate authorization.

4. Classify each finding as fix, documentation correction, or approved

   deferral.

5. Define acceptance tests before implementation.

6. Apply one controlled fix cluster at a time.

7. Run targeted tests after each cluster.

8. Run full automated and shell regression suites.

9. Produce the Step 7 report for Founder review.

Next pending activity:

Step 8 — Stabilization Certification

Step 8 remains PENDING — BLOCKED BY STEP 7 until Step 7 completes and receives

Founder review.

Major Phase 8 expansion must remain paused until Step 8 and Fortress
certification pass and explicit Founder authorization to resume is recorded.

---

## 10. Architecture Authority

JAOS implementation must preserve established platform authority:

- The Runtime Platform controls lifecycle and platform composition.

- The Executive Platform remains the system-action authority.

- The Tool Platform remains the controlled execution boundary.

- Permission and approval systems remain authoritative.

- The AI Platform controls AI-provider access.

- The Memory Platform controls persistent-memory access.

- The AI Intelligence Platform may reason, plan, rank, and propose actions.

- Intelligence components must not directly execute tools.

- Executable actions must pass through authorized platform boundaries.

- Components must depend on contracts rather than concrete providers.

- Provider independence must be preserved.

- Significant decisions and actions must remain auditable.

- Certified public contracts must not be changed accidentally.

Architecture boundaries must not be bypassed for implementation convenience.

Any intentional architectural change requires:

1. A documented reason

2. Impact analysis

3. Founder approval where required

4. Updated requirements and architecture documentation

5. Implementation and migration planning

6. Testing and regression coverage

7. Documentation synchronization

8. Certification

---

## 11. Engineering Principles

JAOS follows these permanent principles:

- Architecture-first engineering

- Interface-first development

- Modular design

- Clean separation of concerns

- Dependency inversion

- Provider independence

- Repository-backed engineering

- Documentation-backed continuity

- Test-driven certification

- Security by design

- Auditable execution

- Backward compatibility where practical

- Thread-safe component design

- Local-first operation where practical

- Cloud and remote execution where justified

- Cost-aware provider and resource selection

- Single-PC-first development

- Incremental hardware scaling

- Continuous monitoring and stabilization

- Production-quality engineering standards

JAOS must remain maintainable, modular, secure, auditable, provider-independent,

hardware-adaptive, and cost-efficient.

---

## 12. Development Rules

Every engineering session must follow these rules:

- Read repository documentation before implementation.

- Preserve the locked 20-phase roadmap.

- Preserve approved architecture and platform boundaries.

- Use complete-file rewrites when changing files.

- Preserve public APIs unless a change is intentional and documented.

- Maintain backward compatibility where practical.

- Keep implementations modular and testable.

- Make one controlled change at a time during stabilization.

- Validate every changed document or component.

- Run the approved tests before certification.

- Complete runtime and JAOS Shell verification where applicable.

- Record confirmed defects and technical debt.

- Record significant architectural decisions.

- Synchronize documentation before certification and release.

- Keep the repository recoverable and resumable.

- Preserve all current Phase 8 work.

- Do not add functionality during the stabilization pause.

- Wait for the current checkpoint to pass before advancing.

Every completed milestone must leave a clear continuation point.

---

## 13. Documentation Workflow

Documentation follows a repository-first workflow.

During implementation:

- Maintain the documentation queue.

- Record architectural decisions.

- Record technical debt.

- Record architecture watch items.

- Record confirmed defects.

- Record test and runtime evidence.

- Record deferred production work.

During documentation synchronization:

- Audit authoritative documents one at a time.

- Compare documented state with implementation and Git history.

- Remove stale release, phase, milestone, and status claims.

- Preserve approved roadmap structure.

- Normalize malformed Markdown.

- Validate internal consistency.

- Run `git diff --check`.

- Review modified, staged, and untracked files.

- Do not stage partially reviewed documentation.

Documentation must describe the real repository state.

Documentation must not declare implementation, certification, or release complete

without supporting evidence.

---

## 14. Testing and Runtime Verification

Before certification, the applicable verification sequence must include:

1. Static and syntax validation

2. Unit tests

3. Integration tests

4. Full automated regression tests

5. Runtime startup verification

6. Runtime shutdown verification

7. JAOS Shell verification

8. Platform composition verification

9. Provider and dependency verification

10. Failure-path verification

11. Bug fixing

12. Regression confirmation

Test counts and results must be recorded accurately.

A previous test result must not be treated as current certification after relevant

implementation or environment changes.

No release may depend only on partial test-suite success.

---

## 15. Release Requirements

Before creating a release commit or tag, verify:

- Approved implementation is complete.

- Unit tests pass.

- Integration tests pass.

- Full regression tests pass.

- Runtime verification passes.

- JAOS Shell verification passes where applicable.

- Architecture audit passes.

- Code-quality audit passes.

- Dependency audit passes.

- Technical-debt review is complete.

- Security and performance reviews are complete.

- Documentation is synchronized.

- Certification records are complete.

- Modified files are reviewed.

- No unintended untracked files exist.

- No unintended staged files exist.

- `git diff --check` passes.

- Release version and tag are correct.

- Git status is clean after the release commit.

- The approved branch is pushed successfully.

No release tag may be created before certification.

A release is not complete until its approved commit and tag are pushed and the

repository state is verified.

---

## 16. Git and Repository Safety

Before modifying repository history or state:

- Inspect the active branch.

- Inspect `git status`.

- Inspect modified files.

- Inspect staged files.

- Inspect untracked files.

- Confirm the exact intended targets.

- Preserve unrelated user changes.

- Create or verify a recoverable checkpoint when required.

Do not delete, reset, merge, pull, rebase, force-push, or rewrite history without

an explicit audit and approved reason.

Do not use destructive Git commands to solve an unclear repository state.

Do not stage or commit files until their scope and validation results have been

reviewed.

Commits must be intentional, focused, and accurately described.

---

## 17. Phase 8 Resume Control

After Step 8 and Fortress certification are complete and explicit Founder
authorization is recorded, Phase 8 resumes from:

MS-0025E — Reasoning and Planning Intelligence

The approved resume order is:

1. Resume MS-0025E — Reasoning and Planning Intelligence.

2. Complete reasoning contracts and behavior.

3. Complete planning contracts and behavior.

4. Complete MS-0025E testing.

5. Complete MS-0025G — Agent and Execution Proposal Foundations.

6. Complete MS-0025X — AI Intelligence Platform Composition.

7. Complete runtime and JAOS Shell integration.

8. Complete MS-0025F — AI Intelligence End-to-End Certification.

9. Synchronize Phase 8 documentation.

10. Certify and release `v0.10.0-alpha`.

11. Complete remaining Memory Platform production work.

12. Begin Phase 9 — Workflow & Automation Platform.

Completed Phase 8 implementation must not be restarted, discarded, or redesigned

without an approved engineering decision.

---

## 18. Reserved Technology Documentation

The following architecture document remains reserved:

`docs/architecture/JAOS_TECHNOLOGY_BIBLE.md`

It must not be created during the current stabilization checkpoint.

It should be created after the Memory and AI Intelligence Platforms are mature

and before the JAOS Experience and Production Certification phases.

Its purpose is to document stable architecture, techniques, technologies, AI

concepts, platform boundaries, security, monitoring, resource management, and

cost-management decisions.

---

## 19. Permanent Product Principles

### Adaptive Resource Management

JAOS must adapt automatically to available CPU, RAM, GPU, VRAM, storage, network,

battery, thermal limits, operating system, and connected accelerators.

Hardware differences should change execution strategy, model size, concurrency,

quality, latency, caching, scheduling, and local-versus-remote placement.

Core capabilities must not be removed merely because a system has lower

specifications when another technically practical execution strategy exists.

### Monitoring and Observability

JAOS must monitor system resources, platform health, provider health, runtime

behavior, performance history, failures, and anomalies.

### Cost Efficiency

Cost efficiency is a first-class architecture requirement.

JAOS must prefer suitable open-source, local-first, provider-independent, and

self-hostable components while preserving quality and security.

JAOS must support cost-aware routing, budgets, quotas, alerts, forecasting,

caching, quantization, and automatic fallback.

### Provider Independence

JAOS must avoid unnecessary vendor lock-in.

AI, memory, storage, tools, workflows, and infrastructure must depend on stable

contracts wherever practical.

---

## 20. Continuation Protocol

At the end of every engineering session:

1. Confirm what was completed.

2. Confirm what remains incomplete.

3. Record the current phase and milestone.

4. Record the exact next action.

5. Record relevant test and runtime results.

6. Record confirmed defects and technical debt.

7. Synchronize affected documents.

8. Inspect repository status.

9. Preserve unstaged and untracked work.

10. Leave complete continuation instructions.

At the start of the next session:

1. Read the mandatory repository entry documents.

2. Verify the branch and repository state.

3. Confirm the documented checkpoint.

4. Review pending changes.

5. Continue from the exact next action.

6. Do not repeat completed work.

If repository documentation conflicts with the repository state, stop and audit

the conflict before implementation continues.

---

## 21. Current Development Target

Certified release:

`v0.9.0-alpha`

Development target:

`v0.10.0-alpha`

Current phase:

Phase 8 — AI Intelligence Platform

Current milestone:

MS-0025E — Reasoning and Planning Intelligence

Current execution state:

Major Phase 8 expansion paused for stabilization and Fortress certification

Latest completed stabilization activity:

Step 6 — JAOS Shell Testing

Current activity:

Step 7 — Bug Fixing and Regression

Active stabilization step:

Step 7 — Bug Fixing and Regression

Step 7 entry status:

APPROVED — IN PROGRESS

Next pending stabilization activity:

Step 8 — Stabilization Certification

Step 8 entry status:

PENDING — BLOCKED BY STEP 7

Major Phase 8 expansion may resume only after Step 8 and Fortress certification
and explicit Founder authorization.

---

## 22. Continuity Promise

A new human or AI engineering session must be able to resume JAOS development

using only the Git repository and its documentation.

The repository must always remain:

- Accurate

- Recoverable

- Auditable

- Testable

- Documented

- Versioned

- Immediately resumable

Implementation, architecture, tests, documentation, audits, certification

records, and Git history are equally important parts of the JAOS engineering

system.

The objective is not merely to build features.

The objective is to build a long-lived, maintainable, extensible, secure,

cost-efficient, production-grade Artificial Intelligence Operating System.
