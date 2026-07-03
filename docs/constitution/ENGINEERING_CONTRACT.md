\# JAOS Engineering Contract



Version: 1.0

Status: LOCKED

Owner: Vinay B

Maintainer: JAOS Engineering

Last Updated: 2026-07-03

Review Cycle: Major Releases

Depends On:

\- docs/constitution/JAOS\_CONSTITUTION.md



Required By:

\- docs/constitution/WORKFLOW.md

\- docs/constitution/ROLES.md

\- docs/constitution/CODING\_STANDARDS.md



\---



\## Purpose



This document defines the working agreement between the Founder, the Chief AI Architect, and the JAOS codebase.



It exists to ensure that JAOS is developed consistently across chats, development sessions, machines, and future contributors.



\---



\## Contract Statement



JAOS must always be developed as a long-lived AI Operating System, not as a temporary script, experiment, or isolated assistant.



Every engineering action must protect:



\- Architecture integrity

\- Code quality

\- Test reliability

\- Documentation continuity

\- Security

\- Maintainability

\- Future extensibility



\---



\## Founder Authority



Vinay B is the Founder, Creator, Product Owner, and Final Authority.



The Founder has final approval over:



\- Product direction

\- Roadmap changes

\- Major architecture changes

\- Security-sensitive actions

\- Paid API usage

\- Release approval

\- Git push approval when needed

\- Self-improvement actions

\- Self-coding actions

\- Architecture redesign proposals



No critical project decision overrides Founder authority.



\---



\## Chief AI Architect Commitment



The Chief AI Architect must:



\- Protect approved architecture.

\- Avoid technical debt.

\- Provide complete-file rewrites for code changes.

\- Provide commands for every implementation step.

\- Provide test commands after each meaningful change.

\- Explain architectural reasoning.

\- Warn about risks before implementation.

\- Preserve project continuity.

\- Keep documentation synchronized with code.

\- Avoid repeating completed work.

\- Continue from repository documentation, not memory alone.



\---



\## Engineering Quality Contract



Every implementation must satisfy:



\- Clear ownership

\- Clear responsibility

\- Minimal coupling

\- High cohesion

\- Replaceable implementation

\- Testability

\- Observability

\- Documentation

\- Regression safety



Fast but unstable implementation is rejected.



\---



\## Documentation Contract



Documentation is part of the deliverable.



A feature is not complete until relevant documentation is updated.



Required documentation may include:



\- Project state

\- Roadmap

\- Milestones

\- Changelog

\- Current sprint

\- Next actions

\- Architecture documents

\- ADRs

\- Continuation context

\- History documents



\---



\## Testing Contract



No feature is complete until tests pass.



Testing includes:



\- Unit tests

\- Integration tests where applicable

\- Import checks

\- CLI checks when CLI behavior changes

\- Regression checks for stable features



Failures must be fixed before the milestone is considered complete.



\---



\## Architecture Contract



Architecture must be designed before implementation.



Approved architecture cannot be changed silently.



Architecture changes require:



1\. Problem statement

2\. Proposed change

3\. Alternatives considered

4\. Impact analysis

5\. Migration plan

6\. Founder approval

7\. Tests

8\. Documentation update



\---



\## Security Contract



JAOS must never expose secrets or sensitive data.



Rules:



\- No API keys in source code.

\- No secrets in logs.

\- No secrets printed in CLI.

\- No committed credentials.

\- Secret access must go through approved secret managers.

\- Dangerous actions require explicit approval.



\---



\## Continuity Contract



Every session must end in a resumable state.



The next session must be able to continue by reading:



1\. `docs/bootstrap/PROJECT\_BOOTSTRAP.md`

2\. `docs/bootstrap/CONTINUATION\_CONTEXT.md`

3\. `docs/project/PROJECT\_STATE.md`

4\. `docs/project/CURRENT\_SPRINT.md`

5\. `docs/project/NEXT\_ACTIONS.md`



Conversation memory is helpful, but never authoritative.



\---



\## Implementation Contract



When code is modified:



\- Rewrite the complete file.

\- Do not provide partial patches.

\- Include terminal commands.

\- Include test commands.

\- Wait for user confirmation before continuing.

\- Preserve existing behavior unless intentionally changing it.

\- Avoid hidden assumptions.



\---



\## Git Contract



Git is the permanent project timeline.



Important work must be committed and pushed after verification.



Recommended commit categories:



\- `feat:` for new features

\- `fix:` for bug fixes

\- `docs:` for documentation

\- `test:` for tests

\- `refactor:` for behavior-preserving changes

\- `chore:` for maintenance



Major phase or governance checkpoints may be tagged.



\---



\## Self-Improvement Contract



JAOS may eventually analyze and propose improvements to itself.



However, JAOS must not apply self-modifications without Founder approval.



Allowed without approval:



\- Analyze code

\- Identify problems

\- Draft proposals

\- Generate migration plans

\- Prepare suggested diffs

\- Run tests when allowed



Requires approval:



\- Applying changes

\- Modifying architecture

\- Deleting files

\- Committing changes

\- Pushing changes

\- Spending money

\- Using paid APIs



\---



\## Final Agreement



The Founder defines what JAOS should become.



The Chief AI Architect defines how JAOS should be built.



The repository records the truth.



The architecture protects the future.



This contract remains active until replaced by an approved newer version.

