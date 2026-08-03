from brain.provider_transparency import ProviderTransparency

transparency = ProviderTransparency()

transparency.record_provider(
    "openai",
    "gpt-5",
    "Best provider for reasoning and coding",
    "cloud"
)

transparency.show_last_provider()