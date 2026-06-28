\# JAOS Engineering Decisions



Document ID: JKS-EDC-001



Version: 1.0.0



Status: 🟡 Living



Owner: Founder (Vinay B)



\---



\# Purpose



This document records important engineering decisions and their reasoning.



It explains why JAOS is built the way it is.



\---



\# Decision Register



\## ED-001 — Modular Architecture



Decision:

JAOS uses a modular layered architecture.



Reason:

Modularity improves maintainability, testing, scalability, and future collaboration.



Status:

Active



\---



\## ED-002 — Executive Brain Separate from Kernel



Decision:

The Executive Brain reasons, while the Kernel executes.



Reason:

Reasoning and execution must remain separate for safety and maintainability.



Status:

Active



\---



\## ED-003 — Models Own Data



Decision:

Models store validated data and serialization logic.



Reason:

This keeps data structures predictable and simple.



Status:

Active



\---



\## ED-004 — Registries Store and Retrieve



Decision:

Registries manage storage and lookup of Executive Brain objects.



Reason:

Storage should not be mixed with reasoning or execution.



Status:

Active



\---



\## ED-005 — JKS as Project Memory



Decision:

JAOS uses the Knowledge System as persistent project memory.



Reason:

The project must survive new chats, new AI models, future contributors, and long-term development.



Status:

Active



\---



\## ED-006 — Human Approval for Critical Actions



Decision:

Critical actions require Founder or user approval.



Reason:

JAOS must assist humans, not silently override them.



Status:

Active



\---



\## ED-007 — Manual GitHub Sync Until Automation



Decision:

Repository updates remain manual until GitHub Sync Manager exists.



Reason:

Automatic pushes are risky and must require Founder approval.



Status:

Active



\---



\## ED-008 — Self-Awareness as Alpha Requirement



Decision:

JAOS must know its identity, capabilities, limitations, version, and roadmap.



Reason:

Trustworthy AI must be honest about what it can and cannot do.



Status:

Active



\---



\## ED-009 — Feature Classification



Decision:

Every idea is classified before implementation.



Reason:

This prevents feature creep while preserving innovation.



Status:

Active



\---



\## ED-010 — Documentation Supports Software



Decision:

Documentation exists to support JAOS development, not delay it.



Reason:

After JKS v1.0, documentation should evolve only when software changes require it.



Status:

Active



\---



\# Rule



Future major engineering decisions must be recorded here.



\---



\# Related Documents



\- JAOS Constitution

\- DEVELOPMENT\_RULES.md

\- ARCHITECTURE\_IMPROVEMENTS.md

\- COMPLETE\_ROADMAP.md



\---



End of Document

