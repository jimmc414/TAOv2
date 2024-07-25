import importlib
import os
from tao.base_plugin import BasePlugin

class PluginSystem:
    def __init__(self, plugin_directory):
        self.plugin_directory = plugin_directory
        self.plugins = {}

    def load_plugins(self):
        for filename in os.listdir(self.plugin_directory):
            if filename.endswith('.py') and not filename.startswith('__'):
                module_name = filename[:-3]
                module = importlib.import_module(f"plugins.{module_name}")
                for item_name in dir(module):
                    item = getattr(module, item_name)
                    if isinstance(item, type) and issubclass(item, BasePlugin) and item is not BasePlugin:
                        plugin_instance = item()
                        plugin_instance.initialize()
                        self.plugins[module_name] = plugin_instance
        return self.plugins

    def get_plugin(self, plugin_name):
        return self.plugins.get(plugin_name)

    def unload_plugins(self):
        for plugin in self.plugins.values():
            plugin.cleanup()
        self.plugins.clear()