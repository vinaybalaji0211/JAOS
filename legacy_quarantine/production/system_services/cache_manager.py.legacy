from logs.logger import logger


class CacheManager:

    def __init__(self):

        self.cache = {}

    def add_cache(
            self,
            key,
            value):

        self.cache[key] = value

        logger.info(
            f"Cache added: {key}"
        )

    def remove_cache(
            self,
            key):

        self.cache.pop(key, None)

        logger.info(
            f"Cache removed: {key}"
        )

    def clear_cache(self):

        self.cache.clear()

        logger.info(
            "Cache cleared."
        )

    def show_cache(self):

        print("\n=== Cache Manager ===\n")

        if not self.cache:

            print("Cache is empty.")
            return

        for key, value in self.cache.items():

            print(f"{key} : {value}")