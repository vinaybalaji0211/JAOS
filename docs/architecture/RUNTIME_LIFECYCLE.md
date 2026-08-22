# JAOS Runtime Lifecycle

## Version

Architecture Freeze v1.0

Status: Draft (broader conceptual lifecycle); canonical Runtime Platform
section below is IMPLEMENTED AND VERIFIED under FORTRESS-03.

---

# Purpose

This document defines the lifecycle of a running JAOS instance from startup
to shutdown.

---

# Canonical Runtime Lifecycle (FORTRESS-03, Verified)

This section documents the actual, implemented, and tested lifecycle owned by
`jaos_platform.PlatformRuntime` and `jaos_platform.BootManager`. It is the
single canonical lifecycle authority for the Runtime Platform. It supersedes
any conflicting lifecycle claim elsewhere in this document for the Runtime
Platform layer specifically; the broader conceptual lifecycle in the sections
below remains a separate, longer-term architectural vision for later phases
and is not superseded.

## States

`jaos_platform.lifecycle_state.RuntimeLifecycleState`:

```text
CREATED -> INITIALIZING -> INITIALIZED -> STARTING -> READY
                                              |          |
                                              v          v
                                         ROLLING_BACK  DEGRADED <-> READY
                                              |          |
                                              v          v
                                            FAILED    STOPPING -> STOPPED
```

The exact legal-transition table is `jaos_platform.lifecycle_transitions.LIFECYCLE_TRANSITIONS`:

| Current | Legal targets |
|---|---|
| CREATED | INITIALIZING |
| INITIALIZING | INITIALIZED, FAILED |
| INITIALIZED | STARTING, STOPPING |
| STARTING | READY, DEGRADED, ROLLING_BACK, FAILED |
| READY | DEGRADED, STOPPING, FAILED |
| DEGRADED | READY, STOPPING, FAILED |
| ROLLING_BACK | STOPPED, FAILED |
| STOPPING | STOPPED, FAILED |
| STOPPED | (terminal) |
| FAILED | (terminal) |

Any transition not in this table raises `LifecycleTransitionError`. STOPPED
and FAILED are true dead ends: no restart contract exists, so reaching either
requires constructing a new `PlatformRuntime` instance.

## Construction is not readiness

`PlatformRuntime()` only resolves `RuntimePaths` and constructs the four
owned platform services (`ServiceContainer`, `ServiceRegistry`,
`RuntimeContext`, `EventBus`) without registering or starting any of them.
`lifecycle_state` is `CREATED` and `RuntimeContext` holds no keys at all.

## Boot flow

`BootManager.boot()`:

1. `runtime.initialize()` — `CREATED -> INITIALIZING -> INITIALIZED`.
2. `runtime.start()` — `INITIALIZED -> STARTING`, registers the four owned
   platform services into `ServiceContainer`/`ServiceRegistry`. On any
   registration failure, every service registered by this attempt is
   unregistered in reverse order, the runtime transitions
   `STARTING -> ROLLING_BACK -> FAILED`, and the original exception is
   re-raised.
3. On successful start, `RuntimeValidator`, `StartupValidator`,
   `DependencyValidator`, and `RuntimeHealthCertifier` run against the real,
   now-registered services and their reports are written to
   `RuntimeContext`.
4. `boot()` returns `True` and sets `boot_status` to `READY` in
   `RuntimeContext` only when every required report agrees the runtime is
   ready. If any required report disagrees, `runtime.mark_failed()`
   transitions `READY -> FAILED`, `boot_status` is set to `FAILED`, and
   `boot()` returns `False`. `RuntimeContext` never claims a readiness fact
   that contradicts `lifecycle_state`.

`StartupValidator` readiness is derived only from `lifecycle_state` plus
`RuntimeValidator`/`DependencyValidator` delegation — never from the legacy
`config_manager_status`, `executive_brain_status`, or `startup_manager_status`
context keys, which nothing in the canonical composition path sets.

Calling `boot()` again on an already-`READY` or `FAILED` runtime raises
`LifecycleTransitionError` at `runtime.initialize()` before any container or
registry mutation occurs; `BootManager.steps` is reset at the start of every
`boot()` attempt, so step reporting never accumulates across attempts.

## Coordinated shutdown

`BootManager.shutdown()` only calls `runtime.stop()` from a state where
`STOPPING` is a legal transition (`INITIALIZED`, `READY`, `DEGRADED`); from
any other state (never started, or already terminal) the illegal transition
is avoided rather than attempted and reported as a failure.

`runtime.stop()` tears down every owned platform service in the reverse of
its registration order. An individual teardown failure does not stop the
unwind: every owned service is still given a chance to release, failures are
aggregated, and if any occurred the runtime transitions to `FAILED` (not
`STOPPED`) and raises one `PartialShutdownError` naming every failure.

On a successful shutdown, `BootManager` clears the boot-time reports
(`runtime_report`, `startup_report`, `dependency_report`, `health_report`)
from `RuntimeContext` so it cannot keep claiming readiness facts about a
runtime that is no longer running, publishes the shutdown notification, and
releases `EventBus` subscriptions as the final step.

`EventBus.publish()` isolates each subscriber: a subscriber exception is
logged and does not stop remaining subscribers from running or propagate
into the lifecycle operation that published the event.

## Health

`RuntimeHealthCertifier` reports one of `HealthStatus.HEALTHY`, `DEGRADED`,
`FAILED`, or `UNKNOWN` per owned service, derived from whether the service
instance actually exists — never `HEALTHY` merely because a name is
registered. Overall health is `FAILED` if any service failed, `DEGRADED` if
`lifecycle_state` is not `READY` or an unrecognized service is present,
`UNKNOWN` if there is nothing yet to check, and `HEALTHY` only when every
real check passes.

`DEGRADED` is representable and reachable on a live runtime via
`PlatformRuntime.mark_degraded()`/`mark_recovered()`. The operational policy
for when a real subsystem should trigger that transition is owned by
FORTRESS-10, not by the Runtime Platform.

---

# Extended / Future Lifecycle Vision

The remainder of this document describes a broader conceptual lifecycle for
later JAOS phases (plugin ecosystem, learning loop, multi-source request
intake). It is not yet implemented and is not superseded by the canonical
section above except where they directly conflict on the Runtime Platform
layer.

# Lifecycle Overview

```text
Boot
    ↓
Initialization
    ↓
Idle
    ↓
Request Processing
    ↓
Task Execution
    ↓
Monitoring
    ↓
Learning
    ↓
Idle
    ↓
Shutdown
```

---

# Runtime States

## Boot

Load platform.

Initialize Kernel.

Verify Core.

---

## Initialization

Load:

- Configuration
- Providers
- Plugins
- Memory
- Executive Brain

---

## Ready

JAOS waits for work.

Possible sources:

- User
- Scheduler
- Automation
- Events
- APIs

---

## Request Processing

Incoming requests are:

- Validated
- Classified
- Planned
- Prioritized

---

## Task Execution

Execution may involve:

- Tools
- Providers
- Agents
- Workflows

Tasks may execute:

- Sequentially
- In parallel
- Asynchronously

---

## Monitoring

Continuously observe:

- CPU
- Memory
- Provider health
- Plugin health
- Queue length
- Failures

---

## Learning

After execution:

Update:

- Memory
- Provider statistics
- Tool statistics
- User preferences
- Behavior patterns

---

## Idle

During idle:

- Cleanup
- Memory consolidation
- Background indexing
- Health checks
- Scheduled tasks

---

## Shutdown

Perform:

- Save runtime state
- Flush logs
- Save memory
- Close providers
- Stop services

---

# Recovery

Unexpected shutdown:

```text
Crash
    ↓
Checkpoint
    ↓
Recovery Manager
    ↓
State Restoration
    ↓
Health Validation
    ↓
Resume
```

---

# Runtime Principles

- Always recoverable
- Observable
- Deterministic
- Secure
- Resource-aware

---

# Principle

JAOS remains continuously aware of its own operational state and can recover safely whenever possible.
