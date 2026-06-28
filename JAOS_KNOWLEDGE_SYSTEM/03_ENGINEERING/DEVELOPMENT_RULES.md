\# JAOS Development Rules



Document ID: JKS-DEV-001



Version: 1.0.0



Status: 🔒 Locked



Owner: Founder (Vinay B)



Knowledge System Version: 1.0.0



Last Updated: 2026-06-28



\---



\# Purpose



This document defines how JAOS must be developed.



These rules apply to all software, documentation, architecture, AI assistance, and future collaboration.



\---



\# Core Development Lifecycle



Every component follows this lifecycle:



Architecture Review



↓



Implementation



↓



Testing



↓



Review



↓



Knowledge System Update, if needed



↓



Git Commit



↓



Git Push



↓



Lock



↓



Continue



\---



\# Rule 1 — Architecture Before Code



Do not write code before understanding:



\- where the component belongs

\- what its responsibility is

\- what it depends on

\- what must not be included



\---



\# Rule 2 — One Responsibility



Every component must have one clear responsibility.



Examples:



\- Model stores data

\- Registry stores and retrieves

\- Manager coordinates

\- Engine reasons

\- Kernel executes

\- Platform interacts with external systems



\---



\# Rule 3 — Never Redesign Locked Components Casually



Locked components may only change for:



\- bugs

\- security issues

\- required architecture changes

\- approved improvements



Any major change requires review.



\---



\# Rule 4 — Test Before Lock



No component is locked until its test passes.



If a component has no test, it is not complete.



\---



\# Rule 5 — No Guessing Current Code



Before building dependent code, use the current actual file.



If a model or interface is needed, inspect it first.



Do not assume old structures are still correct.



\---



\# Rule 6 — Full Code With Commands



Implementation instructions should include:



\- command to create/open file

\- full rewritten code

\- command to run test

\- expected result



\---



\# Rule 7 — Keep Alpha Focused



Alpha priority:



Make JAOS exist.



Make JAOS work.



Avoid polishing non-critical systems before core systems exist.



\---



\# Rule 8 — Classify Every New Idea



Every idea must be classified as:



\- Current Sprint

\- Alpha

\- Beta

\- Gamma

\- Future

\- Research

\- Rejected



Only Current Sprint and approved Alpha work should interrupt development.



\---



\# Rule 9 — Knowledge Must Stay Synchronized



Update the Knowledge System when:



\- architecture changes

\- roadmap changes

\- engineering discipline changes

\- capabilities change

\- limitations change

\- important decisions are made



\---



\# Rule 10 — Repository Must Stay Synchronized



Until automatic GitHub sync exists, every milestone must be manually committed and pushed.



Required commands:



git status



git add .



git commit -m "type: message"



git push



\---



\# Rule 11 — Human Approval



The AI may recommend.



The Founder decides.



Critical changes require explicit Founder approval.



\---



\# Rule 12 — Security Before Convenience



Do not bypass permission systems.



Do not commit secrets.



Do not automate critical actions without approval.



\---



\# Rule 13 — Simplicity First



Prefer simple, understandable solutions.



Avoid unnecessary abstraction until repeated complexity proves it is needed.



\---



\# Rule 14 — Build, Review, Lock



A component is official only after:



\- it is implemented

\- tested

\- reviewed

\- locked

\- committed

\- pushed



\---



\# Rule 15 — Stable Baseline



The repository should always remain recoverable.



Every milestone should create a safe checkpoint.



\---



\# Related Documents



\- JAOS Constitution

\- PROJECT\_DNA.md

\- AI\_BEHAVIOR.md

\- LOCKED\_COMPONENTS.md

\- COMPLETE\_ROADMAP.md



\---



\# Lock Status



This document is part of the JAOS v1.0 Knowledge System baseline.



Changes require Founder approval.



\---



End of Document

