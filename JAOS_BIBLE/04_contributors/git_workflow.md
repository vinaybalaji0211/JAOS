\# JAOS Git Workflow



\## Purpose



This document explains how contributors work together without damaging the main JAOS codebase.



\---



\## Main Branch Rule



The main branch must always remain stable.



No contributor should directly push unfinished work to main.



\---



\## Branch Naming



Use descriptive branch names.



Examples:



feature/executive-brain-registry



feature/voice-platform



fix/kernel-import-error



docs/update-jaos-bible



\---



\## Standard Workflow



1\. Pull latest main branch.

2\. Create a new feature branch.

3\. Make changes.

4\. Run tests.

5\. Commit changes.

6\. Push branch.

7\. Create Pull Request.

8\. Review architecture.

9\. Review code.

10\. Merge only after approval.



\---



\## Commit Message Examples



Good:



\- Add IntentRegistry

\- Fix MissionModel progress validation

\- Update JAOS Bible contributor guide



Bad:



\- update

\- final

\- changes

\- done



\---



\## Pull Request Rule



Every Pull Request must include:



\- What changed

\- Why it changed

\- Tests run

\- Architecture impact

\- Screenshots if UI changed

