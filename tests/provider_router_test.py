from brain.provider_router import ProviderRouter

router = ProviderRouter()

router.show_providers()

print("\nBest for general:")
print(router.select_provider())

print("\nBest for offline:")
print(router.select_provider("offline"))

print("\nBest for coding:")
print(router.select_provider("coding"))

print("\nBest for vision:")
print(router.select_provider("vision"))

print("\nBest for writing:")
print(router.select_provider("writing"))

router.register_provider(
    "mistral",
    "cloud",
    [
        "reasoning",
        "fast",
        "general"
    ],
    priority=4
)

print("\nAfter adding Mistral:")

router.show_providers()