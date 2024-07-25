import importlib
import os

class PluginSystem:
    def __init__(self, plugin_directory):
        self.plugin_directory = plugin_directory

    def load_plugins(self):
        plugins = {}
        for filename in os.listdir(self.plugin_directory):
            if filename.endswith('.py') and not filename.startswith('__'):
                module_name = filename[:-3]
                module = importlib.import_module(f"plugins.{module_name}")
                plugins[module_name] = module
        return plugins