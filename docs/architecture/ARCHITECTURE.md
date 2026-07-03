# JAOS Architecture

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
