\# JAOS Executive Brain Architecture



\## Version



Architecture Freeze v1.0



Status: Draft



\---



\## Current Governance Clarification — ADR-0014



This frozen draft is preserved as historical Executive Brain design evidence.
ADR-0014 supersedes statements below that assign canonical provider ownership,
selection, or routing to the legacy Executive Brain or treat its concrete
OpenAI/Ollama adapters as permanent JAOS contracts. Current provider authority
uses the canonical `PlatformComposition` -> `ProviderManager`/`AIManager` ->
provider-abstraction path and deterministic `MockProvider`. OpenAI is only an
initial FORTRESS-09 reference-provider candidate; Ollama remains optional;
FORTRESS-09 remains NOT STARTED.



\---



\# Purpose



The Executive Brain is the operating intelligence of JAOS.



It is responsible for understanding goals, planning work,

coordinating subsystems, selecting AI providers, managing tools,

and learning from execution.



The Executive Brain never directly performs platform work.



Instead, it orchestrates every subsystem.



\---



\# Core Philosophy



Think.



Plan.



Delegate.



Observe.



Learn.



Improve.



\---



\# Position inside JAOS



```text

User



↓



Interface Layer



↓



Executive Brain



↓



Domain Services



↓



Core Runtime



↓



Kernel



↓



Operating System

```



The Executive Brain is the decision layer.



\---



\# Responsibilities



The Executive Brain owns:



\- Intent understanding

\- Goal management

\- Planning

\- Task decomposition

\- Multi-step reasoning

\- Provider routing

\- Tool selection

\- Agent coordination

\- Context management

\- Memory interaction

\- Reflection

\- Continuous learning

\- Safety validation

\- Execution supervision



\---



\# Internal Components



\## Intent Engine



Responsibilities



\- Understand user requests

\- Detect hidden intent

\- Resolve ambiguity



Output



Structured objective.



\---



\## Goal Manager



Responsibilities



\- Convert objectives into goals

\- Prioritize goals

\- Resolve conflicts



\---



\## Planner



Responsibilities



Generate execution plans.



Example



Goal



↓



Subtasks



↓



Execution order



↓



Dependencies



↓



Expected result



\---



\## Reasoning Engine



Responsibilities



Evaluate possible solutions.



Support



\- Logical reasoning

\- Multi-step reasoning

\- Comparative analysis

\- Confidence estimation



\---



\## Tool Manager



Responsibilities



Determine



\- Which tools are required

\- Execution order

\- Parallel execution

\- Recovery strategy



\---



\## Provider Router



Responsibilities



Select the best AI provider.



Selection based on



\- Capability

\- Cost

\- Speed

\- Availability

\- Privacy

\- Context length



\---



\## Agent Coordinator



Responsibilities



Assign work to specialized agents.



Examples



\- Coding Agent

\- Research Agent

\- Memory Agent

\- Vision Agent

\- Document Agent



\---



\## Memory Coordinator



Responsibilities



Communicate with



\- Short-term memory

\- Long-term memory

\- Knowledge base



Responsibilities



Store



Retrieve



Summarize



Compress



Reuse



\---



\## Reflection Engine



Responsibilities



After execution



Evaluate



\- Success

\- Failure

\- Confidence

\- Lessons learned



Generate improvements.



\---



\## Learning Manager



Responsibilities



Update



\- Behavior patterns

\- Preferences

\- Provider performance

\- Tool statistics



\---



\# Decision Pipeline



```text

User Request



↓



Intent Detection



↓



Goal Generation



↓



Planning



↓



Reasoning



↓



Provider Selection



↓



Tool Selection



↓



Agent Assignment



↓



Execution



↓



Observation



↓



Reflection



↓



Memory Update



↓



Response

```



\---



\# Interaction with Memory



Executive Brain



↓



Working Memory



↓



Conversation Memory



↓



Long-Term Memory



↓



Knowledge Base



↓



Reasoning History



Executive Brain never stores raw files.



Memory subsystem owns persistence.



\---



\# Interaction with Providers



Executive Brain never depends on a single provider.



Supported providers include



\- Ollama

\- OpenAI

\- Claude

\- Gemini

\- DeepSeek

\- Perplexity

\- Qwen

\- Future providers



Providers are interchangeable.



\---



\# Interaction with Tools



Executive Brain decides



What tool



When



Why



Execution order



Expected output



Tools never decide strategy.



\---



\# Safety Rules



Every execution passes through



Permission Layer



Risk Evaluation



Policy Validation



Human Approval (when required)



\---



\# Failure Strategy



If execution fails



1\. Retry

2\. Select another tool

3\. Select another provider

4\. Request clarification

5\. Escalate to user



Never silently fail.



\---



\# Long-Term Evolution



Future Executive Brain capabilities



\- Autonomous planning

\- Predictive assistance

\- Self-improvement planning

\- Multi-agent societies

\- Long-term project management

\- Distributed execution

\- Robotics coordination



\---



\# Principle



The Executive Brain does not execute work.



It decides what work should be executed,

which subsystem should execute it,

and verifies the outcome.

