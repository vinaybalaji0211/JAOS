\# JAOS Memory Platform Requirements



Version: 1.1



Status: ACTIVE



Phase: Phase 7 — Memory Platform



Release Target: v0.9.0-alpha



Owner: Vinay B



Maintainer: JAOS Engineering



\---



\# 1. Purpose



This document defines the approved requirements for the JAOS Memory Platform.



The Memory Platform provides persistent, structured, retrievable, ranked, lifecycle-managed memory for JAOS while preserving existing platform boundaries and public APIs.



This document governs Phase 7 implementation.



Implementation must not begin until these requirements and the corresponding architecture design are accepted.



\---



\# 2. Phase Objective



Phase 7 will introduce a production-oriented Memory Platform that allows JAOS to:



\* Maintain active working context.

\* Preserve recent conversational and operational context.

\* Store durable long-term memories.

\* represent events as episodic memories.

\* Represent reusable facts and concepts as semantic memories.

\* Retrieve relevant memories.

\* Rank retrieved memories.

\* Manage memory lifecycle and retention.

\* Supply relevant memory to the AI prompting pipeline.

\* Associate memories with identities and scopes.

\* Support future vector database integration without requiring it in Phase 7.



\---



\# 3. Approved Platform Boundary



The canonical Memory Platform location is:



```text

jaos/memory/

```



The Memory Platform owns:



\* Memory domain models.

\* Memory storage interfaces.

\* Memory repositories.

\* Short-term memory.

\* Long-term memory.

\* Episodic memory.

\* Semantic memory.

\* Memory retrieval.

\* Memory ranking.

\* Memory lifecycle management.

\* Memory diagnostics.

\* Memory telemetry.

\* Memory platform composition.



The Executive Platform may consume the Memory Platform but must not own persistent memory infrastructure.



The AI Platform may retrieve memory through an approved Memory Platform interface but must not directly access storage implementations.



The Provider Platform must remain unaware of memory storage.



The Tool Platform must not directly mutate memory storage unless routed through a public Memory Platform service.



\---



\# 4. Existing API Compatibility



Founder clarification — ADR-0013 (2026-08-31): the former exact compatibility
requirement for these Executive Memory implementations is superseded:



```text

executive\_brain.memory.working\_memory.WorkingMemory

executive\_brain.memory.memory\_registry.MemoryRegistry

executive\_brain.memory.memory\_manager.MemoryManager

```



These exact `executive_brain.memory` implementations are historical shadow
architecture, not permanent canonical runtime authorities. ADR-0013 is the
documented and approved intentional compatibility change.



The logical responsibilities previously represented by the Executive
`MemoryManager` remain preserved:



\* Current user request.

\* Current mission identifier.

\* Current execution plan identifier.

\* Current decision identifier.

\* Current result identifier.

\* Active execution context.

\* Clear/reset behavior where required by a future approved owner.

\* Observability, health, readiness, and degradation responsibility.



Persistent Memory remains owned by canonical `MemoryStore`/`SQLiteStore`.



Active request and transient session/context state require a future approved
Context Platform or task-session-context owner. Mission, plan, decision, and
result references require explicit canonical owners when Phase 8 resumes;
durable forms belong to FORTRESS-08 where applicable. Working-memory health,
readiness, and degradation belong to FORTRESS-10. Experience Memory remains a
separate future Experience Memory Platform responsibility.



Future owners must deliberately define their contracts through approved
governance before implementation. This clarification creates no replacement
`WorkingMemory`, `MemoryManager`, or `MemoryRegistry` runtime authority and does
not authorize legacy self-registration or composition behavior.



\---



\# 5. Legacy Memory Components



The repository currently contains prototype memory components under:



```text

memory/

```



These files are not the canonical Phase 7 platform boundary.



Phase 7 must:



\* Audit the prototype functionality.

\* Reuse valid concepts where appropriate.

\* Avoid creating new dependencies on the root-level prototype package.

\* Avoid deleting legacy components until compatibility and dependency audits are complete.

\* Record any planned deprecation in the Technical Debt register.

\* Migrate behavior only through complete-file implementations in the canonical platform.



\---



\# 6. Functional Requirements



\## 6.1 Memory Records



Every persistent memory must have a structured representation.



A memory record must support:



\* Unique memory identifier.

\* Memory type.

\* Content.

\* Creation timestamp.

\* Last update timestamp.

\* Source.

\* Scope.

\* Identity association.

\* Importance score.

\* Confidence score.

\* Access count.

\* Last accessed timestamp.

\* Lifecycle state.

\* Metadata.



Memory identifiers must be stable and unique.



Memory records must be serializable.



Memory records must not depend on a specific database implementation.



\---



\## 6.2 Working Memory



Working Memory represents the active state required for current execution.



It must support:



\* Active user request.

\* Current mission.

\* Current execution plan.

\* Current decision.

\* Current result.

\* Active context.

\* Explicit clearing.

\* Serialization.

\* Runtime health reporting.



These are preserved logical responsibilities, not a requirement to retain the
exact `executive_brain.memory.WorkingMemory` API or implementation. ADR-0013
supersedes that exact API-stability requirement.



Persistent Memory remains distinct from future transient-context ownership. No
replacement Working Memory platform, bridge, or runtime authority is authorized
by this clarification.



\---



\## 6.3 Short-Term Memory



Short-Term Memory represents recent information that may be useful during the current session or a limited time window.



It must support:



\* Bounded capacity.

\* Ordered insertion.

\* Recent-memory retrieval.

\* Explicit removal.

\* Explicit clearing.

\* Expiration.

\* Promotion candidates for long-term storage.

\* Memory type and scope filtering.



Short-Term Memory must not automatically create permanent memories without an approved lifecycle decision.



\---



\## 6.4 Long-Term Memory



Long-Term Memory represents durable information retained across sessions.



It must support:



\* Persistent storage.

\* Retrieval by identifier.

\* Query-based retrieval.

\* Update.

\* Lifecycle state changes.

\* Soft deletion or archival.

\* Identity and scope filtering.

\* Importance and confidence metadata.

\* Storage implementation independence.



Long-Term Memory must survive JAOS process restarts.



\---



\## 6.5 Episodic Memory



Episodic Memory represents events or experiences that occurred at a particular time.



It must support:



\* Event description.

\* Event timestamp.

\* Participants or identities.

\* Related mission or task.

\* Outcome.

\* Context.

\* Source.

\* Importance.

\* Confidence.

\* Relationships to other memories.



Examples include:



\* A completed user request.

\* A failed execution.

\* A provider outage.

\* A successful workflow.

\* A user correction.

\* A system recovery event.



\---



\## 6.6 Semantic Memory



Semantic Memory represents reusable facts, concepts, preferences, and learned knowledge.



It must support:



\* Subject.

\* Predicate or relationship.

\* Value or object.

\* Confidence.

\* Source.

\* Identity scope.

\* Version or update history.

\* Conflict detection metadata.



Examples include:



\* User preferences.

\* JAOS architectural facts.

\* Known environment properties.

\* Stable project information.

\* Reusable learned facts.



Phase 7 does not require a complete knowledge graph.



The model must remain compatible with future graph-based storage.



\---



\## 6.7 Memory Retrieval



The Memory Platform must provide a single retrieval service.



Retrieval must support:



\* Text queries.

\* Memory type filtering.

\* Identity filtering.

\* Scope filtering.

\* Time filtering.

\* Importance thresholds.

\* Confidence thresholds.

\* Lifecycle state filtering.

\* Maximum result limits.



The initial implementation may use deterministic lexical matching.



Retrieval interfaces must support future semantic or vector search implementations.



\---



\## 6.8 Memory Ranking



Retrieved memories must be rankable.



The initial ranking model must be deterministic and testable.



Ranking may consider:



\* Query relevance.

\* Importance.

\* Confidence.

\* Recency.

\* Access frequency.

\* Memory type.

\* Identity match.

\* Scope match.



Ranking calculations must be isolated behind a ranking interface.



Provider-specific ranking must not be introduced into the Memory Platform core.



\---



\## 6.9 Memory Lifecycle



The Memory Platform must define explicit lifecycle states.



Required states:



```text

ACTIVE

ARCHIVED

EXPIRED

DELETED

```



The lifecycle service must support:



\* Creation.

\* Activation.

\* Archival.

\* Expiration.

\* Soft deletion.

\* Retention evaluation.

\* Short-term to long-term promotion.

\* Access metadata updates.



Destructive deletion must not be the default behavior.



Lifecycle operations must be testable and auditable.



\---



\## 6.10 Memory-Backed Prompting



The AI Platform must be able to request relevant memory for a prompt.



Integration must occur through an explicit interface or prompt contributor.



The memory prompting component must:



\* Receive the current prompt context.

\* Retrieve relevant memories.

\* Apply identity and scope restrictions.

\* Rank memories.

\* Enforce a configurable result limit.

\* Format memories for prompt composition.

\* Avoid exposing storage implementation details.

\* Return no memory content when no relevant memory is available.



The Prompt Platform must remain responsible for final prompt composition.



The Memory Platform must not call AI providers directly.



\---



\## 6.11 Identity-Aware Memory



Memory must support identity association.



At minimum, a memory may be associated with:



\* System identity.

\* User identity.

\* Session identity.

\* Mission identity.

\* Global scope.



Identity filtering must occur before memory is supplied to another platform.



The design must avoid accidental cross-user memory exposure.



Phase 7 may use simple identity identifiers while preserving compatibility with future identity expansion.



\---



\## 6.12 Memory Safety



The Memory Platform must support safety controls.



It must provide extension points for:



\* Sensitive-data detection.

\* Secret rejection.

\* Restricted-memory categories.

\* Retention restrictions.

\* Identity access rules.

\* Memory redaction.

\* Audit events.



Plaintext credentials, authentication tokens, one-time passwords, and financial secrets must not be intentionally stored as normal memory records.



Secret storage remains the responsibility of the Secret Manager.



\---



\## 6.13 Memory Events



The Memory Platform should publish runtime events for significant operations.



Candidate events include:



```text

memory\_created

memory\_updated

memory\_accessed

memory\_archived

memory\_expired

memory\_deleted

memory\_promoted

memory\_retrieved

memory\_retrieval\_failed

```



Event payloads must avoid leaking sensitive memory content unnecessarily.



Events must use the existing Runtime Event Bus.



The Memory Platform must not introduce a second event system.



\---



\## 6.14 Diagnostics and Health



The Memory Platform must expose health information.



Health reporting should include:



\* Platform status.

\* Storage availability.

\* Repository availability.

\* Record count where practical.

\* Retrieval service status.

\* Lifecycle service status.

\* Last failure information where appropriate.



Diagnostics must not expose secret or sensitive memory content.



\---



\## 6.15 Telemetry



The Memory Platform should provide internal telemetry for:



\* Memories created.

\* Memories retrieved.

\* Retrieval misses.

\* Memories archived.

\* Memories expired.

\* Memories promoted.

\* Storage failures.

\* Retrieval latency where practical.



Telemetry must remain implementation-independent.



External observability systems are not required in Phase 7.



\---



\# 7. Storage Requirements



Phase 7 must introduce a storage abstraction.



The storage abstraction must support:



\* Save.

\* Retrieve by identifier.

\* Update.

\* Query.

\* List.

\* Archive.

\* Soft delete.

\* Health check.



The first persistent storage implementation should be local and deterministic.



A JSON-based or similarly lightweight local implementation is acceptable for Phase 7 if:



\* Writes are safe.

\* Corrupted storage is handled predictably.

\* Storage directories are created safely.

\* Serialization is explicit.

\* Tests use isolated temporary storage.

\* Production data is not written during unit tests.



Direct file access must remain inside the storage implementation.



Memory services must depend on storage interfaces, not file paths.



\---



\# 8. Future Vector Database Compatibility



A vector database is not required for the Phase 7 release.



The architecture must allow a future vector repository to implement the approved retrieval or storage interfaces.



Phase 7 must not:



\* Hard-code a vector database vendor.

\* Require embeddings for basic operation.

\* Couple Memory Platform models to provider-specific embedding formats.

\* Require network access for memory retrieval.

\* Make vector search the only supported retrieval method.



The initial deterministic implementation must remain usable when no vector provider exists.



\---



\# 9. Platform Composition



The Memory Platform must provide a composition root or facade responsible for assembling:



\* Memory repositories.

\* Storage implementation.

\* Retrieval service.

\* Ranking service.

\* Lifecycle service.

\* Memory manager or facade.

\* Diagnostics.

\* Telemetry.



Composition must not occur through hidden global state.



Runtime integration must use the existing JAOS Platform Runtime and service container patterns.



The Memory Platform must expose a stable public facade for consumers.



\---



\# 10. Dependency Direction



Approved dependency direction:



```text

Executive Platform

&#x20;       ↓

Memory Platform public interfaces

&#x20;       ↓

Memory services

&#x20;       ↓

Memory repositories

&#x20;       ↓

Memory storage abstractions

&#x20;       ↓

Local storage implementation

&#x20;       ↓

Runtime Foundation

```



AI Prompt Platform integration:



```text

Prompt Platform

&#x20;       ↓

Memory prompt contributor or gateway

&#x20;       ↓

Memory retrieval facade

```



Prohibited dependency direction:



```text

Memory Platform → Executive Platform internals

Memory Platform → AI provider implementations

Memory Platform → Tool implementations

Storage implementation → Executive Platform

Provider Platform → Memory storage

```



Domain models should have minimal infrastructure dependencies.



\---



\# 11. Public API Requirements



Phase 7 must define a deliberate public API.



Candidate public components include:



```text

MemoryPlatform

MemoryManager

MemoryRecord

MemoryType

MemoryScope

MemoryLifecycleState

MemoryQuery

MemoryResult

MemoryRepository

MemoryRetriever

MemoryRanker

MemoryLifecycleManager

```



Final public names will be approved during architecture design.



Internal storage details must not be exported as general public APIs.



Public APIs must use type hints and predictable exceptions.



Public API changes must be recorded in Architecture Decisions and the changelog.



\---



\# 12. Error Handling Requirements



The Memory Platform must use explicit exceptions for expected failure conditions.



Required error categories should include:



\* Invalid memory data.

\* Memory not found.

\* Storage unavailable.

\* Storage corruption.

\* Unsupported query.

\* Unsafe memory.

\* Invalid lifecycle transition.

\* Identity access violation.



Broad exception swallowing is prohibited.



Storage corruption must not silently return an empty memory collection as though no data existed.



Runtime failures must be logged through the approved JAOS logging platform.



\---



\# 13. Testing Requirements



Phase 7 must include:



\* Unit tests for every memory domain model.

\* Unit tests for storage abstractions.

\* Unit tests for the local storage implementation.

\* Unit tests for retrieval.

\* Unit tests for ranking.

\* Unit tests for lifecycle transitions.

\* Unit tests for identity filtering.

\* Unit tests for memory-backed prompting.

\* Integration tests with Platform Runtime.

\* Integration tests with the Prompt Platform.

\* Integration tests with the Executive Platform where required.

\* Restart persistence tests.

\* Corrupted-storage behavior tests.

\* Regression evidence for preserved logical responsibilities against their
approved canonical owners; ADR-0013 removes the mandate to preserve the exact
legacy Executive Working Memory APIs.



Tests must not depend on production memory files.



Temporary directories or injected storage paths must be used.



All existing repository tests must continue passing.



\---



\# 14. Runtime Verification Requirements



Runtime verification must demonstrate:



\* JAOS boots with the Memory Platform enabled.

\* Memory Platform registers with Platform Runtime.

\* Memory health is available.

\* A memory can be created.

\* A memory survives a restart.

\* A memory can be retrieved.

\* Results are ranked deterministically.

\* Identity filtering is enforced.

\* Lifecycle transitions work.

\* Relevant memory can contribute to an AI prompt.

\* JAOS shuts down cleanly.



Runtime commands will be finalized during integration design.



\---



\# 15. Non-Functional Requirements



The Memory Platform must be:



\* Deterministic where practical.

\* Modular.

\* Testable.

\* Storage-independent.

\* Provider-independent.

\* Backward compatible.

\* Safe by default.

\* Observable.

\* Resumable.

\* Suitable for future scale expansion.



Initial local operations should not require network access.



Memory retrieval should remain bounded by configurable limits.



\---



\# 16. Explicit Non-Goals



Phase 7 does not include:



\* A production cloud database.

\* A mandatory vector database.

\* Autonomous unrestricted memory creation.

\* Autonomous deletion of permanent memory.

\* Full knowledge graph implementation.

\* Cross-device memory synchronization.

\* Cloud memory synchronization.

\* Distributed memory consensus.

\* Multi-user account management.

\* Biometric identity recognition.

\* Provider-managed memory.

\* Self-modifying memory schemas.

\* Phase 8 planning functionality.



These capabilities may be introduced in future phases through approved architecture changes.



\---



\# 17. Documentation Requirements



Phase 7 documentation must include:



\* Memory Platform requirements.

\* Memory Platform architecture.

\* Public API documentation.

\* Dependency direction.

\* Storage design.

\* Retrieval and ranking design.

\* Lifecycle design.

\* Prompt integration design.

\* Architecture decisions.

\* Technical debt.

\* Architecture watchlist.

\* Runtime certification.

\* Stabilization audit.

\* Release checklist.

\* Project state updates.

\* Continuation context updates.



Documentation must be synchronized before release.



\---



\# 18. Stabilization Sprint Requirements



Phase 7 must conclude with the complete JAOS Stabilization Sprint.



Required certifications:



1\. Architecture Audit

2\. Code Quality Audit

3\. Dependency Audit

4\. Test and Coverage Audit

5\. Runtime Certification



The phase must not enter the Documentation and Release Sprint until all five certifications pass.



\---



\# 19. Release Criteria



Phase 7 is complete only when:



\* Requirements are approved.

\* Architecture is approved.

\* Implementation is complete.

\* Unit tests pass.

\* Integration tests pass.

\* Full regression suite passes.

\* Runtime verification passes.

\* Existing public APIs remain compatible or approved changes are documented.

\* Stabilization Sprint passes.

\* Documentation is synchronized.

\* Git status is clean.

\* Release commit is created.

\* Release tag is created.

\* Release is pushed.



Planned release target:



```text

v0.9.0-alpha

```



\---



\# 20. Requirements Status



```text

Phase 7 Requirements: DEFINED

Architecture Design: PENDING

Implementation: NOT STARTED

Testing: NOT STARTED

Runtime Verification: NOT STARTED

Stabilization Sprint: NOT STARTED

Documentation Sprint: NOT STARTED

Release: NOT STARTED

```



\---



\# 21. Next Engineering Action



Create the Phase 7 Memory Platform architecture design.



The architecture design must define:



\* Canonical package structure.

\* Domain models.

\* Public facade.

\* Repository interfaces.

\* Storage interfaces.

\* Retrieval pipeline.

\* Ranking pipeline.

\* Lifecycle transitions.

\* Runtime registration.

\* Executive integration.

\* Prompt Platform integration.

\* Migration treatment for legacy memory components.



