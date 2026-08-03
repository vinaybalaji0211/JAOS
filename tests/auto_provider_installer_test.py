from brain.auto_provider_installer import AutoProviderInstaller

AutoProviderInstaller.install_provider(
    "perplexity",
    "cloud",
    [
        "research",
        "web_search",
        "summarization"
    ],
    priority=4,
    approved=False
)

AutoProviderInstaller.install_provider(
    "perplexity",
    "cloud",
    [
        "research",
        "web_search",
        "summarization"
    ],
    priority=4,
    approved=True
)