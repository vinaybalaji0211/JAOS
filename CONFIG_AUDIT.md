\# JAOS Config Audit



\## Overall Status



Status:

🟡 Active / Needs Update



Priority:

HIGH



\## Files



| File | Role | Status |

|---|---|---|

| providers.json | Multi-provider registry | High value |

| settings.json | Runtime settings | Active |

| ai\_config.py | AI provider config | Active |

| config.py | Legacy project constants | Outdated |



\## Findings



\- providers.json already supports OpenAI, Ollama, Gemini, DeepSeek, Claude, Qwen, llama.cpp, Mistral, and Perplexity.

\- ai\_config.py currently defines Ollama and OpenAI configs.

\- settings.json defines current mode and selected provider.

\- config.py is outdated and must be updated later.



\## Final Decision



Do not delete.



Config should become the official centralized configuration layer for JAOS.

