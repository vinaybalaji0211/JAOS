from brain.plugin_manager import PluginManager

manager = PluginManager()

manager.load_plugin(
    "Weather Plugin"
)

manager.load_plugin(
    "Browser Plugin"
)

manager.show_plugins()

manager.unload_plugin(
    "Weather Plugin"
)

manager.show_plugins()