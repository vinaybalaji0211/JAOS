\# JAOS Component Dependency Matrix



\## Version



Architecture Freeze v1.0



\---



\# Purpose



This document defines every major JAOS subsystem, its responsibility,

allowed dependencies, and consumers.



It serves as the master architectural reference for subsystem interactions.



\---



\# Component Matrix



| Component | Layer | Depends On | Used By | Status |

|-----------|-------|------------|---------|--------|

| Kernel | Kernel | Operating System | Core | Production |

| Core | Core Runtime | Kernel | Executive Brain, Domain Services | Production |

| Executive Brain | Executive Brain | Core, Domain Services | Interface | Production |

| Memory | Domain Services | Core | Executive Brain | Foundation |

| Knowledge | Domain Services | Core | Executive Brain | Foundation |

| Workflow | Domain Services | Core | Executive Brain | Foundation |

| Security | Domain Services | Core | Executive Brain, Core | Foundation |

| Communication | Domain Services | Core | Executive Brain | Foundation |

| PC Control | Domain Services | Core | Executive Brain | Foundation |

| Infrastructure | Domain Services | Core | Executive Brain | Foundation |

| Dashboard | Interface | Executive Brain | User | Foundation |

| Plugins | Domain Services | Core | Executive Brain | Reserved |

| Providers | Domain Services | Core | Executive Brain | Reserved |

| Engineering | Domain Services | Core | Developers | Foundation |

| Development | Domain Services | Core | Developers | Foundation |



\---



\# Component Responsibilities



\## Kernel



Primary responsibility:



\- Platform lifecycle

\- Boot

\- Shutdown

\- Service registry

\- Runtime routing



\---



\## Core



Primary responsibility:



\- Runtime services

\- Scheduling

\- Events

\- Recovery

\- Configuration

\- Monitoring



\---



\## Executive Brain



Primary responsibility:



\- Planning

\- Reasoning

\- Decision making

\- Task orchestration

\- Provider routing

\- Agent coordination



\---



\## Memory



Primary responsibility:



\- Store and retrieve information

\- Maintain short-term and long-term memory

\- Preserve execution history



\---



\## Knowledge



Primary responsibility:



\- Structured knowledge

\- Research

\- OCR

\- Knowledge graph

\- Learning synchronization



\---



\## Workflow



Primary responsibility:



\- Task execution

\- Scheduling

\- Automation

\- Retry and recovery



\---



\## Security



Primary responsibility:



\- Authentication

\- Authorization

\- Permissions

\- Audit logging

\- Identity management



\---



\## Infrastructure



Primary responsibility:



\- AI providers

\- APIs

\- Storage

\- Database

\- Resource orchestration



\---



\## PC Control



Primary responsibility:



\- Applications

\- Browser

\- File system

\- Windows

\- Terminal

\- Notifications



\---



\## Dashboard



Primary responsibility:



\- Visual interaction

\- Status display

\- Notifications

\- Mission control



\---



\# Dependency Graph



```text

User

│

▼

Dashboard / Voice / Vision

│

▼

Executive Brain

│

├──────────────┐

│              │

▼              ▼

Core      Domain Services

│              │

└──────┬───────┘

&#x20;      ▼

&#x20;   Kernel

&#x20;      ▼

Operating System

```



\---



\# Design Rules



\- Components communicate through documented interfaces.

\- Cross-component dependencies require justification.

\- Components should remain independently testable.

\- Business logic belongs in Domain Services or Executive Brain.

\- Runtime infrastructure belongs in Core and Kernel.



\---



\# Future Expansion



Reserved components:



\- Vision

\- Voice

\- Mobile

\- Robotics

\- IoT

\- Cloud Runtime

\- Distributed Agents

\- Vector Memory

\- Semantic Search

\- Autonomous Planning



These will integrate into this matrix without altering the core architecture.



\---



\# Guiding Principle



Every new subsystem must answer:



1\. Which layer does it belong to?

2\. What is its single responsibility?

3\. What components may it depend on?

4\. Who is allowed to use it?

5\. How is it tested?

