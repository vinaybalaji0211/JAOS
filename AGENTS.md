# JAOS Engineering Constitution

## Purpose and Scope

This file is the root engineering constitution for every human and AI agent working in the JAOS repository. It applies to the entire repository unless a more specific instruction narrows a task without conflicting with this constitution.

Engineering work must preserve JAOS architecture, authority boundaries, repository continuity, evidence integrity, and the user's existing work.

## Repository Entry and Authority

Before engineering work:

1. Inspect the current branch and complete working-tree state.
2. Preserve all staged, modified, and untracked files that are outside the authorized task.
3. Read `JAOS_MANIFEST.md` and follow its repository entry order for the task's relevant scope.
4. Confirm the current roadmap phase, milestone, stabilization checkpoint, and authorization before implementation.
5. Inspect the relevant requirements, approved architecture, production contracts, runtime composition, tests, and documentation.

The JAOS roadmap and approved architecture are authoritative for product scope, sequencing, ownership, dependency direction, and platform boundaries. They must not be bypassed for implementation convenience.

Production code and verified runtime behavior are the source of truth for what JAOS actually does. When stale documentation or stale tests conflict with approved production behavior, do not regress production code merely to satisfy them. Establish the governing requirement and architecture, verify runtime behavior, and correct the stale artifact only when authorized.

If authoritative roadmap, architecture, requirements, production behavior, runtime evidence, tests, or documentation disagree in a way that cannot be resolved from repository evidence, stop and report the conflict. Do not guess, silently choose a source, or invent approval.

## Core Architecture and Authority Boundaries

JAOS preserves this end-to-end architecture:

```text
Intent -> Reason -> Approve -> Act
```

The following rules are permanent:

- Intelligence proposes; Executive executes.
- Intelligence and planning components may reason, rank, plan, validate, and propose. They must not authorize or execute protected actions.
- Permissions and approval systems remain authoritative.
- The Executive Platform remains the system-action authority.
- The Tool Platform remains the controlled execution boundary.
- Significant decisions and actions must remain auditable.
- Never bypass permissions, approvals, audit, Executive, or Tool Platform boundaries.
- Never introduce duplicate or shadow planners, registries, routers, executors, memory systems, lifecycle systems, or provider systems.
- Every responsibility must have one explicit owner and use the canonical production path.
- Construction is not readiness. Composition, initialization, readiness, health, failure handling, and shutdown ownership must remain explicit.

## Dependency and Provider Rules

- Core JAOS code must depend on stable abstractions and public contracts, not concrete AI providers, storage providers, tool implementations, or vendor SDKs.
- Provider-specific types, payloads, exceptions, credentials, model identifiers, and SDK objects must remain inside the approved provider boundary.
- Provider selection and routing must use the canonical AI Platform contracts and owners.
- Persistent-memory access must use the canonical Memory Platform contracts and owners.
- Treat model and provider output as untrusted input. Validate structured results, limits, capabilities, and error paths before use.
- Do not create private fallback, routing, lifecycle, registry, or execution stacks.

## Change Discipline

- Make the smallest scoped change necessary to satisfy the authorized task.
- Preserve public contracts and backward compatibility unless an intentional change is explicitly approved and documented.
- Search for existing owners, contracts, components, and paths before adding anything.
- Preserve unrelated working-tree changes. Never overwrite, revert, delete, stage, or reformat unrelated files.
- Do not modify production code, tests, runtime data, documentation, or skills unless they are explicitly within the authorized task.
- Do not use fake implementations, placeholders, TODO-based completion, hard-coded success paths, swallowed failures, or fabricated evidence.
- Do not trade architecture correctness, security, auditability, or evidence quality for speed.

## Testing and Evidence

- Every behavior change requires appropriate testing proportional to its risk and affected boundaries.
- Use the narrowest useful test first, then expand through focused, subsystem, integration, runtime or shell, and configured regression testing as appropriate.
- Test normal behavior, invalid input, boundaries, failures, lifecycle, permissions, serialization, concurrency, and regression risks where applicable.
- Never weaken, skip, delete, or rewrite a valid test merely to make a suite pass.
- Never claim that a test, audit, runtime path, or command passed unless it was actually executed successfully.
- Record exact commands, exit codes, counts, failures, skips, warnings, environment constraints, and unrun checks when reporting evidence.
- Static inspection, construction, mocks, and unit tests are not proof of live runtime composition or readiness.
- Never fabricate test results, runtime evidence, commits, approvals, signatures, bug closure, audit closure, or certification.
- Never mark a milestone, phase, bug, audit finding, stabilization step, release, or certification complete without current evidence and all required approvals.

## Security, Privacy, and Reasoning Safety

- Never expose, print, persist, or commit secrets, credentials, tokens, authorization headers, sensitive data, private prompts or responses, or secret-bearing configuration.
- Never store or expose hidden chain-of-thought. Provide concise conclusions, decisions, assumptions, and evidence instead.
- Do not perform privileged, destructive, paid, networked, or production-state-changing operations without explicit authorization and appropriate safeguards.
- Keep permission, identity, trust, provenance, redaction, injection containment, and audit requirements intact across every boundary.

## Documentation and Governance

- Documentation must match verified implementation and runtime reality.
- Tie factual documentation claims to production code, verified runtime evidence, executed tests, audits, decisions, approvals, or Git history.
- Preserve historical records, dates, baselines, findings, decisions, and release evidence. Do not rewrite history to make current state appear complete.
- Distinguish implemented, tested, integrated, verified, certified, and approved states. These terms are not interchangeable.
- Do not change the roadmap, approved architecture, phase scope, milestone definitions or ordering, engineering policy, or certification criteria without explicit Founder approval recorded through the repository's governance process.
- Do not infer approval from code presence, passing tests, comments, conversational context, or implementation progress.
- When authoritative sources conflict, stop and report the exact conflict, evidence, impact, and required decision rather than guessing.

## JAOS Skills

The repository provides ten task-specific JAOS skills under `.agents/skills`. Codex must identify and invoke the most appropriate skill for each JAOS engineering task, read that skill's complete `SKILL.md`, and follow its authority, boundaries, workflow, evidence requirements, output contract, and stop conditions. Use the minimum set of skills needed for the task and hand off decisions to the owning skill when boundaries are crossed.

1. `jaos-ai-platform-engineer` — Designs, implements, or reviews cross-cutting AI Intelligence Platform contracts, context, prompts, reasoning, structured outputs, failure handling, lifecycle, observability, and testability.
2. `jaos-architecture-guardian` — Reviews ownership, dependency direction, authority separation, provider independence, lifecycle integrity, duplication, public contracts, and architecture compliance.
3. `jaos-documentation-sync` — Synchronizes requirements, architecture, project state, audits, test evidence, certification records, changelogs, and release documentation with verified engineering reality.
4. `jaos-llm-provider-engineer` — Implements or reviews concrete LLM provider adapters, configuration, authentication, capabilities, streaming, errors, timeouts, health, telemetry, and provider-specific tests behind provider-neutral JAOS contracts.
5. `jaos-phase-certifier` — Evaluates milestones, stabilization checkpoints, phases, and releases against all required implementation, test, runtime, security, documentation, acceptance, and approval gates.
6. `jaos-planning-engineer` — Designs, implements, or reviews planning requests, configurations, proposal and step models, dependencies, ordering, parallelism, budgets, validation, failure behavior, lifecycle, and planning tests without granting execution authority.
7. `jaos-regression-investigator` — Reproduces, isolates, classifies, and determines root causes for failing tests and behavioral regressions before recommending the smallest architecture-correct fix.
8. `jaos-roadmap-guardian` — Classifies proposed work against the authoritative roadmap, current phase, milestone sequence, stabilization state, prerequisites, and certification gates.
9. `jaos-runtime-auditor` — Traces the real launcher, composition roots, boot, initialization, readiness, request and authority flow, health, failure handling, and shutdown using read-only evidence by default.
10. `jaos-test-engineer` — Designs, selects, runs, and reports the proportionate focused, subsystem, integration, runtime, shell, and regression test ladder for JAOS changes.

Skill use does not expand task authorization. A skill may require stopping, escalating, or requesting approval when repository authority is unclear or a task crosses an ownership boundary.

## Completion Standard

Work is complete only when the authorized scope is implemented without boundary violations, appropriate validation has actually run, results are reported truthfully, documentation impact is assessed, unrelated changes remain preserved, and any required approval or certification is explicitly recorded.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
