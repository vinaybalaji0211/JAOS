from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path.cwd()
STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP = ROOT / "docs" / "_backups" / f"dg1_backup_{STAMP}"

DOCS = {
"JAOS_MANIFEST.md": """# JAOS Manifest

Version: 1.0
Status: LOCKED
Owner: Vinay B
Maintainer: JAOS Engineering

JAOS is a modular AI Operating System. The repository is the source of truth.

Start every session by reading:
1. docs/bootstrap/PROJECT_BOOTSTRAP.md
2. docs/bootstrap/CONTINUATION_CONTEXT.md
3. docs/project/PROJECT_STATE.md
4. docs/project/CURRENT_SPRINT.md
5. docs/project/NEXT_ACTIONS.md

Current focus:
DG-1 Documentation Governance, then Phase 6 MS-0023X AI Platform Composition.
""",

"docs/bootstrap/PROJECT_BOOTSTRAP.md": """# Project Bootstrap

Version: 1.0
Status: LOCKED
Owner: Vinay B
Maintainer: JAOS Engineering

## Purpose
Fast onboarding guide for humans and AI sessions.

## Project
JAOS — Jarvis Artificial Operating System.

## Current Rule
Repository documentation is the source of truth.

## Start Order
1. JAOS_MANIFEST.md
2. docs/constitution/JAOS_CONSTITUTION.md
3. docs/bootstrap/CONTINUATION_CONTEXT.md
4. docs/project/PROJECT_STATE.md
5. docs/project/CURRENT_SPRINT.md
6. docs/project/NEXT_ACTIONS.md

## Development Rule
Continue from the last verified checkpoint. Do not redesign approved architecture.
""",

"docs/bootstrap/CONTINUATION_CONTEXT.md": """# Continuation Context

Version: 1.0
Status: ACTIVE
Owner: Vinay B
Maintainer: JAOS Engineering

## Current Checkpoint
DG-1 documentation governance sprint is being completed.

## Completed Recently
- AI Platform diagnostics and telemetry
- Identity Platform and CLI
- Provider profile system and CLI
- Secret Manager
- Provider operational status

## Next Implementation After DG-1
Phase 6 MS-0023X — AI Platform Composition.

## Immediate Next Action
Run documentation QA, tests, commit, push, then resume Phase 6 in a new chat.
""",

"docs/bootstrap/NEW_CHAT_GUIDE.md": """# New Chat Guide

Version: 1.0
Status: LOCKED
Owner: Vinay B
Maintainer: JAOS Engineering

## Rule
Every new chat must resume from repository documentation, not memory alone.

## Required Reading Order
1. JAOS_MANIFEST.md
2. docs/bootstrap/PROJECT_BOOTSTRAP.md
3. docs/bootstrap/CONTINUATION_CONTEXT.md
4. docs/project/PROJECT_STATE.md
5. docs/project/CURRENT_SPRINT.md
6. docs/project/NEXT_ACTIONS.md

## New Chat Prompt
Continue JAOS from repository documentation. Do not redesign approved architecture. Start from the current sprint and next actions.
""",

"docs/constitution/DEVELOPMENT_PHILOSOPHY.md": """# Development Philosophy

Version: 1.0
Status: LOCKED
Owner: Vinay B
Maintainer: JAOS Engineering

JAOS is built as a long-lived AI Operating System.

Principles:
- Architecture before implementation.
- Documentation is part of the deliverable.
- Repository is the source of truth.
- Capability-first design.
- Platform-first architecture.
- Security and stability over speed.
- Human approval for critical actions.
- Every session must end resumable.
""",

"docs/constitution/ENGINEERING_PRINCIPLES.md": """# Engineering Principles

Version: 1.0
Status: LOCKED
Owner: Vinay B
Maintainer: JAOS Engineering

## Core Principles
- Loose coupling
- High cohesion
- Dependency inversion
- Provider abstraction
- Replaceable implementations
- Complete-file rewrites
- Test before completion
- Documentation synchronized with code
- Explainable decisions
- No silent architecture changes
""",

"docs/constitution/WORKFLOW.md": """# Workflow

Version: 1.0
Status: LOCKED
Owner: Vinay B
Maintainer: JAOS Engineering

## Standard Workflow
1. Requirement
2. Architecture
3. Approval when required
4. Complete-file implementation
5. Unit tests
6. Integration tests
7. Documentation update
8. Review
9. Git commit
10. Git push
11. Update continuation context
""",

"docs/constitution/ROLES.md": """# Roles

Version: 1.0
Status: LOCKED
Owner: Vinay B
Maintainer: JAOS Engineering

## Vinay B
Founder, Creator, Product Owner, Final Authority.

## Chief AI Architect
Software architect, AI systems architect, senior engineer, QA, documentation lead, security reviewer, continuity manager.

## Future JAOS
May analyze, suggest, benchmark, and prepare proposals. It must not apply critical changes without approval.
""",

"docs/constitution/CODING_STANDARDS.md": """# Coding Standards

Version: 1.0
Status: LOCKED
Owner: Vinay B
Maintainer: JAOS Engineering

## Python Standards
- Type hints
- Dataclasses for simple models
- Clear module ownership
- No monolithic files
- Complete-file rewrites for changes
- Tests for new behavior
- No hardcoded secrets
- Public APIs through __init__.py
""",

"docs/architecture/ARCHITECTURE.md": """# JAOS Architecture

Version: 1.0
Status: LOCKED
Owner: Vinay B
Maintainer: JAOS Engineering

## Architecture Model
JAOS is composed of modular platforms:
Runtime, Executive, Tool, AI, Identity, Memory, Voice, Vision, Automation, Security, Knowledge, Intelligence, Developer, UX.

## Dependency Rule
Higher-level platforms depend on stable public APIs, not internal implementation details.

## Current Focus
Phase 6 AI Infrastructure. AIManager will become a facade over AIPlatform composition root.
""",

"docs/architecture/CORE_PLATFORMS.md": """# Core Platforms

Version: 1.0
Status: LOCKED
Owner: Vinay B
Maintainer: JAOS Engineering

## Platforms
- Runtime Platform
- Executive Platform
- Tool Platform
- AI Platform
- Identity Platform
- Memory Platform
- Voice Platform
- Vision Platform
- Automation Platform
- Security Platform
- Knowledge Platform
- Intelligence Platform
- Developer Platform
- UX Platform

Every feature must belong to a platform.
""",

"docs/architecture/PLATFORM_GUIDELINES.md": """# Platform Guidelines

Version: 1.0
Status: LOCKED
Owner: Vinay B
Maintainer: JAOS Engineering

Every platform should expose:
- Identity
- Public API
- Manager or facade
- Diagnostics
- Telemetry
- Tests
- Documentation

Platforms must be modular, replaceable, observable, and testable.
""",

"docs/architecture/DEPENDENCY_RULES.md": """# Dependency Rules

Version: 1.0
Status: LOCKED
Owner: Vinay B
Maintainer: JAOS Engineering

## Rules
- Executive may depend on AIManager, not providers directly.
- AIManager may depend on AIPlatform composition.
- Providers must not call Executive directly.
- Tools execute only through Tool Platform.
- Secrets accessed only through SecretManager.
- No circular platform dependencies.
""",

"docs/architecture/ARCHITECTURE_GOVERNANCE.md": """# Architecture Governance

Version: 1.0
Status: LOCKED
Owner: Vinay B
Maintainer: JAOS Engineering

Architecture changes require:
1. Problem statement
2. Proposed design
3. Alternatives considered
4. Impact analysis
5. Migration plan
6. Founder approval
7. Tests
8. Documentation update
""",

"docs/knowledge/ENGINEERING_MEMORY.md": """# Engineering Memory

Version: 1.0
Status: ACTIVE
Owner: Vinay B
Maintainer: JAOS Engineering

## Purpose
Record why JAOS is built the way it is.

## Current Decisions
- Repository is source of truth.
- AIManager will become facade.
- Provider Profiles and Provider Operational Status remain separate.
- Secret Manager centralizes API keys.
- Human approval required for critical actions.
""",

"docs/knowledge/DESIGN_PATTERNS.md": """# Design Patterns

Version: 1.0
Status: ACTIVE
Owner: Vinay B
Maintainer: JAOS Engineering

JAOS uses:
- Facade
- Registry
- Manager
- Strategy
- Dependency Injection
- Provider Abstraction
- Composition Root
- Domain Separation
""",

"docs/knowledge/PROVIDER_CATALOG.md": """# Provider Catalog

Version: 1.0
Status: ACTIVE
Owner: Vinay B
Maintainer: JAOS Engineering

Known providers:
- Mock: local, free, testing only.
- Ollama: local, free, private, hardware dependent.
- OpenAI: cloud, paid, strong coding and reasoning.
- Gemini: cloud, free/paid, multimodal and Google ecosystem.
- Claude: cloud, paid, long context and documents.

Future: Groq, DeepSeek, Mistral, OpenRouter, xAI, HuggingFace, Bedrock, Vertex AI.
""",

"docs/knowledge/ARCHITECTURE_GLOSSARY.md": """# Architecture Glossary

Version: 1.0
Status: ACTIVE
Owner: Vinay B
Maintainer: JAOS Engineering

- Platform: Modular subsystem with clear ownership.
- Facade: Simple public interface hiding internal complexity.
- Provider: Replaceable AI backend.
- Capability: What JAOS needs, independent of vendor.
- Composition Root: Object that wires platform components together.
- Continuation Context: Current working memory for future sessions.
""",

"docs/knowledge/FUTURE_IDEAS.md": """# Future Ideas

Version: 1.0
Status: ACTIVE
Owner: Vinay B
Maintainer: JAOS Engineering

Future JAOS capabilities:
- Provider recommendation engine
- Smart AI router
- API usage and cost tracking
- Architecture redesign proposals
- Safe self-coding with approval
- Voice and HUD
- Vision
- Mobile companion
- Multi-agent intelligence
- Robotics and IoT
""",

"docs/knowledge/VISION_TRACEABILITY.md": """# Vision Traceability

Version: 1.0
Status: ACTIVE
Owner: Vinay B
Maintainer: JAOS Engineering

## Vision Items
- JAOS knows itself: Identity Platform.
- Multi-provider AI: AI Provider Platform.
- API key safety: Secret Manager.
- Provider suggestions: Provider Intelligence.
- Safe self-improvement: Architecture Governance and future Self-Improvement Platform.
- Continuity across chats: Bootstrap and Continuation Context.
""",

"docs/project/PROJECT_STATE.md": """# Project State

Version: 1.0
Status: ACTIVE
Owner: Vinay B
Maintainer: JAOS Engineering

Current Version: v0.7.0-alpha
Current Sprint: DG-1 Documentation Governance
Current Product Phase: Phase 6 AI Infrastructure

## Completed
- Phase 1-5 completed and pushed.
- AI diagnostics and telemetry.
- Executive-AI fallback.
- Identity platform.
- Provider profiles.
- Secret manager.
- Provider operational status.

## Next
Complete DG-1, push, then resume MS-0023X AI Platform Composition.
""",

"docs/project/ROADMAP.md": """# Roadmap

Version: 1.0
Status: ACTIVE
Owner: Vinay B
Maintainer: JAOS Engineering

## Completed
Phase 1 Core Foundation
Phase 2 Engineering Foundation
Phase 3 Tool Platform
Phase 4 Executive Foundation
Phase 5 Executive Platform

## Current
DG-1 Documentation Governance
Phase 6 AI Infrastructure

## Phase 6 Remaining
- AI Platform Composition
- Provider usage and health
- Recommendation engine
- Smart router
- Ollama
- OpenAI
- Gemini
- Claude
- Conversation
- Memory integration
- Dynamic planning
""",

"docs/project/CHANGELOG.md": """# Changelog

Version: 1.0
Status: ACTIVE
Owner: Vinay B
Maintainer: JAOS Engineering

## Unreleased
- Added DG-1 Documentation Governance framework.
- Added repository continuity system.
- Added documentation source-of-truth model.

## v0.7.0-alpha
- AI diagnostics and telemetry.
- Identity Platform.
- Provider profiles.
- Secret Manager.
- Provider operational status.
""",

"docs/project/MILESTONES.md": """# Milestones

Version: 1.0
Status: ACTIVE
Owner: Vinay B
Maintainer: JAOS Engineering

## DG-1
Documentation and Engineering Governance Platform.

## Phase 6 Completed So Far
- MS-0020A AI Architecture Audit
- MS-0021 AI Diagnostics and Telemetry
- MS-0022 Executive AI Integration
- MS-0023 Identity Platform
- MS-0024A Provider Profiles
- MS-0024B Secret Manager
- MS-0024C.1 Provider Operational Status

## Next
MS-0023X AI Platform Composition.
""",

"docs/project/CURRENT_SPRINT.md": """# Current Sprint

Version: 1.0
Status: ACTIVE
Owner: Vinay B
Maintainer: JAOS Engineering

Sprint: DG-1 Documentation Governance

Goal:
Create the permanent documentation, governance, and continuity baseline for JAOS.

Exit:
Docs reviewed, tests pass, committed, pushed, tagged.
""",

"docs/project/NEXT_ACTIONS.md": """# Next Actions

Version: 1.0
Status: ACTIVE
Owner: Vinay B
Maintainer: JAOS Engineering

1. Run documentation generation.
2. Review docs tree.
3. Run pytest.
4. Run python run_jaos.py.
5. Commit docs.
6. Push GitHub.
7. Start new chat.
8. Resume Phase 6 MS-0023X.
""",

"docs/project/KNOWN_ISSUES.md": """# Known Issues

Version: 1.0
Status: ACTIVE
Owner: Vinay B
Maintainer: JAOS Engineering

## Current
- Boot screen still shows v0.6.0-alpha while identity reports v0.7.0-alpha.
- README may contain older project status.
- AIManager needs composition refinement into AIPlatform facade architecture.

## Priority
Fix after DG-1 during Phase 6 implementation.
""",

"docs/project/AI_CONTEXT.md": """# AI Context

Version: 1.0
Status: ACTIVE
Owner: Vinay B
Maintainer: JAOS Engineering

This file helps future AI sessions continue JAOS.

Rules:
- Repository is source of truth.
- Do not redesign approved architecture.
- Complete-file rewrites only.
- Commands and tests required.
- Continue from NEXT_ACTIONS.md.

Current next implementation:
MS-0023X AI Platform Composition.
""",

"docs/templates/ADR_TEMPLATE.md": """# ADR-XXXX Title

Version: 1.0
Status: TEMPLATE
Owner: Vinay B
Maintainer: JAOS Engineering

## Context
Describe the problem.

## Decision
Describe the decision.

## Alternatives Considered
List alternatives.

## Consequences
Describe benefits, tradeoffs, and risks.

## Approval
Founder approval required for major architecture decisions.
""",

"docs/templates/PHASE_HISTORY_TEMPLATE.md": """# Phase XX History

Version: 1.0
Status: TEMPLATE
Owner: Vinay B
Maintainer: JAOS Engineering

## Objective
## Components Added
## Files Created
## Files Modified
## Architecture Decisions
## Problems Encountered
## Solutions
## Tests
## Documentation
## Lessons Learned
## Technical Debt
## Security Notes
## Git Commit
## Certification
""",

"docs/statistics/LIVING_STATISTICS.md": """# Living Statistics

Version: 1.0
Status: ACTIVE
Owner: Vinay B
Maintainer: JAOS Engineering

Current Version: v0.7.0-alpha
Current Product Phase: Phase 6
Current Governance Sprint: DG-1

Completed Product Phases: 5
Current Focus: AI Infrastructure
Tests: 479 passing as last verified
Known Providers: Mock, Ollama, OpenAI, Gemini, Claude

Update this file after major milestones.
""",
}

def write_file(path_text: str, content: str) -> None:
    path = ROOT / path_text
    if path.exists():
        backup_path = BACKUP / path_text
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")

def main() -> None:
    for path, content in DOCS.items():
        write_file(path, content)
    print(f"DG-1 docs generated: {len(DOCS)} files")
    print(f"Backup folder: {BACKUP}")

if __name__ == "__main__":
    main()