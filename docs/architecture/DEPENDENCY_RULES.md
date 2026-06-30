\# JAOS Dependency Rules



\## Version



Architecture Freeze v1.0



\---



\# Purpose



This document defines the dependency rules for every JAOS subsystem.



The objective is to prevent:



\- Circular dependencies

\- Tight coupling

\- Layer violations

\- Architecture drift



Every new module must comply with these rules.



\---



\# Global Rule



Dependencies always flow downward.



```

User

↓



Interface

↓



Executive Brain

↓



Domain Services

↓



Core Runtime

↓



Kernel

↓



Operating System

```



No layer may directly depend on a higher layer.



\---



\# Layer Dependency Matrix



| Layer | May Depend On |

|---------|---------------|

| User | Interface |

| Interface | Executive Brain |

| Executive Brain | Domain Services, Core |

| Domain Services | Core |

| Core | Kernel |

| Kernel | Operating System |

| Operating System | External only |



\---



\# Forbidden Dependencies



Kernel must never import:



\- Executive Brain

\- Memory

\- Knowledge

\- Dashboard

\- Voice

\- Vision



Core must never import:



\- Dashboard

\- Voice

\- Vision



Domain Services must never import:



\- Dashboard

\- Voice

\- Vision



Interface must never access:



\- Kernel internals

\- Snapshot internals

\- Recovery internals



\---



\# Allowed Cross-Layer Communication



Cross-layer interaction must occur through one of:



\- Public API

\- Event Bus

\- Registry

\- Service Interface

\- Message Queue



Direct imports are discouraged unless documented.



\---



\# Event-Based Communication



Preferred pattern:



```

Component A



↓



Publish Event



↓



Event Bus



↓



Subscriber



↓



Component B

```



Avoid direct calls when asynchronous behavior is appropriate.



\---



\# Service Registry Pattern



Subsystems should discover services through registries rather than hard-coded references whenever practical.



Examples:



\- Tool Registry

\- Provider Registry

\- Plugin Registry

\- Service Registry



\---



\# Plugin Rule



Plugins must never modify Core or Kernel.



Plugins communicate only through documented plugin interfaces.



\---



\# Provider Rule



Providers must never contain business logic.



Responsibilities:



\- Execute requests

\- Return responses

\- Report health

\- Report capabilities



Decision-making belongs to the Executive Brain.



\---



\# Memory Rule



Memory stores information.



Memory does not decide actions.



Reasoning belongs to the Executive Brain.



\---



\# Knowledge Rule



Knowledge provides facts.



Knowledge does not execute tasks.



\---



\# Security Rule



Every privileged action must pass through:



Permission Manager



or



Kernel Permission Gateway



No bypasses.



\---



\# Testing Rule



Every new subsystem must include:



\- Unit tests

\- Integration tests

\- Architecture validation



\---



\# Import Rule



Imports should follow the smallest stable abstraction.



Prefer:



```

Registry

↓



Interface

↓



Implementation

```



Avoid importing concrete implementations when an interface exists.



\---



\# Future Rule



If a dependency violates this document:



\- Refactor the design.

\- Do not add exceptions without an Architecture Decision Record (ADR).



\---



\# Principle



Architecture is permanent.



Implementation may change.

