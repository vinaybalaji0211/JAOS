[1mdiff --git a/CHANGELOG.md b/CHANGELOG.md[m
[1mindex aaa8d4d..ff8b804 100644[m
[1m--- a/CHANGELOG.md[m
[1m+++ b/CHANGELOG.md[m
[36m@@ -1,62 +1,98 @@[m
[31m-\# Phase 3 — AI Layer[m
[32m+[m[32m\# JAOS Changelog[m
 [m
 [m
 [m
[31m-\## Added[m
[32m+[m[32m\## v0.4.0-alpha[m
 [m
 [m
 [m
[31m-\* AI Provider Interface[m
[32m+[m[32m\### Added[m
 [m
[31m-\* AI Provider Models[m
 [m
[31m-\* AI Provider Exceptions[m
 [m
[31m-\* AI Provider Manager[m
[32m+[m[32m\- Platform Runtime[m
 [m
[31m-\* Prompt Models[m
[32m+[m[32m\- Service Container[m
 [m
[31m-\* Prompt Engine[m
[32m+[m[32m\- Runtime Context[m
 [m
[31m-\* Centralized AI Configuration[m
[32m+[m[32m\- Event Bus[m
 [m
[31m-\* Ollama Provider[m
[32m+[m[32m\- BasePlatformService[m
 [m
[31m-\* OpenAI Provider[m
[32m+[m[32m\- Boot Manager[m
 [m
[31m-\* Multi-LLM Router[m
[32m+[m[32m\- Runtime Validator[m
 [m
[32m+[m[32m\- Startup Validator[m
 [m
[32m+[m[32m\- Dependency Validator[m
 [m
[31m-\## Architecture[m
[32m+[m[32m\- Runtime Health Certification[m
 [m
[32m+[m[32m\- Executive Pipeline[m
 [m
[32m+[m[32m\- Runtime-managed subsystem architecture[m
 [m
[31m-\* Refactored AI package into:[m
 [m
 [m
[32m+[m[32m\### Integrated[m
 [m
[31m-&#x20; \* providers/[m
 [m
[31m-&#x20; \* prompt/[m
 [m
[31m-&#x20; \* routing/[m
[32m+[m[32m\- Executive Brain[m
 [m
[32m+[m[32m\- Memory[m
 [m
[32m+[m[32m\- Workflow[m
 [m
[31m-\## Testing[m
[32m+[m[32m\- Security[m
 [m
[32m+[m[32m\- Knowledge[m
 [m
[32m+[m[32m\- Infrastructure[m
 [m
[31m-\* Expanded test suite from 138 to \*\*204 passing tests\*\*[m
[32m+[m[32m\- Communication[m
 [m
[32m+[m[32m\- PC Control[m
 [m
[32m+[m[32m\- Dashboard[m
 [m
[31m-\## Release[m
[32m+[m[32m\- Development[m
 [m
[32m+[m[32m\- Engineering[m
 [m
[32m+[m[32m\- System Services[m
 [m
[31m-\*\*v0.1.0-alpha\*\*[m
 [m
 [m
[32m+[m[32m\### Architecture[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32m\- Unified Runtime[m
[32m+[m
[32m+[m[32m\- Unified Boot Sequence[m
[32m+[m
[32m+[m[32m\- Unified Execution Pipeline[m
[32m+[m
[32m+[m[32m\- Dependency Injection[m
[32m+[m
[32m+[m[32m\- Event-driven Platform[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32m\### Testing[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32m\- Full regression suite passing[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32m\### Status[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32mPhase 4.12 nearing completion[m
 [m
[1mdiff --git a/MILESTONES.md b/MILESTONES.md[m
[1mindex 91c4e6c..8370b36 100644[m
[1m--- a/MILESTONES.md[m
[1m+++ b/MILESTONES.md[m
[36m@@ -1,76 +1,53 @@[m
[31m-\# Phase 3 — AI Layer[m
[31m-[m
[31m-[m
[31m-[m
[31m-Status[m
[31m-[m
[32m+[m[32m# JAOS Milestones[m
 [m
[32m+[m[32m## Phase 1[m
 [m
 ✅ COMPLETE[m
 [m
[32m+[m[32m---[m
 [m
[32m+[m[32m## Phase 2[m
 [m
[31m-Completed Milestones[m
[31m-[m
[31m-[m
[31m-[m
[31m-\* JAOS-M-0023[m
[31m-[m
[31m-\* JAOS-M-0024[m
[31m-[m
[31m-\* JAOS-M-0025[m
[31m-[m
[31m-\* JAOS-M-0025.1[m
[31m-[m
[31m-\* JAOS-M-0026[m
[31m-[m
[31m-\* JAOS-M-0027[m
[31m-[m
[31m-\* JAOS-M-0028[m
[31m-[m
[31m-[m
[31m-[m
[31m-Deliverables[m
[31m-[m
[31m-[m
[31m-[m
[31m-\* AI Provider Interface[m
[31m-[m
[31m-\* AI Provider Manager[m
[31m-[m
[31m-\* Prompt Engine[m
[31m-[m
[31m-\* AI Configuration[m
[31m-[m
[31m-\* Ollama Provider[m
[31m-[m
[31m-\* OpenAI Provider[m
[31m-[m
[31m-\* LLM Router[m
[32m+[m[32m✅ COMPLETE[m
 [m
[32m+[m[32m---[m
 [m
[32m+[m[32m## Phase 3[m
 [m
[31m-Testing[m
[32m+[m[32m✅ COMPLETE[m
 [m
[32m+[m[32m---[m
 [m
[32m+[m[32m## Phase 3.5[m
 [m
[31m-\*\*204 / 204 Passing\*\*[m
[32m+[m[32m✅ COMPLETE[m
 [m
[32m+[m[32m---[m
 [m
[32m+[m[32m## Phase 4[m
 [m
[31m-Architecture[m
[32m+[m[32m### Completed[m
 [m
[32m+[m[32m- Platform Runtime[m
[32m+[m[32m- Runtime Integration[m
[32m+[m[32m- Boot Manager[m
[32m+[m[32m- Runtime Validator[m
[32m+[m[32m- Startup Validator[m
[32m+[m[32m- Dependency Validator[m
[32m+[m[32m- Runtime Health Certification[m
[32m+[m[32m- Executive Pipeline[m
[32m+[m[32m- Unified Boot Sequence[m
 [m
[32m+[m[32m### Remaining[m
 [m
[31m-\*\*Frozen\*\*[m
[32m+[m[32m- Documentation Freeze[m
[32m+[m[32m- Architecture Freeze[m
[32m+[m[32m- Platform Certification[m
 [m
[32m+[m[32mStatus[m
 [m
[32m+[m[32m🚧 IN PROGRESS[m
 [m
 Version[m
 [m
[31m-[m
[31m-[m
[31m-\*\*v0.1.0-alpha\*\*[m
[31m-[m
[31m-[m
[31m-[m
[32m+[m[32mv0.4.0-alpha[m
\ No newline at end of file[m
[1mdiff --git a/PROJECT_STATE.md b/PROJECT_STATE.md[m
[1mindex 975da5d..c91c938 100644[m
[1m--- a/PROJECT_STATE.md[m
[1m+++ b/PROJECT_STATE.md[m
[36m@@ -6,7 +6,23 @@[m
 [m
 [m
 [m
[31m-\*\*v0.1.0-alpha\*\*[m
[32m+[m[32m\*\*v0.4.0-alpha\*\*[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32m\---[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32m\## Current Status[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32m\*\*Phase 4.12 in Progress\*\*[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32mPlatform architecture is feature complete and undergoing final consolidation before Phase 5.[m
 [m
 [m
 [m
[36m@@ -22,17 +38,21 @@[m
 [m
 [m
 [m
[31m-\* JAOS Kernel[m
[32m+[m[32m\- JAOS Kernel[m
[32m+[m
[32m+[m[32m\- Executive Brain[m
[32m+[m
[32m+[m[32m\- Core Models[m
[32m+[m
[32m+[m[32m\- Registries[m
 [m
[31m-\* Executive Brain[m
[32m+[m[32m\- Managers[m
 [m
[31m-\* Models[m
[32m+[m[32m\- Initial Executive Pipeline[m
 [m
[31m-\* Registries[m
 [m
[31m-\* Managers[m
 [m
[31m-\* Executive Pipeline[m
[32m+[m[32m\---[m
 [m
 [m
 [m
[36m@@ -40,71 +60,165 @@[m
 [m
 [m
 [m
[31m-\* Working Memory[m
[32m+[m[32m\- Working Memory[m
[32m+[m
[32m+[m[32m\- Memory Registry[m
[32m+[m
[32m+[m[32m\- Memory Manager[m
[32m+[m
[32m+[m[32m\- Executive Brain ↔ Memory Integration[m
[32m+[m
[32m+[m[32m\- Integration Tests[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32m\---[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32m\### ✅ Phase 3 — AI Foundation[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32m\- AI Provider Interface[m
[32m+[m
[32m+[m[32m\- AI Provider Manager[m
[32m+[m
[32m+[m[32m\- Prompt Engine[m
[32m+[m
[32m+[m[32m\- Configuration Layer[m
[32m+[m
[32m+[m[32m\- Ollama Provider[m
[32m+[m
[32m+[m[32m\- OpenAI Provider[m
[32m+[m
[32m+[m[32m\- Multi-Provider Routing[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32m\---[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32m\### ✅ Phase 3.5 — Architecture Foundation[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32m\- Architecture Documentation[m
[32m+[m
[32m+[m[32m\- Engineering Documentation[m
[32m+[m
[32m+[m[32m\- Coding Standards[m
[32m+[m
[32m+[m[32m\- Dependency Rules[m
[32m+[m
[32m+[m[32m\- Runtime Contracts[m
[32m+[m
[32m+[m[32m\- Layer Model[m
[32m+[m
[32m+[m[32m\- Plugin Architecture[m
[32m+[m
[32m+[m[32m\- Provider Architecture[m
[32m+[m
[32m+[m[32m\- Security Architecture[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32m\---[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32m\### ✅ Phase 4.1 – Phase 4.11[m
[32m+[m
 [m
[31m-\* Memory Registry[m
 [m
[31m-\* Memory Manager[m
[32m+[m[32mCompleted:[m
 [m
[31m-\* Executive Brain ↔ Memory Integration[m
 [m
[31m-\* End-to-End Integration Tests[m
 [m
[32m+[m[32m\- Platform Runtime[m
 [m
[32m+[m[32m\- Service Container[m
 [m
[31m-\### ✅ Phase 3 — AI Layer[m
[32m+[m[32m\- Runtime Context[m
 [m
[32m+[m[32m\- Event Bus[m
 [m
[32m+[m[32m\- Base Platform Service[m
 [m
[31m-Completed Milestones[m
[32m+[m[32m\- Runtime-managed Services[m
 [m
[32m+[m[32m\- Executive Brain Integration[m
 [m
[32m+[m[32m\- Memory Integration[m
 [m
[31m-\* JAOS-M-0023 — AI Provider Interface[m
[32m+[m[32m\- Workflow Integration[m
 [m
[31m-\* JAOS-M-0024 — AI Provider Manager[m
[32m+[m[32m\- Security Integration[m
 [m
[31m-\* JAOS-M-0025 — Prompt Engine[m
[32m+[m[32m\- Knowledge Integration[m
 [m
[31m-\* JAOS-M-0025.1 — Configuration Layer[m
[32m+[m[32m\- Infrastructure Integration[m
 [m
[31m-\* JAOS-M-0026 — Ollama Integration[m
[32m+[m[32m\- Communication Integration[m
 [m
[31m-\* JAOS-M-0027 — OpenAI Integration[m
[32m+[m[32m\- PC Control Integration[m
 [m
[31m-\* JAOS-M-0028 — Multi-LLM Routing[m
[32m+[m[32m\- Dashboard Integration[m
 [m
[32m+[m[32m\- Development Integration[m
 [m
[32m+[m[32m\- Engineering Integration[m
 [m
[31m-Architecture[m
[32m+[m[32m\- System Services Integration[m
 [m
 [m
 [m
[31m-\* Provider-independent AI Layer[m
[32m+[m[32m\---[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32m\### 🚧 Phase 4.12[m
[32m+[m
[32m+[m
 [m
[31m-\* Prompt Engine[m
[32m+[m[32mCompleted[m
 [m
[31m-\* AI Provider Manager[m
 [m
[31m-\* Ollama Provider[m
 [m
[31m-\* OpenAI Provider[m
[32m+[m[32m\- Boot Manager[m
 [m
[31m-\* LLM Router[m
[32m+[m[32m\- Runtime Validator[m
 [m
[31m-\* Centralized AI Configuration[m
[32m+[m[32m\- Startup Validator[m
 [m
[32m+[m[32m\- Executive Pipeline[m
 [m
[32m+[m[32m\- Dependency Validator[m
 [m
[31m-Test Status[m
[32m+[m[32m\- Runtime Health Certification[m
 [m
[32m+[m[32m\- Unified Boot Sequence[m
 [m
 [m
[31m-\*\*204 / 204 Tests Passing\*\*[m
 [m
[32m+[m[32mPending[m
 [m
 [m
[31m-Project Status[m
[32m+[m
[32m+[m[32m\- Documentation Freeze[m
[32m+[m
[32m+[m[32m\- Architecture Freeze[m
[32m+[m
[32m+[m[32m\- Platform Certification[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32m\---[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32m\## Architecture Status[m
 [m
 [m
 [m
[36m@@ -112,11 +226,17 @@[m [mProject Status[m
 [m
 [m
 [m
[31m-Next Phase[m
[32m+[m[32mArchitecture Freeze pending.[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32m\---[m
[32m+[m
 [m
 [m
[32m+[m[32m\## Next Phase[m
 [m
[31m-🚀 Phase 4 — Tool Layer[m
 [m
 [m
[32m+[m[32m\*\*Phase 5 — AI Execution Engine\*\*[m
 [m
[1mdiff --git a/ROADMAP.md b/ROADMAP.md[m
[1mindex 582074d..68b5b4f 100644[m
[1m--- a/ROADMAP.md[m
[1m+++ b/ROADMAP.md[m
[36m@@ -1,78 +1,230 @@[m
[31m-\## 🚀 Phase 3 — AI Layer ✅ COMPLETE[m
[32m+[m[32m\# JAOS Roadmap[m
 [m
 [m
 [m
[31m-\### AI Provider Abstraction[m
[32m+[m[32m\## ✅ Phase 1[m
 [m
 [m
 [m
[31m-\* ✅ AI Provider Interface[m
[32m+[m[32mExecutive Brain Foundation[m
 [m
[31m-\* ✅ AI Provider Models[m
 [m
[31m-\* ✅ AI Provider Exceptions[m
 [m
[31m-\* ✅ AI Provider Manager[m
[32m+[m[32mStatus: COMPLETE[m
 [m
 [m
 [m
[31m-\### Prompt System[m
[32m+[m[32m\---[m
 [m
 [m
 [m
[31m-\* ✅ Prompt Models[m
[32m+[m[32m\## ✅ Phase 2[m
 [m
[31m-\* ✅ Prompt Engine[m
 [m
[31m-\* ✅ Prompt Validation[m
 [m
[31m-\* ✅ Prompt Builder[m
[32m+[m[32mMemory Foundation[m
 [m
 [m
 [m
[31m-\### Configuration[m
[32m+[m[32mStatus: COMPLETE[m
 [m
 [m
 [m
[31m-\* ✅ Centralized AI Configuration[m
[32m+[m[32m\---[m
 [m
 [m
 [m
[31m-\### AI Providers[m
[32m+[m[32m\## ✅ Phase 3[m
 [m
 [m
 [m
[31m-\* ✅ Ollama[m
[32m+[m[32mAI Foundation[m
 [m
[31m-\* ✅ OpenAI[m
 [m
 [m
[32m+[m[32mStatus: COMPLETE[m
 [m
[31m-\### Multi-Provider[m
 [m
 [m
[32m+[m[32m\---[m
 [m
[31m-\* ✅ Provider Routing[m
 [m
[31m-\* ✅ Default Provider Routing[m
 [m
[31m-\* ✅ Manual Provider Selection[m
[32m+[m[32m\## ✅ Phase 3.5[m
 [m
 [m
 [m
[31m-\### Testing[m
[32m+[m[32mArchitecture \& Engineering Foundation[m
 [m
 [m
 [m
[31m-\* ✅ Provider Tests[m
[32m+[m[32mStatus: COMPLETE[m
 [m
[31m-\* ✅ Prompt Tests[m
 [m
[31m-\* ✅ Routing Tests[m
 [m
[32m+[m[32m\---[m
 [m
 [m
[31m-\*\*Phase Status: COMPLETE\*\*[m
 [m
[32m+[m[32m\## 🚧 Phase 4[m
 [m
 [m
[32m+[m
[32m+[m[32mPlatform Runtime[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32mCompleted[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32m\- Runtime[m
[32m+[m
[32m+[m[32m\- Boot System[m
[32m+[m
[32m+[m[32m\- Runtime Validation[m
[32m+[m
[32m+[m[32m\- Startup Validation[m
[32m+[m
[32m+[m[32m\- Dependency Validation[m
[32m+[m
[32m+[m[32m\- Executive Pipeline[m
[32m+[m
[32m+[m[32m\- Runtime Health[m
[32m+[m
[32m+[m[32m\- Service Integration[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32mPending[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32m\- Documentation Freeze[m
[32m+[m
[32m+[m[32m\- Architecture Freeze[m
[32m+[m
[32m+[m[32m\- Platform Certification[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32mStatus: IN PROGRESS[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32m\---[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32m\## Phase 5[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32mAI Execution Engine[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32mPlanned[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32m\- Multi-Provider Execution[m
[32m+[m
[32m+[m[32m\- Dynamic Routing[m
[32m+[m
[32m+[m[32m\- Task Planning[m
[32m+[m
[32m+[m[32m\- Reasoning Engine[m
[32m+[m
[32m+[m[32m\- Provider Selection[m
[32m+[m
[32m+[m[32m\- Execution Orchestrator[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32mStatus: NOT STARTED[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32m\---[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32m\## Phase 6[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32mMulti-Agent System[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32mStatus: Planned[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32m\---[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32m\## Phase 7[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32mVoice System[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32mStatus: Planned[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32m\---[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32m\## Phase 8[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32mVision System[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32mStatus: Planned[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32m\---[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32m\## Phase 9[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32mDesktop Automation[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32mStatus: Planned[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32m\---[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32m\## Phase 10+[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32mLearning[m
[32m+[m
[32m+[m[32mMobile[m
[32m+[m
[32m+[m[32mCloud[m
[32m+[m
[32m+[m[32mSelf Improvement[m
[32m+[m
[32m+[m[32mBusiness Platform[m
[32m+[m
[1mdiff --git a/communication/communication_hub.py b/communication/communication_hub.py[m
[1mindex 212333b..65bb8f3 100644[m
[1m--- a/communication/communication_hub.py[m
[1m+++ b/communication/communication_hub.py[m
[36m@@ -1,53 +1,46 @@[m
[32m+[m[32mfrom jaos_platform.base_platform_service import BasePlatformService[m
 from logs.logger import logger[m
 [m
 [m
[31m-class CommunicationHub:[m
[32m+[m[32mclass CommunicationHub(BasePlatformService):[m
[32m+[m[32m    """Runtime-managed communication hub service."""[m
 [m
[31m-    def __init__(self):[m
[32m+[m[32m    SERVICE_NAME = "communication_hub"[m
 [m
[32m+[m[32m    def __init__(self, runtime=None):[m
         self.events = [][m
 [m
[31m-    def add_event([m
[31m-            self,[m
[31m-            source,[m
[31m-            category,[m
[31m-            message):[m
[32m+[m[32m        super().__init__(runtime)[m
 [m
[32m+[m[32m    def add_event(self, source, category, message):[m
         self.events.append([m
             {[m
                 "source": source,[m
                 "category": category,[m
[31m-                "message": message[m
[32m+[m[32m                "message": message,[m
             }[m
         )[m
 [m
[31m-        logger.info([m
[31m-            f"Communication event: {source}"[m
[31m-        )[m
[32m+[m[32m        logger.info(f"Communication event: {source}")[m
 [m
[31m-    def show_events(self):[m
[32m+[m[32m        if self.runtime is not None:[m
[32m+[m[32m            self.runtime.events.publish([m
[32m+[m[32m                "communication_event_added",[m
[32m+[m[32m                {[m
[32m+[m[32m                    "source": source,[m
[32m+[m[32m                    "category": category,[m
[32m+[m[32m                    "message": message,[m
[32m+[m[32m                },[m
[32m+[m[32m            )[m
 [m
[31m-        print([m
[31m-            "\n=== Communication Hub ===\n"[m
[31m-        )[m
[32m+[m[32m    def show_events(self):[m
[32m+[m[32m        print("\n=== Communication Hub ===\n")[m
 [m
         if not self.events:[m
[31m-[m
[31m-            print([m
[31m-                "No communication events."[m
[31m-            )[m
[31m-[m
[32m+[m[32m            print("No communication events.")[m
             return[m
 [m
         for event in self.events:[m
[31m-[m
[31m-            print([m
[31m-                f"[{event['source']}] "[m
[31m-                f"{event['category']}"[m
[31m-            )[m
[31m-[m
[31m-            print([m
[31m-                f"  {event['message']}"[m
[31m-            )[m
[31m-[m
[32m+[m[32m            print(f"[{event['source']}] {event['category']}")[m
[32m+[m[32m            print(f"  {event['message']}")[m
             print()[m
\ No newline at end of file[m
[1mdiff --git a/core/engine.py b/core/engine.py[m
[1mindex f05c6e8..a2942d4 100644[m
[1m--- a/core/engine.py[m
[1m+++ b/core/engine.py[m
[36m@@ -13,151 +13,105 @@[m [mfrom core.config_manager import ConfigManager[m
 from core.command_system import CommandSystem[m
 from core.version_manager import VersionManager[m
 from tests.test_runner import TestRunner[m
[32m+[m[32mfrom jaos_platform.platform_runtime import PlatformRuntime[m
 [m
 [m
 class JarvisEngine:[m
 [m
[31m-    def __init__(self):[m
[32m+[m[32m    def __init__(self, runtime: PlatformRuntime | None = None):[m
 [m
         logger.info("Engine initialized")[m
 [m
[31m-        self.module_loader = ModuleLoader()[m
[32m+[m[32m        self.runtime = runtime or PlatformRuntime()[m
 [m
[32m+[m[32m        self.module_loader = ModuleLoader()[m
         self.event_system = EventSystem()[m
[31m-[m
         self.plugin_manager = PluginManager()[m
[31m-[m
         self.status_manager = StatusManager()[m
[31m-[m
         self.config = ConfigManager.load_config()[m
 [m
[32m+[m[32m        self.runtime.container.register("jarvis_engine", self)[m
[32m+[m[32m        self.runtime.context.set("engine_status", "INITIALIZED")[m
[32m+[m[32m        self.runtime.events.publish([m
[32m+[m[32m            "engine_initialized",[m
[32m+[m[32m            {"status": "INITIALIZED"}[m
[32m+[m[32m        )[m
[32m+[m
     def start(self):[m
 [m
         try:[m
 [m
             logger.info("Engine started")[m
 [m
[31m-            ActionHistory.record_action([m
[31m-                "Engine started"[m
[31m-            )[m
[32m+[m[32m            ActionHistory.record_action("Engine started")[m
 [m
[31m-            print([m
[31m-                f"{self.config['jarvis_name']} is online."[m
[31m-            )[m
[31m-[m
[31m-            self.module_loader.load_module([m
[31m-                "Logger"[m
[31m-            )[m
[31m-[m
[31m-            ActionHistory.record_action([m
[31m-                "Logger module loaded"[m
[31m-            )[m
[32m+[m[32m            print(f"{self.config['jarvis_name']} is online.")[m
 [m
[32m+[m[32m            self.module_loader.load_module("Logger")[m
[32m+[m[32m            ActionHistory.record_action("Logger module loaded")[m
             self.module_loader.show_modules()[m
 [m
[31m-            self.event_system.emit([m
[31m-                "system_started"[m
[31m-            )[m
[31m-[m
[31m-            ActionHistory.record_action([m
[31m-                "system_started event emitted"[m
[31m-            )[m
[31m-[m
[32m+[m[32m            self.event_system.emit("system_started")[m
[32m+[m[32m            ActionHistory.record_action("system_started event emitted")[m
             self.event_system.show_events()[m
 [m
             self.plugin_manager.load_plugins()[m
[31m-[m
             self.plugin_manager.show_plugins()[m
[31m-[m
[31m-            ActionHistory.record_action([m
[31m-                "Plugins loaded"[m
[31m-            )[m
[32m+[m[32m            ActionHistory.record_action("Plugins loaded")[m
 [m
             TestRunner.run_tests()[m
[31m-[m
[31m-            ActionHistory.record_action([m
[31m-                "System tests completed"[m
[31m-            )[m
[32m+[m[32m            ActionHistory.record_action("System tests completed")[m
 [m
             health = HealthMonitor.get_system_health()[m
 [m
             print("\nSystem Health:")[m
 [m
             for key, value in health.items():[m
[31m-[m
                 print(f"{key}: {value}%")[m
 [m
             diagnostics = Diagnostics.run_diagnostics([m
[31m-[m
                 self.module_loader.modules,[m
[31m-[m
                 self.event_system.events,[m
[31m-[m
                 self.plugin_manager.plugins,[m
[31m-[m
                 health[m
[31m-[m
             )[m
 [m
             print("\nDiagnostics Report:\n")[m
 [m
             for key, value in diagnostics.items():[m
[31m-[m
                 print(f"{key}: {value}")[m
 [m
             self.status_manager.show_status()[m
[31m-[m
             VersionManager.show_version()[m
 [m
[31m-            ActionHistory.record_action([m
[31m-                "Version information displayed"[m
[31m-            )[m
[32m+[m[32m            ActionHistory.record_action("Version information displayed")[m
 [m
             previous_state = RecoveryManager.recover_latest_snapshot()[m
 [m
             if previous_state:[m
[31m-[m
                 print("\nRecovered Previous State:")[m
[31m-[m
                 print(previous_state)[m
 [m
             SnapshotManager.create_snapshot([m
[31m-[m
                 {[m
[31m-[m
                     "status": self.status_manager.get_status(),[m
[31m-[m
                     "modules": self.module_loader.modules,[m
[31m-[m
                     "events": self.event_system.events,[m
[31m-[m
                     "plugins": self.plugin_manager.plugins,[m
[31m-[m
                     "health": health,[m
[31m-[m
                     "diagnostics": diagnostics,[m
[31m-[m
                     "config": self.config[m
[31m-[m
                 }[m
[31m-[m
             )[m
 [m
             SnapshotManager.create_snapshot([m
[31m-[m
                 {[m
[31m-[m
                     "milestone": "PHASE_1_COMPLETE",[m
[31m-[m
                     "version": "0.1"[m
[31m-[m
                 }[m
[31m-[m
             )[m
 [m
[31m-            ActionHistory.record_action([m
[31m-                "Snapshot created"[m
[31m-            )[m
[32m+[m[32m            ActionHistory.record_action("Snapshot created")[m
 [m
             print("\nInteractive Console Started")[m
 [m
[36m@@ -169,16 +123,11 @@[m [mclass JarvisEngine:[m
 [m
                 print("JARVIS:", response)[m
 [m
[31m-                ActionHistory.record_action([m
[31m-                    f"Command: {command}"[m
[31m-                )[m
[32m+[m[32m                ActionHistory.record_action(f"Command: {command}")[m
 [m
                 if command.lower() == "exit":[m
[31m-[m
                     break[m
 [m
         except Exception as error:[m
 [m
[31m-            ErrorHandler.handle_error([m
[31m-                error[m
[31m-            )[m
\ No newline at end of file[m
[32m+[m[32m            ErrorHandler.handle_error(error)[m
\ No newline at end of file[m
[1mdiff --git a/dashboard/mission_control.py b/dashboard/mission_control.py[m
[1mindex ddced89..b392070 100644[m
[1m--- a/dashboard/mission_control.py[m
[1m+++ b/dashboard/mission_control.py[m
[36m@@ -1,32 +1,32 @@[m
[32m+[m[32mfrom jaos_platform.base_platform_service import BasePlatformService[m
 from logs.logger import logger[m
 [m
 [m
[31m-class MissionControl:[m
[32m+[m[32mclass MissionControl(BasePlatformService):[m
[32m+[m[32m    """Runtime-managed JAOS mission control dashboard service."""[m
 [m
[31m-    def __init__(self):[m
[32m+[m[32m    SERVICE_NAME = "mission_control"[m
 [m
[32m+[m[32m    def __init__(self, runtime=None):[m
         self.version = "JAOS v1 Alpha"[m
[31m-[m
         self.status = "ONLINE"[m
[31m-[m
         self.platforms = 15[m
[31m-[m
         self.user = "Vinay"[m
 [m
[31m-    def show_dashboard(self):[m
[32m+[m[32m        super().__init__(runtime)[m
 [m
[32m+[m[32m    def show_dashboard(self):[m
         print("\n========== JAOS MISSION CONTROL ==========\n")[m
[31m-[m
         print(f"Version   : {self.version}")[m
[31m-[m
         print(f"Status    : {self.status}")[m
[31m-[m
         print(f"Platforms : {self.platforms}")[m
[31m-[m
         print(f"User      : {self.user}")[m
[31m-[m
         print("\n==========================================\n")[m
 [m
[31m-        logger.info([m
[31m-            "Mission Control displayed."[m
[31m-        )[m
\ No newline at end of file[m
[32m+[m[32m        logger.info("Mission Control displayed.")[m
[32m+[m
[32m+[m[32m        if self.runtime is not None:[m
[32m+[m[32m            self.runtime.events.publish([m
[32m+[m[32m                "mission_control_displayed",[m
[32m+[m[32m                {"status": self.status},[m
[32m+[m[32m            )[m
\ No newline at end of file[m
[1mdiff --git a/development/development_workspace_manager.py b/development/development_workspace_manager.py[m
[1mindex cab7ebe..b76b22d 100644[m
[1m--- a/development/development_workspace_manager.py[m
[1m+++ b/development/development_workspace_manager.py[m
[36m@@ -1,38 +1,50 @@[m
[32m+[m[32mfrom jaos_platform.base_platform_service import BasePlatformService[m
 from logs.logger import logger[m
 [m
 [m
[31m-class DevelopmentWorkspaceManager:[m
[32m+[m[32mclass DevelopmentWorkspaceManager(BasePlatformService):[m
[32m+[m[32m    """Runtime-managed development workspace service."""[m
 [m
[31m-    def __init__(self):[m
[32m+[m[32m    SERVICE_NAME = "development_workspace_manager"[m
 [m
[32m+[m[32m    def __init__(self, runtime=None):[m
         self.workspaces = {}[m
 [m
[31m-    def register_workspace([m
[31m-            self,[m
[31m-            name,[m
[31m-            repository,[m
[31m-            vscode_workspace):[m
[32m+[m[32m        super().__init__(runtime)[m
 [m
[32m+[m[32m    def register_workspace([m
[32m+[m[32m        self,[m
[32m+[m[32m        name,[m
[32m+[m[32m        repository,[m
[32m+[m[32m        vscode_workspace,[m
[32m+[m[32m    ):[m
         self.workspaces[name] = {[m
             "repository": repository,[m
[31m-            "vscode_workspace": vscode_workspace[m
[32m+[m[32m            "vscode_workspace": vscode_workspace,[m
         }[m
 [m
         logger.info([m
             f"Development workspace registered: {name}"[m
         )[m
 [m
[31m-    def show_workspaces(self):[m
[32m+[m[32m        if self.runtime is not None:[m
[32m+[m[32m            self.runtime.events.publish([m
[32m+[m[32m                "development_workspace_registered",[m
[32m+[m[32m                {[m
[32m+[m[32m                    "name": name,[m
[32m+[m[32m                    "repository": repository,[m
[32m+[m[32m                    "vscode_workspace": vscode_workspace,[m
[32m+[m[32m                },[m
[32m+[m[32m            )[m
 [m
[32m+[m[32m    def show_workspaces(self):[m
         print("\n=== Development Workspace Manager ===\n")[m
 [m
         if not self.workspaces:[m
[31m-[m
             print("No development workspaces.")[m
             return[m
 [m
         for name, data in self.workspaces.items():[m
[31m-[m
             print(name)[m
             print(f"  Repository : {data['repository']}")[m
             print(f"  VS Code    : {data['vscode_workspace']}")[m
[1mdiff --git a/engineering/platform_health_dashboard.py b/engineering/platform_health_dashboard.py[m
[1mindex d25f9e3..0d8f599 100644[m
[1m--- a/engineering/platform_health_dashboard.py[m
[1m+++ b/engineering/platform_health_dashboard.py[m
[36m@@ -1,62 +1,63 @@[m
[31m-from logs.logger import logger[m
 from datetime import datetime[m
 [m
[32m+[m[32mfrom jaos_platform.base_platform_service import BasePlatformService[m
[32m+[m[32mfrom logs.logger import logger[m
[32m+[m
 [m
[31m-class PlatformHealthDashboard:[m
[32m+[m[32mclass PlatformHealthDashboard(BasePlatformService):[m
[32m+[m[32m    """Runtime-managed engineering platform health service."""[m
 [m
[31m-    def __init__(self):[m
[32m+[m[32m    SERVICE_NAME = "platform_health_dashboard"[m
 [m
[32m+[m[32m    def __init__(self, runtime=None):[m
         self.platforms = {}[m
 [m
[31m-    def update_platform([m
[31m-            self,[m
[31m-            name,[m
[31m-            health,[m
[31m-            passed,[m
[31m-            failed,[m
[31m-            certified=False):[m
[32m+[m[32m        super().__init__(runtime)[m
 [m
[32m+[m[32m    def update_platform([m
[32m+[m[32m        self,[m
[32m+[m[32m        name,[m
[32m+[m[32m        health,[m
[32m+[m[32m        passed,[m
[32m+[m[32m        failed,[m
[32m+[m[32m        certified=False,[m
[32m+[m[32m    ):[m
         self.platforms[name] = {[m
[31m-[m
             "health": health,[m
[31m-[m
             "passed": passed,[m
[31m-[m
             "failed": failed,[m
[31m-[m
             "certified": certified,[m
[31m-[m
             "last_validation": datetime.now().strftime([m
                 "%Y-%m-%d %H:%M:%S"[m
[31m-            )[m
[31m-[m
[32m+[m[32m            ),[m
         }[m
 [m
[31m-        logger.info([m
[31m-            f"Health updated: {name}"[m
[31m-        )[m
[32m+[m[32m        logger.info(f"Health updated: {name}")[m
[32m+[m
[32m+[m[32m        if self.runtime is not None:[m
[32m+[m[32m            self.runtime.events.publish([m
[32m+[m[32m                "platform_health_updated",[m
[32m+[m[32m                {[m
[32m+[m[32m                    "platform": name,[m
[32m+[m[32m                    "health": health,[m
[32m+[m[32m                    "passed": passed,[m
[32m+[m[32m                    "failed": failed,[m
[32m+[m[32m                    "certified": certified,[m
[32m+[m[32m                },[m
[32m+[m[32m            )[m
 [m
     def show_dashboard(self):[m
[31m-[m
         print("\n========== PLATFORM HEALTH ==========\n")[m
 [m
         if not self.platforms:[m
[31m-[m
             print("No platform health data.")[m
             return[m
 [m
         for name, data in self.platforms.items():[m
[31m-[m
             print(name)[m
[31m-[m
             print(f"  Health           : {data['health']}")[m
[31m-[m
             print(f"  Tests Passed     : {data['passed']}")[m
[31m-[m
             print(f"  Tests Failed     : {data['failed']}")[m
[31m-[m
             print(f"  Certified        : {data['certified']}")[m
[31m-[m
             print(f"  Last Validation  : {data['last_validation']}")[m
[31m-[m
             print()[m
\ No newline at end of file[m
[1mdiff --git a/executive_brain/brain/executive_brain.py b/executive_brain/brain/executive_brain.py[m
[1mindex c8e4113..1055ce3 100644[m
[1m--- a/executive_brain/brain/executive_brain.py[m
[1m+++ b/executive_brain/brain/executive_brain.py[m
[36m@@ -10,6 +10,7 @@[m [mResponsibilities:[m
     - Maintain working memory[m
     - Report executive health[m
     - Provide a single entry point for orchestration[m
[32m+[m[32m    - Integrate with the JAOS Platform Runtime[m
 [m
 Non-Responsibilities:[m
     - AI reasoning[m
[36m@@ -17,6 +18,8 @@[m [mNon-Responsibilities:[m
     - Real tool execution[m
 """[m
 [m
[32m+[m[32mfrom jaos_platform.platform_runtime import PlatformRuntime[m
[32m+[m
 from executive_brain.managers.registry_manager import RegistryManager[m
 from executive_brain.managers.planning_manager import PlanningManager[m
 from executive_brain.managers.decision_manager import DecisionManager[m
[36m@@ -31,9 +34,17 @@[m [mclass ExecutiveBrain:[m
 [m
     VERSION = "0.5.0-dev"[m
 [m
[31m-    def __init__(self):[m
[32m+[m[32m    def __init__(self, runtime: PlatformRuntime | None = None):[m
[32m+[m[32m        self.runtime = runtime or PlatformRuntime()[m
[32m+[m
         self.registry_manager = RegistryManager()[m
[31m-        self.memory_manager = MemoryManager()[m
[32m+[m
[32m+[m[32m        if self.runtime.container.is_registered("memory_manager"):[m
[32m+[m[32m            self.memory_manager = self.runtime.container.resolve([m
[32m+[m[32m                "memory_manager"[m
[32m+[m[32m            )[m
[32m+[m[32m        else:[m
[32m+[m[32m            self.memory_manager = MemoryManager(self.runtime)[m
 [m
         self.planning_manager = PlanningManager(self.registry_manager)[m
         self.decision_manager = DecisionManager(self.registry_manager)[m
[36m@@ -43,6 +54,13 @@[m [mclass ExecutiveBrain:[m
 [m
         self.status = "INITIALIZED"[m
 [m
[32m+[m[32m        self.runtime.container.register("executive_brain", self)[m
[32m+[m[32m        self.runtime.context.set("executive_brain_status", self.status)[m
[32m+[m[32m        self.runtime.events.publish([m
[32m+[m[32m            "executive_brain_initialized",[m
[32m+[m[32m            {"status": self.status},[m
[32m+[m[32m        )[m
[32m+[m
     def initialize(self):[m
         self.planning_manager.initialize()[m
         self.decision_manager.initialize()[m
[36m@@ -51,6 +69,13 @@[m [mclass ExecutiveBrain:[m
         self.result_manager.initialize()[m
 [m
         self.status = "READY"[m
[32m+[m
[32m+[m[32m        self.runtime.context.set("executive_brain_status", self.status)[m
[32m+[m[32m        self.runtime.events.publish([m
[32m+[m[32m            "executive_brain_ready",[m
[32m+[m[32m            {"status": self.status},[m
[32m+[m[32m        )[m
[32m+[m
         return True[m
 [m
     def get_status(self):[m
[1mdiff --git a/executive_brain/memory/memory_manager.py b/executive_brain/memory/memory_manager.py[m
[1mindex 54694e0..a9adb2b 100644[m
[1m--- a/executive_brain/memory/memory_manager.py[m
[1m+++ b/executive_brain/memory/memory_manager.py[m
[36m@@ -9,6 +9,7 @@[m [mResponsibilities:[m
     - Update working memory[m
     - Clear working memory[m
     - Provide access to current working memory[m
[32m+[m[32m    - Integrate with JAOS Platform Runtime[m
 [m
 Non-Responsibilities:[m
     - Long-term memory[m
[36m@@ -16,15 +17,22 @@[m [mNon-Responsibilities:[m
     - Memory ranking[m
 """[m
 [m
[32m+[m[32mfrom jaos_platform.base_platform_service import BasePlatformService[m
[32m+[m
 from executive_brain.memory.working_memory import WorkingMemory[m
 from executive_brain.memory.memory_registry import MemoryRegistry[m
 [m
 [m
[31m-class MemoryManager:[m
[32m+[m[32mclass MemoryManager(BasePlatformService):[m
     """Manager responsible for WorkingMemory."""[m
 [m
[31m-    def __init__(self):[m
[32m+[m[32m    SERVICE_NAME = "memory_manager"[m
[32m+[m
[32m+[m[32m    def __init__(self, runtime=None):[m
         self.registry = MemoryRegistry()[m
[32m+[m
[32m+[m[32m        super().__init__(runtime)[m
[32m+[m
         self.initialize()[m
 [m
     def initialize(self):[m
[36m@@ -37,9 +45,23 @@[m [mclass MemoryManager:[m
     def clear(self):[m
         self.get_memory().clear()[m
 [m
[32m+[m[32m        if self.runtime is not None:[m
[32m+[m[32m            self.runtime.events.publish([m
[32m+[m[32m                "memory_cleared",[m
[32m+[m[32m                {},[m
[32m+[m[32m            )[m
[32m+[m
     def set_user_request(self, request: str):[m
         self.get_memory().set_user_request(request)[m
 [m
[32m+[m[32m        if self.runtime is not None:[m
[32m+[m[32m            self.runtime.events.publish([m
[32m+[m[32m                "memory_user_request_set",[m
[32m+[m[32m                {[m
[32m+[m[32m                    "request": request,[m
[32m+[m[32m                },[m
[32m+[m[32m            )[m
[32m+[m
     def set_mission(self, mission_id: str):[m
         self.get_memory().set_mission(mission_id)[m
 [m
[1mdiff --git a/infrastructure/ai_provider_manager.py b/infrastructure/ai_provider_manager.py[m
[1mindex 6a6fca1..b14629f 100644[m
[1m--- a/infrastructure/ai_provider_manager.py[m
[1m+++ b/infrastructure/ai_provider_manager.py[m
[36m@@ -1,51 +1,40 @@[m
[32m+[m[32mfrom jaos_platform.base_platform_service import BasePlatformService[m
 from logs.logger import logger[m
 [m
 [m
[31m-class AIProviderManager:[m
[32m+[m[32mclass AIProviderManager(BasePlatformService):[m
[32m+[m[32m    """Runtime-managed AI provider manager."""[m
 [m
[31m-    def __init__(self):[m
[32m+[m[32m    SERVICE_NAME = "ai_provider_manager"[m
 [m
[32m+[m[32m    def __init__(self, runtime=None):[m
         self.providers = {}[m
 [m
[31m-    def register_provider([m
[31m-            self,[m
[31m-            name,[m
[31m-            status):[m
[32m+[m[32m        super().__init__(runtime)[m
 [m
[31m-        self.providers[[m
[31m-            name[m
[31m-        ] = status[m
[32m+[m[32m    def register_provider(self, name, status):[m
[32m+[m[32m        self.providers[name] = status[m
 [m
[31m-        logger.info([m
[31m-            f"AI Provider Registered: {name}"[m
[31m-        )[m
[32m+[m[32m        logger.info(f"AI Provider Registered: {name}")[m
 [m
[31m-    def provider_status([m
[31m-            self,[m
[31m-            name):[m
[32m+[m[32m        if self.runtime is not None:[m
[32m+[m[32m            self.runtime.events.publish([m
[32m+[m[32m                "ai_provider_registered",[m
[32m+[m[32m                {[m
[32m+[m[32m                    "name": name,[m
[32m+[m[32m                    "status": status,[m
[32m+[m[32m                },[m
[32m+[m[32m            )[m
 [m
[31m-        return self.providers.get([m
[31m-            name,[m
[31m-            "UNKNOWN"[m
[31m-        )[m
[32m+[m[32m    def provider_status(self, name):[m
[32m+[m[32m        return self.providers.get(name, "UNKNOWN")[m
 [m
     def show_providers(self):[m
[31m-[m
[31m-        print([m
[31m-            "\nAI Providers\n"[m
[31m-        )[m
[32m+[m[32m        print("\nAI Providers\n")[m
 [m
         if not self.providers:[m
[31m-[m
[31m-            print([m
[31m-                "No providers registered."[m
[31m-            )[m
[31m-[m
[32m+[m[32m            print("No providers registered.")[m
             return[m
 [m
[31m-        for provider, status in ([m
[31m-                self.providers.items()):[m
[31m-[m
[31m-            print([m
[31m-                f"{provider}: {status}"[m
[31m-            )[m
\ No newline at end of file[m
[32m+[m[32m        for provider, status in self.providers.items():[m
[32m+[m[32m            print(f"{provider}: {status}")[m
\ No newline at end of file[m
[1mdiff --git a/kernel/jaos_kernel.py b/kernel/jaos_kernel.py[m
[1mindex 26cb19d..7681503 100644[m
[1m--- a/kernel/jaos_kernel.py[m
[1m+++ b/kernel/jaos_kernel.py[m
[36m@@ -1,14 +1,22 @@[m
 from logs.logger import logger[m
[32m+[m[32mfrom jaos_platform.platform_runtime import PlatformRuntime[m
 [m
 [m
 class JAOSKernel:[m
 [m
     def __init__(self):[m
 [m
[32m+[m[32m        self.runtime = PlatformRuntime()[m
         self.platforms = {}[m
 [m
         self.status = "INITIALIZED"[m
 [m
[32m+[m[32m        self.register_platform([m
[32m+[m[32m            "platform_runtime",[m
[32m+[m[32m            self.runtime,[m
[32m+[m[32m            status="ACTIVE",[m
[32m+[m[32m        )[m
[32m+[m
     def register_platform([m
             self,[m
             name,[m
[36m@@ -27,6 +35,8 @@[m [mclass JAOSKernel:[m
     def start(self):[m
 [m
         self.status = "ONLINE"[m
[32m+[m[32m        self.runtime.context.set("kernel_status", self.status)[m
[32m+[m[32m        self.runtime.events.publish("kernel_started", {"status": self.status})[m
 [m
         logger.info([m
             "JAOS Kernel started."[m
[1mdiff --git a/knowledge/knowledge_base.py b/knowledge/knowledge_base.py[m
[1mindex 4c5229d..19e4e41 100644[m
[1m--- a/knowledge/knowledge_base.py[m
[1m+++ b/knowledge/knowledge_base.py[m
[36m@@ -1,34 +1,39 @@[m
[32m+[m[32mfrom jaos_platform.base_platform_service import BasePlatformService[m
 from logs.logger import logger[m
 [m
 [m
[31m-class KnowledgeBase:[m
[32m+[m[32mclass KnowledgeBase(BasePlatformService):[m
[32m+[m[32m    """Runtime-managed JAOS knowledge base service."""[m
 [m
[31m-    def __init__(self):[m
[32m+[m[32m    SERVICE_NAME = "knowledge_base"[m
 [m
[32m+[m[32m    def __init__(self, runtime=None):[m
         self.entries = {}[m
 [m
[31m-    def add_entry([m
[31m-            self,[m
[31m-            topic,[m
[31m-            content):[m
[32m+[m[32m        super().__init__(runtime)[m
 [m
[32m+[m[32m    def add_entry(self, topic, content):[m
         self.entries[topic] = content[m
 [m
[31m-        logger.info([m
[31m-            f"Knowledge entry added: {topic}"[m
[31m-        )[m
[32m+[m[32m        logger.info(f"Knowledge entry added: {topic}")[m
 [m
[31m-    def show_entries(self):[m
[32m+[m[32m        if self.runtime is not None:[m
[32m+[m[32m            self.runtime.events.publish([m
[32m+[m[32m                "knowledge_entry_added",[m
[32m+[m[32m                {[m
[32m+[m[32m                    "topic": topic,[m
[32m+[m[32m                    "content": content,[m
[32m+[m[32m                },[m
[32m+[m[32m            )[m
 [m
[32m+[m[32m    def show_entries(self):[m
         print("\n=== Knowledge Base ===\n")[m
 [m
         if not self.entries:[m
[31m-[m
             print("No knowledge entries.")[m
             return[m
 [m
         for topic, content in self.entries.items():[m
[31m-[m
             print(topic)[m
             print(f"  Content : {content}")[m
             print()[m
\ No newline at end of file[m
[1mdiff --git a/pc_control/application_manager.py b/pc_control/application_manager.py[m
[1mindex e976504..8042150 100644[m
[1m--- a/pc_control/application_manager.py[m
[1m+++ b/pc_control/application_manager.py[m
[36m@@ -1,38 +1,43 @@[m
[32m+[m[32mfrom jaos_platform.base_platform_service import BasePlatformService[m
 from logs.logger import logger[m
 [m
 [m
[31m-class ApplicationManager:[m
[32m+[m[32mclass ApplicationManager(BasePlatformService):[m
[32m+[m[32m    """Runtime-managed PC application manager service."""[m
 [m
[31m-    def __init__(self):[m
[32m+[m[32m    SERVICE_NAME = "application_manager"[m
 [m
[32m+[m[32m    def __init__(self, runtime=None):[m
         self.applications = {}[m
 [m
[31m-    def register_application([m
[31m-            self,[m
[31m-            name,[m
[31m-            executable,[m
[31m-            status="AVAILABLE"):[m
[32m+[m[32m        super().__init__(runtime)[m
 [m
[32m+[m[32m    def register_application(self, name, executable, status="AVAILABLE"):[m
         self.applications[name] = {[m
             "executable": executable,[m
[31m-            "status": status[m
[32m+[m[32m            "status": status,[m
         }[m
 [m
[31m-        logger.info([m
[31m-            f"Application registered: {name}"[m
[31m-        )[m
[32m+[m[32m        logger.info(f"Application registered: {name}")[m
 [m
[31m-    def show_applications(self):[m
[32m+[m[32m        if self.runtime is not None:[m
[32m+[m[32m            self.runtime.events.publish([m
[32m+[m[32m                "application_registered",[m
[32m+[m[32m                {[m
[32m+[m[32m                    "name": name,[m
[32m+[m[32m                    "executable": executable,[m
[32m+[m[32m                    "status": status,[m
[32m+[m[32m                },[m
[32m+[m[32m            )[m
 [m
[32m+[m[32m    def show_applications(self):[m
         print("\n=== Application Manager ===\n")[m
 [m
         if not self.applications:[m
[31m-[m
             print("No applications registered.")[m
             return[m
 [m
         for app, data in self.applications.items():[m
[31m-[m
             print(app)[m
             print(f"  Executable : {data['executable']}")[m
             print(f"  Status     : {data['status']}")[m
[1mdiff --git a/security/security_monitor.py b/security/security_monitor.py[m
[1mindex dab38fd..75f3c2c 100644[m
[1m--- a/security/security_monitor.py[m
[1m+++ b/security/security_monitor.py[m
[36m@@ -1,35 +1,40 @@[m
[32m+[m[32mfrom jaos_platform.base_platform_service import BasePlatformService[m
 from logs.logger import logger[m
 [m
 [m
[31m-class SecurityMonitor:[m
[32m+[m[32mclass SecurityMonitor(BasePlatformService):[m
[32m+[m[32m    """Runtime-managed security monitoring service."""[m
 [m
[31m-    def __init__(self):[m
[32m+[m[32m    SERVICE_NAME = "security_monitor"[m
 [m
[32m+[m[32m    def __init__(self, runtime=None):[m
         self.events = [][m
 [m
[31m-    def record_event([m
[31m-            self,[m
[31m-            level,[m
[31m-            description):[m
[32m+[m[32m        super().__init__(runtime)[m
 [m
[32m+[m[32m    def record_event(self, level, description):[m
         self.events.append({[m
             "level": level,[m
[31m-            "description": description[m
[32m+[m[32m            "description": description,[m
         })[m
 [m
[31m-        logger.info([m
[31m-            f"Security event: {level}"[m
[31m-        )[m
[32m+[m[32m        logger.info(f"Security event: {level}")[m
 [m
[31m-    def show_events(self):[m
[32m+[m[32m        if self.runtime is not None:[m
[32m+[m[32m            self.runtime.events.publish([m
[32m+[m[32m                "security_event_recorded",[m
[32m+[m[32m                {[m
[32m+[m[32m                    "level": level,[m
[32m+[m[32m                    "description": description,[m
[32m+[m[32m                },[m
[32m+[m[32m            )[m
 [m
[32m+[m[32m    def show_events(self):[m
         print("\n=== Security Monitor ===\n")[m
 [m
         if not self.events:[m
[31m-[m
             print("No security events.")[m
             return[m
 [m
         for event in self.events:[m
[31m-[m
             print(f"[{event['level']}] {event['description']}")[m
\ No newline at end of file[m
[1mdiff --git a/system_services/startup_manager.py b/system_services/startup_manager.py[m
[1mindex 5b08329..19794ea 100644[m
[1m--- a/system_services/startup_manager.py[m
[1m+++ b/system_services/startup_manager.py[m
[36m@@ -1,34 +1,45 @@[m
[32m+[m[32mfrom jaos_platform.base_platform_service import BasePlatformService[m
 from logs.logger import logger[m
 [m
 [m
[31m-class StartupManager:[m
[32m+[m[32mclass StartupManager(BasePlatformService):[m
[32m+[m[32m    """Runtime-managed startup service."""[m
 [m
[31m-    def __init__(self):[m
[32m+[m[32m    SERVICE_NAME = "startup_manager"[m
 [m
[32m+[m[32m    def __init__(self, runtime=None):[m
         self.services = {}[m
 [m
[31m-    def register_service([m
[31m-            self,[m
[31m-            name,[m
[31m-            enabled=True):[m
[32m+[m[32m        super().__init__(runtime)[m
 [m
[32m+[m[32m    def register_service([m
[32m+[m[32m        self,[m
[32m+[m[32m        name,[m
[32m+[m[32m        enabled=True,[m
[32m+[m[32m    ):[m
         self.services[name] = enabled[m
 [m
         logger.info([m
             f"Startup service registered: {name}"[m
         )[m
 [m
[31m-    def show_services(self):[m
[32m+[m[32m        if self.runtime is not None:[m
[32m+[m[32m            self.runtime.events.publish([m
[32m+[m[32m                "startup_service_registered",[m
[32m+[m[32m                {[m
[32m+[m[32m                    "service": name,[m
[32m+[m[32m                    "enabled": enabled,[m
[32m+[m[32m                },[m
[32m+[m[32m            )[m
 [m
[32m+[m[32m    def show_services(self):[m
         print("\n=== Startup Manager ===\n")[m
 [m
         if not self.services:[m
[31m-[m
             print("No startup services.")[m
             return[m
 [m
         for service, enabled in self.services.items():[m
[31m-[m
             print(service)[m
             print(f"  Enabled : {enabled}")[m
             print()[m
\ No newline at end of file[m
[1mdiff --git a/workflow/workflow_engine.py b/workflow/workflow_engine.py[m
[1mindex a0c3169..cb1d369 100644[m
[1m--- a/workflow/workflow_engine.py[m
[1m+++ b/workflow/workflow_engine.py[m
[36m@@ -1,43 +1,43 @@[m
[32m+[m[32mfrom jaos_platform.base_platform_service import BasePlatformService[m
 from logs.logger import logger[m
 [m
 [m
[31m-class WorkflowEngine:[m
[32m+[m[32mclass WorkflowEngine(BasePlatformService):[m
[32m+[m[32m    """Central workflow orchestration service."""[m
 [m
[31m-    def __init__(self):[m
[32m+[m[32m    SERVICE_NAME = "workflow_engine"[m
 [m
[32m+[m[32m    def __init__(self, runtime=None):[m
         self.workflows = {}[m
 [m
[31m-    def register_workflow([m
[31m-            self,[m
[31m-            workflow_name,[m
[31m-            status="READY"):[m
[32m+[m[32m        super().__init__(runtime)[m
 [m
[32m+[m[32m    def register_workflow(self, workflow_name, status="READY"):[m
         self.workflows[workflow_name] = status[m
 [m
[31m-        logger.info([m
[31m-            f"Workflow registered: {workflow_name}"[m
[31m-        )[m
[32m+[m[32m        logger.info(f"Workflow registered: {workflow_name}")[m
 [m
[31m-    def workflow_status([m
[31m-            self,[m
[31m-            workflow_name):[m
[32m+[m[32m        if self.runtime is not None:[m
[32m+[m[32m            self.runtime.events.publish([m
[32m+[m[32m                "workflow_registered",[m
[32m+[m[32m                {[m
[32m+[m[32m                    "workflow": workflow_name,[m
[32m+[m[32m                    "status": status,[m
[32m+[m[32m                },[m
[32m+[m[32m            )[m
 [m
[32m+[m[32m    def workflow_status(self, workflow_name):[m
         return self.workflows.get([m
             workflow_name,[m
[31m-            "UNKNOWN"[m
[32m+[m[32m            "UNKNOWN",[m
         )[m
 [m
     def show_workflows(self):[m
[31m-[m
         print("\n=== Workflow Engine ===\n")[m
 [m
         if not self.workflows:[m
[31m-[m
             print("No workflows registered.")[m
             return[m
 [m
         for workflow, status in self.workflows.items():[m
[31m-[m
[31m-            print([m
[31m-                f"{workflow}: {status}"[m
[31m-            )[m
\ No newline at end of file[m
[32m+[m[32m            print(f"{workflow}: {status}")[m
\ No newline at end of file[m
