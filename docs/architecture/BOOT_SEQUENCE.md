# JAOS Boot Sequence

## Version

Architecture Freeze v1.0

Status: Draft (broader conceptual boot flow); canonical Runtime Platform
sequence below is IMPLEMENTED AND VERIFIED under FORTRESS-03.

---

# Purpose

This document defines the startup sequence of JAOS.

Every startup follows this order.

---

# Canonical Runtime Platform Boot Sequence (FORTRESS-03, Verified)

This is the actual, tested boot sequence executed by
`jaos_platform.BootManager.boot()` against a `jaos_platform.PlatformRuntime`
instance. It is the canonical Runtime Platform boot authority. It does not
yet run on the production `run_jaos.py` launcher path — that composition is
FORTRESS-04's scope — but is fully implemented and verified in isolation.

```text
PlatformRuntime() construction
    (RuntimePaths resolved; no service registered; lifecycle_state = CREATED)
    ↓
BootManager.boot() called; steps reset to []
    ↓
runtime.initialize()
    CREATED -> INITIALIZING -> INITIALIZED
    ↓
runtime.start()
    INITIALIZED -> STARTING
    register service_container, service_registry, runtime_context, event_bus
    (any registration failure: unwind in reverse, STARTING -> ROLLING_BACK -> FAILED, re-raise)
    STARTING -> READY
    ↓
RuntimeValidator.validate()      -> runtime_report
StartupValidator.validate()      -> startup_report
DependencyValidator.validate()   -> dependency_report
RuntimeHealthCertifier.certify() -> health_report
    ↓
required_ready = runtime_report.healthy
                  and startup_report.ready
                  and dependency_report.valid
    ↓
required_ready == True                  required_ready == False
    ↓                                        ↓
boot_status = READY                     runtime.mark_failed()
RuntimeContext holds all four reports   READY -> FAILED
boot() returns True                     boot_status = FAILED
                                         boot() returns False
```

Every report is computed from the real, just-registered platform services
and the real `lifecycle_state` — none of them is assigned unconditionally.
Calling `boot()` again after `READY` or `FAILED` raises
`LifecycleTransitionError` at the first `runtime.initialize()` call, before
any container or registry mutation.

## Shutdown

`BootManager.shutdown()` calls `runtime.stop()` only when `STOPPING` is a
legal transition from the current state. `runtime.stop()` tears down every
owned service in reverse registration order, continues past individual
teardown failures, and aggregates them into one `PartialShutdownError` if any
occurred, leaving the runtime truthfully `FAILED` rather than `STOPPED`.
`BootManager` then clears the boot-time reports from `RuntimeContext`,
publishes the shutdown notification, and releases `EventBus` subscriptions.

See `docs/architecture/RUNTIME_LIFECYCLE.md` for the full canonical state
table and health contract.

---

# Extended / Future Boot Flow

The remainder of this document describes a broader conceptual boot sequence
for later JAOS phases (plugin ecosystem, multi-interface startup, security
subsystem). It is not yet implemented and is not superseded by the canonical
section above except where they directly conflict on the Runtime Platform
layer.

# Boot Flow

```text
Power On
    ↓
Operating System
    ↓
JAOS Launcher
    ↓
Kernel Initialization
    ↓
Core Runtime Initialization
    ↓
Configuration Loading
    ↓
Security Initialization
    ↓
Provider Discovery
    ↓
Plugin Discovery
    ↓
Memory Initialization
    ↓
Executive Brain Initialization
    ↓
Domain Services Startup
    ↓
Interface Startup
    ↓
Health Validation
    ↓
Ready
```

---

# Phase 1 — Kernel

Responsibilities:

- Initialize runtime
- Register core services
- Start event bus
- Create runtime context

---

# Phase 2 — Core Runtime

Initialize:

- Event System
- Scheduler
- Recovery Manager
- Snapshot Manager
- Config Manager
- Health Monitor
- Plugin Manager

---

# Phase 3 — Configuration

Load:

- System settings
- AI configuration
- Provider configuration
- User configuration

Validate integrity before continuing.

---

# Phase 4 — Security

Initialize:

- Authentication
- Authorization
- Permission Manager
- Audit Logger
- Security Monitor

---

# Phase 5 — Provider Discovery

Discover:

- Local providers
- Cloud providers
- Health status
- Capabilities

Build Provider Registry.

---

# Phase 6 — Plugin Discovery

Locate plugins.

Validate:

- Compatibility
- Signatures (future)
- Permissions
- Dependencies

Register valid plugins.

---

# Phase 7 — Memory

Initialize:

- Working memory
- Conversation memory
- Long-term memory
- Knowledge Base

Verify persistence.

---

# Phase 8 — Executive Brain

Initialize:

- Planner
- Reasoner
- Provider Router
- Tool Manager
- Agent Coordinator
- Reflection Engine

---

# Phase 9 — Domain Services

Start:

- Workflow
- Communication
- PC Control
- Infrastructure
- Dashboard support
- Development services

---

# Phase 10 — Interfaces

Start:

- Dashboard
- API
- Voice (future)
- Vision (future)
- Mobile (future)

---

# Phase 11 — Health Validation

Verify:

- Required services
- Provider availability
- Memory health
- Plugin health
- Configuration consistency

---

# Recovery

If any required stage fails:

1. Retry initialization.
2. Recover from checkpoint if available.
3. Disable optional components if necessary.
4. Enter Safe Mode if startup cannot complete safely.

---

# Startup Principles

- Deterministic
- Recoverable
- Observable
- Secure
- Extensible

---

# Principle

JAOS should always start in a known, validated, and recoverable state.
