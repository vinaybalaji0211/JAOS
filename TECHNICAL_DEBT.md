\# JAOS Technical Debt Register



\## Status



Current Phase: Foundation Audit



Overall Debt Level: Low



\---



\# Active Technical Debt



\## TD-001



Title:

Legacy foundation not yet integrated



Priority:

High



Impact:

Large amount of functionality exists outside the production architecture.



Plan:



\- Audit

\- Categorize

\- Refactor

\- Integrate

\- Test



Status:

Open



\---



\## TD-002



Title:

Placeholder components



Priority:

Medium



Impact:



Several future folders exist but are not yet connected.



Plan:



Implement gradually during roadmap execution.



Status:



Open



\---



\## TD-003



Title:

Architecture duplication



Priority:



Medium



Impact:



Some concepts exist in both the preserved foundation and Executive Brain.



Plan:



Keep the best implementation.



Remove duplication only after validation.



Status:



Pending audit



\---



\## TD-004



Title:



Missing dependency visualization



Priority:



Low



Plan:



Generate architecture graph after subsystem integration.



Status:



Future



\---



\## TD-005



Title:



Capability registry expansion



Priority:



Medium



Plan:



Create centralized capability registry for every subsystem.



Status:



Planned



\---



\# Technical Debt Policy



Technical debt is tracked.



It is never ignored.



Every resolved debt item must reference:



\- commit

\- milestone

\- changelog



No hidden technical debt is allowed.

