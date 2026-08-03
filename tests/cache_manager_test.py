from system_services.cache_manager import CacheManager

cache = CacheManager()

cache.add_cache(
    "active_ai",
    "OpenAI"
)

cache.add_cache(
    "current_project",
    "JAOS"
)

cache.show_cache()

print()

cache.remove_cache(
    "active_ai"
)

cache.show_cache()

print()

cache.clear_cache()

cache.show_cache()