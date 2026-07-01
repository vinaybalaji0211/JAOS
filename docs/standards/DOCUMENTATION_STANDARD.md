\# JAOS Documentation Standard



Document ID: STD-0001



Document Version: 1.0



Repository Version: 0.5.0-alpha



Status: Active



Owner: JAOS Engineering



Last Updated: 2026-07-01



\---



\# Purpose



This document defines the official documentation standards for the JAOS repository.



It establishes a consistent structure, terminology, and maintenance process so that documentation evolves together with the codebase and remains the primary source of project knowledge.



\---



\# Core Principles



1\. The repository is the source of truth.

2\. Documentation evolves together with code.

3\. Every document has one clearly defined responsibility.

4\. Documentation must be evidence-based.

5\. Avoid duplication; reference related documents instead.

6\. Documentation is reviewed with the same discipline as code.

7\. A platform is not complete until its documentation is synchronized.



\---



\# Documentation Categories



\## Project



High-level repository information.



Examples:



\- README.md

\- PROJECT\_STATE.md

\- ROADMAP.md

\- CHANGELOG.md

\- MILESTONES.md



\---



\## Architecture



System design, platform structure, interfaces, dependencies, contracts, and migration plans.



Location:



docs/architecture/



\---



\## Engineering



Development workflow, coding standards, technical debt, improvements, engineering decisions, repository status.



Location:



docs/engineering/



\---



\## Certification



Engineering certification reports for completed platforms.



Location:



docs/certification/



\---



\## Standards



Repository-wide engineering and documentation standards.



Location:



docs/standards/



\---



\## Release



Release notes and phase summaries.



Location:



docs/releases/ (future)



\---



\## Platform



Platform-specific documentation.



Location:



docs/platforms/ (future)



\---



\# Required Metadata



Every major document should contain:



\- Document ID

\- Document Name

\- Document Version

\- Repository Version

\- Status

\- Owner

\- Last Updated

\- Related Documents



\---



\# Standard Document Structure



1\. Metadata



2\. Purpose



3\. Executive Summary



4\. Detailed Information



5\. Current Status



6\. Related Documents



7\. Update History



\---



\# Status Vocabulary



Use only the following status values:



\- Planned

\- In Progress

\- Implemented

\- Certified

\- Completed

\- Deprecated

\- Archived



\---



\# Documentation Lifecycle



Every major documentation update follows:



Audit



↓



Review



↓



Update



↓



Approval



↓



Commit



\---



\# Engineering Lifecycle



Research



↓



Architecture



↓



Implementation



↓



Unit Testing



↓



Integration Testing



↓



Repository Audit



↓



Certification



↓



Improvement Sprint



↓



Documentation Synchronization



↓



Git Checkpoint



\---



\# Writing Guidelines



\- Write objectively.

\- Use evidence rather than opinions.

\- Keep summaries concise.

\- Preserve historical information.

\- Avoid duplicated explanations.

\- Prefer links or references over copied content.



\---



\# Cross References



Related information should be linked instead of duplicated.



Each document should identify its related documents.



\---



\# Versioning



Repository Version and Document Version are independent.



Example:



Repository Version:

0.5.0-alpha



Document Version:

2.1



\---



\# Repository Philosophy



Documentation is part of the product.



A feature is not complete until its documentation, tests, and certification (where applicable) are complete.



\---



\# Approval



This standard applies to every current and future document within the JAOS repository.

