\# JAOS Foundation Status



\## Purpose



This document defines the current status of every major root-level folder in the JAOS repository.



Status types:



\* \*\*Production\*\*: Active, tested, and currently used.

\* \*\*Foundation\*\*: Valuable architecture skeleton or future subsystem.

\* \*\*Documentation\*\*: Project knowledge, planning, or governance.

\* \*\*Infrastructure\*\*: Supporting project/runtime files.

\* \*\*Local Only\*\*: Must not be committed.

\* \*\*Review\*\*: Needs later inspection.



\---



\## Production Components



| Folder             | Status                | Notes                                                          |

| ------------------ | --------------------- | -------------------------------------------------------------- |

| `executive\_brain/` | Production            | Main tested Executive Brain backend.                           |

| `core/`            | Production/Foundation | Still used by tests through `core.kernel`. Do not move/delete. |

| `tests/`           | Production            | Main validation layer. Current suite: 386 passing tests.       |

| `config/`          | Production            | Configuration package.                                         |

| `jaos\_platform/`   | Production/Foundation | Platform contract layer. Preserve.                             |



\---



\## Foundation / Planned Subsystems



| Folder             | Status            | Notes                                                                                       |

| ------------------ | ----------------- | ------------------------------------------------------------------------------------------- |

| `brain/`           | Foundation        | Cognitive blueprint: agents, reasoning, self-awareness, planning, learning.                 |

| `kernel/`          | Foundation        | Future OS kernel/runtime lifecycle layer.                                                   |

| `memory/`          | Foundation        | Future long-term/semantic memory subsystem.                                                 |

| `communication/`   | Foundation        | Email, calendar, contacts, and communication layer.                                         |

| `dashboard/`       | Foundation        | Future UI/backend dashboard components.                                                     |

| `development/`     | Foundation        | Development workspace, GitHub, VS Code, and repository management.                          |

| `engineering/`     | Foundation        | Validation, reports, package registry, and project health tooling.                          |

| `infrastructure/`  | Foundation        | Provider, storage, database, resource orchestration concepts.                               |

| `knowledge/`       | Foundation        | Knowledge base, OCR, research, and learning synchronization.                                |

| `pc\_control/`      | Foundation        | PC/application/browser/window/terminal control concepts.                                    |

| `providers/`       | Foundation        | Future provider expansion area.                                                             |

| `security/`        | Foundation        | Authentication, authorization, permission, audit, and monitoring concepts.                  |

| `system\_services/` | Foundation        | Backup, cleanup, configuration, startup, update, scheduling.                                |

| `tools/`           | Foundation        | Future/general tool namespace. Current production tools are under `executive\_brain/tools/`. |

| `workflow/`        | Foundation        | Automation, task queue, retry, recovery, workflow monitoring.                               |

| `agents/`          | Foundation        | Currently empty or placeholder. Preserve as future agent namespace.                         |

| `exports/`         | Foundation/Review | Output/export area. Review later before using.                                              |



\---



\## Documentation Systems



| Folder/File                  | Status        | Notes                                                                  |

| ---------------------------- | ------------- | ---------------------------------------------------------------------- |

| `docs/`                      | Documentation | Current project docs and architecture standards.                       |

| `JAOS\_BIBLE/`                | Documentation | Long-term vision, contributor, roadmap, and platform knowledge.        |

| `JAOS\_ENGINEERING\_HANDBOOK/` | Documentation | Engineering governance, development workflow, testing, release policy. |

| `JAOS\_KNOWLEDGE\_SYSTEM/`     | Documentation | Project memory, roadmap, ADRs, AI context, continuation protocol.      |

| `README.md`                  | Documentation | Main project entry point.                                              |

| `PROJECT\_STATE.md`           | Documentation | Current project status.                                                |

| `ROADMAP.md`                 | Documentation | Development roadmap.                                                   |

| `CHANGELOG.md`               | Documentation | Project history.                                                       |

| `MILESTONES.md`              | Documentation | Milestone tracking.                                                    |

| `PROJECT\_MANIFEST.md`        | Documentation | Project manifest.                                                      |

| `AI\_CONTEXT.md`              | Documentation | AI assistant/project context.                                          |

| `CONTRIBUTING.md`            | Documentation | Contributor guide.                                                     |

| `CODE\_OF\_CONDUCT.md`         | Documentation | Conduct policy.                                                        |

| `SECURITY.md`                | Documentation | Security policy.                                                       |



\---



\## Infrastructure / Support



| Folder/File            | Status                    | Notes                                                                       |

| ---------------------- | ------------------------- | --------------------------------------------------------------------------- |

| `.github/`             | Infrastructure            | GitHub templates and workflows.                                             |

| `data/`                | Infrastructure            | Runtime/project data, snapshots, backups, memory, diagnostics.              |

| `logs/`                | Infrastructure            | Local logs. Usually ignored unless specific logs are intentionally tracked. |

| `plugins/`             | Infrastructure/Foundation | Plugin area.                                                                |

| `requirements.txt`     | Infrastructure            | Runtime dependency lock/reference.                                          |

| `requirements-dev.txt` | Infrastructure            | Development dependency reference.                                           |

| `.gitignore`           | Infrastructure            | Keeps virtual environments, caches, and generated files out of Git.         |



\---



\## Local Only / Do Not Commit



| Folder/File        | Status     | Notes                                                |

| ------------------ | ---------- | ---------------------------------------------------- |

| `jaos/`            | Local Only | Python virtual environment. Must never be committed. |

| `.pytest\_cache/`   | Local Only | Generated by pytest.                                 |

| `\_\_pycache\_\_/`     | Local Only | Generated Python bytecode cache.                     |

| `audit\_\*.txt`      | Local Only | Temporary audit output.                              |

| `foundation\_\*.txt` | Local Only | Temporary inventory output.                          |

| `repo\_tree.txt`    | Local Only | Temporary repository tree output.                    |

| `\*\_files.txt`      | Local Only | Temporary file inventory output.                     |



\---



\## Current Foundation Decision



The old foundation folders are \*\*not obsolete\*\*.



They represent the long-term JAOS architecture skeleton and should be preserved. The current production implementation lives mainly in `executive\_brain/`, while the foundation folders define planned subsystems for future phases.



Future development must follow this rule:



> Do not delete foundation modules unless they are reviewed, documented, and replaced by a production implementation.



\---



\## Current Validation Baseline



\* Current environment: `jaos`

\* Current test command: `pytest -v tests\\tests`

\* Current expected result: `386 passed`

\* Current production backend: `executive\_brain`

\* Current active legacy dependency: `core.kernel`



\---



\## Next Actions



1\. Create `COMPONENT\_REGISTRY.md`.

2\. Create `ARCHITECTURE\_STATUS.md`.

3\. Create `TECHNICAL\_DEBT.md`.

4\. Update project docs to reflect:



&#x20;  \* 386 passing tests

&#x20;  \* Alpha 0.4 backend

&#x20;  \* old foundation preserved

&#x20;  \* `executive\_brain` as production backend

&#x20;  \* foundation folders as planned subsystems



