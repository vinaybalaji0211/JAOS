from brain.provider_health_monitor import ProviderHealthMonitor

monitor = ProviderHealthMonitor()

monitor.record_success(
    "openai",
    latency=1.2
)

monitor.record_success(
    "openai",
    latency=1.1
)

monitor.record_failure(
    "gemini"
)

monitor.record_success(
    "ollama",
    latency=0.7
)

monitor.show_health()