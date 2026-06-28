\# JAOS Engineering Handbook



Version: 1.0



Status: Active



Authority: Secondary (after the Constitution)



\---



\# Purpose



This handbook defines the engineering process used to build JAOS.



Every contributor—including AI agents—must follow these standards.



\---



\# Development Workflow



Every component follows this lifecycle:



Architecture Review



↓



Design Review



↓



Alpha Suggestions Review



↓



Implementation



↓



Unit Testing



↓



Integration Testing (if applicable)



↓



Code Review



↓



Documentation Update



↓



Git Commit



↓



GitHub Push



↓



Component Lock



↓



Roadmap Update



\---



\# Architecture Review Checklist



Before implementation answer:



1\. What problem does this solve?



2\. Which layer owns this responsibility?



3\. Does another component already solve this?



4\. Does this violate architecture?



5\. Does it belong in Alpha?



Only after all answers are satisfactory should implementation begin.



\---



\# Coding Standards



Every module must:



• Have one responsibility.



• Use meaningful names.



• Include type hints.



• Include docstrings for public APIs.



• Avoid duplicated logic.



• Avoid unnecessary complexity.



• Prefer readability over cleverness.



\---



\# Testing Policy



Every component must include:



✔ Unit Tests



✔ Invalid Input Tests



✔ Edge Case Tests



✔ Regression Tests (when fixing bugs)



Integration tests are required whenever a component interacts with another layer.



\---



\# Git Workflow



Commit only tested code.



Commit message format:



feat:



fix:



docs:



test:



refactor:



perf:



chore:



Push every completed milestone.



Never leave completed work only on the local machine.



\---



\# Documentation Policy



Documentation is treated as source code.



Whenever code changes:



• Update documentation.



• Update project state.



• Update roadmap if required.



• Update changelog if required.



\---



\# Component Lifecycle



Planned



↓



In Progress



↓



Testing



↓



Review



↓



Locked



Only locked components become architectural dependencies.



\---



\# Definition of Done



A component is complete only when:



Architecture reviewed.



Implementation complete.



Tests passed.



Documentation updated.



Git committed.



GitHub pushed.



Component locked.



\---



\# Suggestion Classification



🟢 Alpha



Required for current milestone.



🔵 Beta



Useful after Alpha.



🟡 Version 1



Production enhancement.



🟣 Research



Future investigation.



\---



\# Repository Policy



GitHub is the single source of truth.



Every completed milestone must exist in GitHub.



No completed feature should exist only on a developer machine.



\---



\# AI Development Policy



AI assists.



AI explains.



AI recommends.



Founder decides.



AI never silently redesigns architecture.



\---



\# Quality Goal



Simple today.



Extensible tomorrow.



Reliable always.

