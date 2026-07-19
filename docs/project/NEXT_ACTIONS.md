# JAOS Next Actions

Version: 3.0
Status: ACTIVE
Owner: Vinay B
Maintainer: JAOS Engineering
Current Release: v0.9.0-alpha
Current Phase: Phase 8 — AI Intelligence Platform
Current Branch: phase8-ai-intelligence

---

## 1. Current Engineering State

Phase 7 — Memory Platform is complete, certified, released, tagged, and pushed.

Verified release baseline:

- Release: v0.9.0-alpha
- Regression suite: 805 tests passed
- Provider-independent Memory Platform: complete
- In-memory, SQLite, and PostgreSQL foundations: complete
- Phase 7 architecture audit: complete
- Phase 7 technical debt review: complete
- Phase 7 certification: complete
- Phase 8 development branch: active and synchronized

Phase 8 architecture is established in:

`docs/architecture/AI_INTELLIGENCE_ARCHITECTURE.md`

Architecture baseline commit:

`e5f5e33 — docs: establish Phase 8 AI Intelligence architecture`

---

## 2. Immediate Priority

Complete Phase 8 engineering planning before implementation begins.

The architecture baseline is complete. The next required activities are:

1. Review existing Phase 8 requirements.
2. Create the Phase 8 milestone breakdown.
3. Assign milestone identifiers using the existing repository sequence.
4. Synchronize the roadmap and active project documents.
5. Begin the first approved implementation milestone.

Milestone identifiers must not be invented before `MILESTONES.md` is reviewed.

---

## 3. Phase 8 Objectives

Phase 8 will establish the intelligence layer that connects user interaction,
the AI Platform, the Memory Platform, and the existing execution infrastructure.

Primary objectives:

- Intelligence Manager facade
- Intelligence domain models
- Conversation Engine
- Context Manager
- Prompt Composer
- Reasoning Engine
- Planning Intelligence Engine
- Agent Orchestrator foundation
- Execution Proposal Engine
- AI Platform integration
- Memory Platform integration
- Intelligence diagnostics and telemetry

---

## 4. Required Platform Boundaries

All Phase 8 work must preserve the approved architecture.

- AI providers are accessed only through AI Platform interfaces.
- Memory providers are accessed only through Memory Platform interfaces.
- Intelligence components may reason, recommend, and propose actions.
- Intelligence components may not authorize protected actions.
- Intelligence components may not invoke tools directly.
- Operational plans remain managed by Planning Manager.
- Decisions remain controlled by Decision Manager.
- Execution remains coordinated by Execution Manager.
- Results remain managed by Result Manager.
- Tool authorization and invocation remain inside the Tool Platform.
- Model output is untrusted until validated into structured domain models.
- Hidden chain-of-thought is never stored as JAOS memory.

---

## 5. Proposed Implementation Order

The final milestone identifiers will be assigned after the repository milestone
sequence is reviewed.

### Foundation

- Intelligence domain models
- Component protocols and interfaces
- Validation and structured error models
- Package exports

### Context and Prompt Composition

- Context item and context bundle construction
- Context ranking and size limits
- Memory Platform retrieval boundary
- Provider-neutral prompt composition

### Conversation Intelligence

- Conversation sessions
- Conversation turns
- Multi-turn state
- Working-memory integration
- Approved conversation persistence

### Reasoning and Planning Intelligence

- Structured reasoning requests and results
- Assumptions, risks, alternatives, and confidence
- Structured plan proposals
- Planning Manager handoff

### Agent and Execution Foundations

- Agent descriptors and capability routing
- Structured agent tasks and results
- Execution proposals
- Permission and risk metadata
- Executive and Manager Platform handoff

### Integration and Stabilization

- AI Platform integration tests
- Memory Platform integration tests
- Executive and Manager integration tests
- Runtime diagnostics
- Architecture review
- Technical debt review
- Stabilization Sprint
- Phase certification and release

---

## 6. First Implementation Target

After requirements and milestone planning are approved, implementation begins
with the Intelligence domain models and component interfaces.

This foundation must be completed before conversation, context, reasoning,
planning, or agent orchestration engines are implemented.

The first target must define stable, provider-independent, storage-independent,
and serializable contracts for the rest of Phase 8.

---

## 7. Documentation Synchronization

After the Phase 8 requirements and milestone breakdown are approved, update:

1. `docs/project/MILESTONES.md`
2. `docs/project/ROADMAP.md`
3. `docs/project/CURRENT_SPRINT.md`
4. `docs/project/PROJECT_STATE.md`
5. `docs/bootstrap/CONTINUATION_CONTEXT.md`
6. `docs/bootstrap/PROJECT_BOOTSTRAP.md`
7. `JAOS_MANIFEST.md` when its active target changes

Documentation synchronization must be completed once for the Phase 8 planning
baseline and then maintained at milestone boundaries.

---

## 8. Cloud Memory Commitment

The provider-independent Cloud Memory architecture remains an approved future
capability and must remain compatible with Phase 8.

Preserved architecture:

- PostgreSQL and pgvector for structured and semantic memory
- S3-compatible object storage for large artifacts
- MinIO for the initial local object-storage deployment
- Client-side encryption and TLS
- Per-user keys and device authentication
- Scoped agent permissions and short-lived tokens
- Immutable audit logs, versioning, backups, and recovery testing
- Local, MinIO, S3, encrypted, and hybrid storage providers behind stable
  provider interfaces

Phase 8 must use Memory Platform abstractions and must not bind intelligence
components directly to these storage technologies.

---

## 9. Engineering Workflow

Every Phase 8 milestone must follow this lifecycle:

1. Confirm scope and architecture boundary.
2. Implement complete components.
3. Add unit tests.
4. Add integration tests where required.
5. Run targeted tests.
6. Run the full regression suite.
7. Perform architecture review.
8. Record technical debt when applicable.
9. Update milestone documentation.
10. Commit and push the locked milestone.

Phase 8 must finish with a Stabilization Sprint before release.

---

## 10. Phase 8 Planning Exit Criteria

Phase 8 planning is complete when:

- Requirements are reviewed and documented.
- Milestone identifiers and scopes are approved.
- The roadmap is synchronized.
- Current project and bootstrap documents identify Phase 8 correctly.
- The first implementation milestone has explicit acceptance criteria.
- Existing AI, Memory, Executive, Manager, and Tool boundaries are preserved.
- The repository is clean, committed, and pushed.

After these conditions are satisfied, Phase 8 implementation may begin.

---

## 11. Next Command-Level Action

Inspect the existing requirements documents and the Phase 8 entries in
`MILESTONES.md` before assigning milestone identifiers or creating code.