from brain.provider_memory import ProviderMemory
from brain.provider_benchmark import ProviderBenchmark


ProviderMemory.record_result(
    "openai",
    "coding",
    "SUCCESS",
    "Generated strong code"
)

ProviderMemory.record_result(
    "openai",
    "coding",
    "SUCCESS",
    "Handled debugging well"
)

ProviderMemory.record_result(
    "gemini",
    "coding",
    "FAILURE",
    "Weak coding response"
)

ProviderMemory.record_result(
    "deepseek",
    "coding",
    "SUCCESS",
    "Good coding response"
)

ProviderMemory.record_result(
    "gemini",
    "vision",
    "SUCCESS",
    "Good image analysis"
)

ProviderBenchmark.show_ranking()

ProviderBenchmark.show_ranking(
    "coding"
)