import os

from logs.logger import logger


class PluginManager:

    def __init__(self):

        self.plugins = []

    def load_plugins(self):

        plugin_folder = "plugins"

        if not os.path.exists(plugin_folder):

            logger.warning("Plugins folder not found.")

            return

        for file in os.listdir(plugin_folder):

            if file.endswith(".py"):

                plugin_name = file[:-3]

                self.plugins.append(plugin_name)

                logger.info(
                    f"Plugin loaded: {plugin_name}"
                )

    def show_plugins(self):

        print("\nPlugins:")

        if not self.plugins:

            print("No plugins loaded.")

        else:

            for plugin in self.plugins:

                print("-", plugin)