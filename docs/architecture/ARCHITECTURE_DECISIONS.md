\# Architecture Decisions



Version: 1.3

Status: ACTIVE

Owner: Vinay B

Maintainer: JAOS Engineering



\---



\# Purpose



This document records permanent Architecture Decision Records (ADRs) for JAOS.



Each decision explains why a major architectural choice was made and serves as guidance for future development.



\---



\# ADR-0001



Title



Layered Platform Architecture



Status



Accepted



Decision



JAOS is organized into independent platforms with clearly defined responsibilities.



Architecture



CLI



↓



Executive Platform



↓



Executive AI Gateway



↓



AI Platform



↓



Provider Platform



↓



Tool Platform



↓



Runtime Platform



Reason



Clear separation of concerns, maintainability, scalability, and testability.



\---



\# ADR-0002



Title



AIManager as a Facade



Status



Accepted



Decision



AIManager serves only as the public entry point for the AI Platform.



Business logic is delegated to specialized managers.



Reason



Prevent AIManager from becoming a monolithic class while preserving a stable public API.



\---



\# ADR-0003



Title



Executive AI Gateway



Status



Accepted



Decision



The Executive Platform communicates with the AI Platform only through the Executive AI Gateway.



Reason



Protect platform boundaries and prevent Executive dependencies on AI internals.



\---



\# ADR-0004



Title



Provider Abstraction Layer



Status



Accepted



Decision



All AI providers implement the common provider interface and are managed through ProviderManager.



Reason



Support multiple providers while keeping the AI Platform provider-independent.



\---



\# ADR-0005



Title



Composition Root



Status



Accepted



Decision



The AI Platform is assembled through AIPlatformComposition.



Reason



Centralize dependency wiring while keeping components modular.



\---



\# ADR-0006



Title



Public API Governance



Status



Accepted



Decision



Only documented public interfaces may be consumed by external platforms.



Internal modules may change without affecting platform consumers.



Reason



Maintain backward compatibility and reduce coupling.



\---



\# ADR-0007



Title



Stabilization Sprint



Status



Accepted



Decision



Every implementation phase concludes with a Stabilization Sprint before release.



Required activities



\- Architecture Audit

\- Code Quality Audit

\- Dependency Audit

\- Test Audit

\- Runtime Certification

\- Documentation

\- Release



Reason



Improve software quality and maintain engineering consistency.



\---



\# ADR-0008



Title



Repository-First Continuity



Status



Accepted



Decision



Repository documentation is the authoritative engineering record.



Future development sessions resume from repository documentation instead of conversation history.



Reason



Provide reliable continuity across engineering sessions.



\---



\# ADR-0009



Title



Fortress Program Hard Gate and Canonical Runtime Target



Status



Accepted



Decision



JAOS Architectural Unification & Runtime Hardening (the "Fortress Program") is
the mandatory hard gate before major Phase 8 intelligence expansion.



The canonical production target is `run_jaos.py` as the sole thin launcher into
the Runtime Platform-owned `PlatformRuntime`, governed by `BootManager` lifecycle
control and the canonical Memory, AI, Executive, Tool, Permission, Approval,
Audit, and Tool Execution path.



`CommandDispatcher` is an injected interface adapter, not a composition root.
Intelligence remains proposal-only: Intelligence proposes; Executive executes.



The approved program definition, sequencing, preservation rules, migration and
quarantine constraints, current stabilization relationship, and certification
gate are maintained in `docs/architecture/FORTRESS_PROGRAM.md`.



Consequences



- Step 7 history and prior audit evidence remain unchanged.
- Step 8 Stabilization Certification has not begun.
- Existing Phase 6 and Phase 7 certifications are not revoked or rewritten.
- Legacy and shadow paths require controlled migration and quarantine; this
  decision does not authorize deletion.
- FORTRESS-01 through FORTRESS-12 must complete with evidence before Fortress
  certification and explicit authorization to resume major Phase 8 expansion.



Approved By



Founder Vinay B — 2026-08-21



\---



\# ADR-0010



Title



FORTRESS-02 Runtime Path Ownership and Isolation



Status



Accepted



Context



JAOS currently has repository-relative runtime-data writers, tracked runtime
artifacts, and tests that can mutate repository state. FORTRESS-02 requires one
owner for production runtime paths and disposable isolated test state without
rewriting or automatically migrating existing data.



Decision



`jaos_platform` owns runtime-path resolution. The canonical abstractions to be
implemented later are `RuntimePaths` and `RuntimePathResolver`.



`RuntimePaths` is an immutable typed contract. `PlatformRuntime` resolves and
injects it exactly once at the composition root. Resolution precedence is:



1. Explicitly injected `RuntimePaths`.
2. An absolute `JAOS_RUNTIME_DIR` environment override.
3. The operating-system local application-data default.



Subsystems must not independently resolve runtime roots. `run_jaos.py` remains
a thin launcher, and each subsystem receives only the path scopes it owns.
Subsystems must not construct internal runtime paths from the current working
directory, repository root, `C:\JARVIS`, or private hard-coded data directories.



Operating-System Defaults



- Windows: `%LOCALAPPDATA%\JAOS`
- Linux: `$XDG_DATA_HOME/jaos`, falling back to `~/.local/share/jaos`
- macOS: `~/Library/Application Support/JAOS`



The initial implementation uses the Python standard library. `platformdirs` is
not added during FORTRESS-02 unless later evidence establishes a need.



Versioned Layout



```text
<runtime-root>/
└── v1/
    └── profiles/
        └── <profile-id>/
            ├── config/
            ├── memory/
            ├── state/
            ├── recovery/
            ├── audit/
            ├── logs/
            ├── exports/
            ├── backups/
            ├── migrations/
            └── tmp/
```



Profile Semantics



The current single-user profile identifier is `default`. It is not derived
from the operating-system username. Future profiles may add identifiers without
changing the runtime-root contract.



Profile identifiers must match `^[A-Za-z0-9_-]{1,64}$`. This grammar and the
resolver containment checks must reject `..`, path separators, absolute paths,
drive-qualified paths, UNC paths, traversal, and junction or symlink escape.



Repository Containment



Production JAOS internal runtime state must never default inside the Git
working tree. `JAOS_RUNTIME_DIR` must be absolute. When repository context is
known, the resolver must reject a root whose resolved location is inside the
repository. Tests must use disposable temporary roots rather than weaken this
protection.



Secrets Boundary



`RuntimePaths` is not a secret-storage mechanism. Credentials, API keys,
authorization material, and provider secrets remain governed by the canonical
secret boundary and must not be persisted merely because the runtime directory
is external.



Legacy Data and Migration



Every existing file under `data/`, tracked exports, logs, snapshots, backups,
profile state, configuration, and currently modified runtime JSON remains
preserved. These artifacts are legacy migration inputs, not active automatic
migration targets.



No deletion, movement, rewrite, reset, untracking, or automatic ingestion is
authorized by this decision. Future migration must be opt-in, copy-based,
dry-run capable, checksummed, schema-aware, idempotent, crash-safe, reversible,
and explicitly approved for sensitive user data.



Test Contract



FORTRESS-02 implementation must establish function-scoped disposable runtime
roots, worker isolation, practical external pytest cache and bytecode placement,
no repository writes during test import or collection, and clean-tree-before
and clean-tree-after certification checks. The 428 excluded pytest-named files
are not reclassified by this decision.



Alternatives Considered



- Repository-local runtime roots were rejected because production and tests
  must not pollute or expose state through the working tree.
- Independent subsystem resolution was rejected because it would create
  duplicate path authorities and inconsistent safety checks.
- Operating-system usernames as profile identifiers were rejected because they
  couple the persistent contract to host identity and portability concerns.
- `platformdirs` was deferred because the approved initial defaults can be
  implemented with the standard library; it may be reconsidered with evidence.



Consequences



- `jaos_platform` becomes the single path-resolution authority.
- Production composition, runtime writers, logging, persistence, and tests will
  require later, separately authorized implementation changes.
- Existing legacy data remains untouched until an approved migration workflow
  exists.
- The first implementation slice has a fixed ownership, precedence, layout,
  profile, containment, secrets, migration, and test contract.
- This decision does not begin FORTRESS-03, canonical runtime composition
  changes, legacy deletion, Git untracking, data migration, or Phase 8
  expansion.



Validation Required During Implementation



- Unit tests for precedence, OS defaults, validation, absolute overrides, and
  repository containment.
- Function-scoped and worker-isolated path tests.
- Junction, symlink, traversal, drive, UNC, and separator rejection tests.
- Clean-tree-before and clean-tree-after certification evidence.
- Migration tests only under separate migration authorization.



Approved By



Founder Vinay B — 2026-08-21



\---



\# ADR-0011



Title



FORTRESS-05 Canonical Composition Carve-Out and Authority Contract



Status



Accepted — Founder-approved 2026-08-24



Context



FORTRESS-05 must establish one canonical production composition graph without
starting the paused MS-0025X Intelligence Manager milestone. The already
completed MS-0025A-D Conversation Intelligence foundation is sufficiently
mature to be composed, initialized, lifecycle-owned, and readiness-tested as a
narrow Fortress carve-out. It is not yet authorized as a production request
route.



Decision



The canonical authority graph is:



```text
PlatformRuntime
  -> PlatformComposition
     -> ToolManager
     -> AIManager
     -> ExecutiveController
     -> MemoryStore
     -> ConversationOrchestrator
```



`PlatformRuntime` and `PlatformComposition` own the graph. The five registered
service authorities are:



| Authority | Runtime service name | Registry owner |
|---|---|---|
| ToolManager | `tool_manager_platform` | Platform |
| AIManager | `ai_manager_platform` | Platform |
| ExecutiveController | `executive_controller_platform` | Platform |
| MemoryStore | `memory_store_platform` | Platform |
| ConversationOrchestrator | `intelligence_orchestrator_platform` | Intelligence |



The Conversation bootstrap policy is exactly:



```python
ConversationPolicy(policy_name="default")
```



All other dataclass defaults remain unchanged: `context_policy="default"`,
`max_history_turns=100`, `reference_window_turns=20`, reference resolution,
interruption, continuation, required context bundles, and working memory are
enabled; memory-candidate submission is disabled; provider responses are
limited to 50,000 characters and 100 metadata items; metadata is empty.



The only bootstrap prompt template is `conversation@1.0`. Both identifiers are
explicitly pinned on `ConversationOrchestrator`. Its exact approved content is:



```python
system_instruction = (
    "You are the conversational intelligence component of JAOS. "
    "Respond using the supplied conversation context, policy, and resolved "
    "references. Do not claim that tools, actions, approvals, or external "
    "operations occurred unless their results are explicitly provided."
)
task_instruction = (
    "Produce a helpful response to the user's current message. "
    "Preserve conversational continuity and respect the supplied context and "
    "policy."
)
```



Scope Boundary



FORTRESS-05 may compose, initialize, lifecycle-own, and health/readiness-test
the completed MS-0025A-D Conversation Intelligence components. It does not
route production CLI requests through `ConversationOrchestrator`; expand an
Intelligence manager or facade; add planning, reasoning, decision, autonomy,
agents, multi-agent behavior, execution proposals, or advanced Phase 8
capabilities; or integrate `MemoryContextSource`.



MS-0025X remains paused until the Fortress gate and a later governing decision
permit it. `MemoryStore` is canonical and lifecycle-owned but is not used by
live CLI behavior. `ConversationOrchestrator` is canonical and lifecycle-owned
but has no live production request consumer.



Compatibility and Deferred Ownership



`CommandDispatcher` and `JAOSShell` retain compatibility-only self-construction
fallbacks. The canonical `run_jaos.py` path must inject Tool, AI, and Executive
and must never reach those fallbacks. Their removal or quarantine belongs to
FORTRESS-06, together with legacy/shadow-stack quarantine.



The lazy `jaos.intelligence` package facades are interim import containment.
They compatibility-preserve public exports and the `context`, `exceptions`,
`interfaces`, `models`, and `prompt` submodule attributes without eager
deferred-capability loading. Their packaging debt belongs to FORTRESS-06.



No `SQLiteStore` to `MemorySearchEngine` adapter is authorized.
`MemoryContextSource` integration remains deferred.



Finding Disposition



- RAA-002 is PARTIALLY RESOLVED: composition and lifecycle ownership are
  resolved; production request-path routing remains deferred to the
  post-Fortress/MS-0025X owner unless later governance assigns it elsewhere.
- RAA-007 is PARTIALLY RESOLVED: canonical production composition ownership is
  resolved; `CommandDispatcher`/`JAOSShell` self-construction compatibility
  remains FORTRESS-06 debt.
- RAA-009 remains OPEN — DEFERRED: the Memory-context coupling is unchanged.



Authorization Trail



- FORTRESS-05A/05B — Tool, AI, and Executive composition; committed checkpoint
  `f9b054e`.
- FORTRESS-05C — canonical Memory composition; committed checkpoint `1df73e3`.
- FORTRESS-05D — narrow Conversation Intelligence composition; committed
  checkpoint `cf26693`.
- FORTRESS-05E — uncommitted invariant and closure candidate authorized before
  this decision was recorded.
- FORTRESS-05 closure remediation — Founder-authorized 2026-08-24 to correct
  lifecycle, failure, readiness, import, governance, and evidence gaps found by
  independent review.



Consequences



- AI initialization and registration must be rollback-scoped so no initialized
  provider survives a failed registration.
- `MemoryStore` owns a provider-neutral `close()`/`is_closed` lifecycle
  contract.
- A composition-owned Memory, AI, or Intelligence lifecycle failure must retain
  its reachable service registration, ownership name, and required lifecycle
  references for deterministic retry. Independent safe cleanup continues and
  all teardown errors are aggregated; a successful retry releases the retained
  service and references.
- Functional closure evidence must include a real composed mock-backed
  Conversation turn and a real Memory create/get round trip under disposable
  `RuntimePaths.memory`.
- FORTRESS-05 cannot be marked COMPLETE AND VERIFIED until its focused,
  affected-subsystem, and full configured verification ladder passes.
- This decision does not certify the Fortress Program, complete Step 7, start
  Step 8, resume Phase 8, or begin FORTRESS-06.



Approved By



Founder Vinay B — 2026-08-24



\---



\# Review Policy



New ADRs are added only for decisions that affect long-term architecture.



Existing accepted ADRs should not be modified without founder approval.

