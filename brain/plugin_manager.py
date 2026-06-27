from logs.logger import logger


class PluginManager:

    def __init__(self):

        self.plugins = {}

    def load_plugin(
            self,
            plugin_name):

        self.plugins[plugin_name] = "LOADED"

        logger.info(
            f"Plugin loaded: {plugin_name}"
        )

    def unload_plugin(
            self,
            plugin_name):

        if plugin_name in self.plugins:

            self.plugins[plugin_name] = "UNLOADED"

            logger.info(
                f"Plugin unloaded: {plugin_name}"
            )

    def show_plugins(self):

        print("\nPlugin Manager:\n")

        if not self.plugins:

            print(
                "No plugins."
            )

            return

        for plugin, state in self.plugins.items():

            print(
                f"{plugin}: {state}"
            )