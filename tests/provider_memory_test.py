from brain.provider_memory import ProviderMemory

ProviderMemory.record_result(
    "openai",
    "coding",
    "SUCCESS",
    "Generated correct Python code"
)

ProviderMemory.record_result(
    "gemini",
    "vision",
    "SUCCESS",
    "Good for multimodal analysis"
)

ProviderMemory.record_result(
    "deepseek",
    "coding",
    "SUCCESS",
    "Useful for low-cost coding tasks"
)

ProviderMemory.show_memory()