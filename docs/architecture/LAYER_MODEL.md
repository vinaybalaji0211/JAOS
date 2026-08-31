\# JAOS Layer Model



\## Version



Architecture Freeze v1.0



\---



\## Current Governance Clarification — ADR-0014



This frozen layer model is preserved as historical design evidence. ADR-0014
supersedes statements below that place canonical provider routing or ownership
inside the legacy Executive Brain. Current provider authority is composed
through `PlatformComposition` -> `ProviderManager`/`AIManager` -> canonical
provider abstractions -> deterministic `MockProvider`. OpenAI is only an
initial FORTRESS-09 reference-provider candidate, Ollama is optional, and
FORTRESS-09 remains NOT STARTED.



\---



\# Philosophy



JAOS follows a strict layered architecture.



Each layer has:



\- A single responsibility

\- A defined API

\- Allowed dependencies

\- Forbidden dependencies



A layer may only depend on layers below it unless an explicit interface or event contract exists.



\---



\# Layer 1 — User Layer



Purpose:



Represents the human operator.



Responsibilities:



\- Issue commands

\- Receive responses

\- Approve sensitive actions

\- Configure JAOS



Examples:



\- Keyboard

\- Mouse

\- Voice

\- Mobile App

\- REST API

\- Future AR/HUD



Never contains business logic.



\---



\# Layer 2 — Interface Layer



Purpose:



Translate human interaction into structured requests.



Components:



\- Voice

\- Dashboard

\- Vision

\- Mobile

\- Web UI

\- API Gateway



Responsibilities:



\- Input validation

\- Session handling

\- UI rendering

\- Voice transcription

\- Image preprocessing



Allowed dependencies:



\- Executive Brain



Forbidden:



\- Memory

\- Kernel

\- Core

\- Direct provider access



\---



\# Layer 3 — Executive Brain



Purpose:



Operating intelligence of JAOS.



Responsibilities:



\- Intent recognition

\- Planning

\- Decision making

\- Tool selection

\- Agent coordination

\- Provider routing

\- Reflection

\- Learning orchestration



Components:



\- Executive Controller

\- Mission Manager

\- Task Planner

\- Tool Manager

\- Provider Manager

\- Reasoning Engine



Allowed dependencies:



\- Domain Services

\- Core



Forbidden:



\- Kernel internals

\- UI implementation



\---



\# Layer 4 — Domain Services



Purpose:



Provide reusable platform capabilities.



Domains:



\- Memory

\- Knowledge

\- Workflow

\- Communication

\- Security

\- Infrastructure

\- PC Control

\- Dashboard

\- Plugins



Responsibilities:



Implement domain-specific business logic.



Allowed dependencies:



\- Core



Forbidden:



\- User interfaces

\- Executive Brain internals



\---



\# Layer 5 — Core Runtime



Purpose:



Provide runtime services.



Components:



\- Engine

\- Event System

\- Scheduler

\- Recovery

\- Snapshot

\- Health Monitor

\- Config

\- Permissions

\- Plugin Manager



Responsibilities:



\- Runtime coordination

\- Monitoring

\- Recovery

\- Execution



Allowed dependencies:



\- Kernel



Forbidden:



\- Executive Brain logic



\---



\# Layer 6 — Kernel



Purpose:



Lowest JAOS software layer.



Responsibilities:



\- Boot

\- Shutdown

\- Lifecycle

\- Service Registry

\- Routing

\- Runtime Context

\- Permission Gateway



Allowed dependencies:



Operating System only.



Forbidden:



Everything above.



\---



\# Layer 7 — Operating System



Purpose:



External execution environment.



Includes:



\- Windows

\- Future Linux

\- File System

\- Network

\- CPU

\- GPU

\- RAM

\- Cloud Hardware



\---



\# Dependency Rule



Dependencies always flow downward.



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



\---



\# Cross-Layer Communication



Cross-layer communication must occur through one of the following:



\- Public API

\- Event Bus

\- Message Queue

\- Registry

\- Service Interface



Direct cross-layer imports are prohibited unless documented.



\---



\# Design Principles



Every layer must be:



\- Replaceable

\- Testable

\- Observable

\- Secure

\- Independent

\- Extensible



\---



\# Long-Term Goal



The layer model ensures JAOS remains maintainable as it evolves into:



\- Multi-agent platform

\- AI operating system

\- Distributed runtime

\- Robotics controller

\- Cloud-native platform

\- Mobile companion

