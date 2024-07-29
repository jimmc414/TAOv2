import importlib
import os
from typing import Dict, Any, List
import logging
from tao.base_plugin import BasePlugin

class PluginSystem:
    def __init__(self, plugin_directory: str, logger: logging.Logger):
        self.plugin_directory = plugin_directory
        self.plugins: Dict[str, BasePlugin] = {}
        self.logger = logger

    def load_plugins(self) -> Dict[str, BasePlugin]:
        self.logger.info(f"Loading plugins from directory: {self.plugin_directory}")
        for filename in os.listdir(self.plugin_directory):
            if filename.endswith('.py') and not filename.startswith('__'):
                plugin_name = filename[:-3]
                try:
                    module = importlib.import_module(f"plugins.{plugin_name}")
                    for item_name in dir(module):
                        item = getattr(module, item_name)
                        if isinstance(item, type) and issubclass(item, BasePlugin) and item is not BasePlugin:
                            plugin_instance = item()
                            self.logger.info(f"Initializing plugin: {plugin_name}")
                            plugin_instance.initialize()
                            self.plugins[plugin_name] = plugin_instance
                            self.logger.info(f"Successfully loaded plugin: {plugin_name}")
                except Exception as e:
                    self.logger.error(f"Error loading plugin {plugin_name}: {str(e)}")
        return self.plugins

    def get_plugin(self, plugin_name: str) -> BasePlugin:
        plugin = self.plugins.get(plugin_name)
        if plugin is None:
            raise ValueError(f"Plugin not found: {plugin_name}")
        return plugin

    def execute_task(self, plugin_name: str, task_name: str, parameters: Dict[str, Any], variables: Dict[str, Any]) -> Any:
        plugin = self.get_plugin(plugin_name)
        self.logger.info(f"Executing task '{task_name}' with plugin '{plugin_name}'")
        try:
            result = plugin.execute_task(task_name, parameters, variables)
            self.logger.info(f"Task '{task_name}' executed successfully")
            return result
        except Exception as e:
            self.logger.error(f"Error executing task '{task_name}' with plugin '{plugin_name}': {str(e)}")
            raise

    def get_available_tasks(self, plugin_name: str) -> List[str]:
        plugin = self.get_plugin(plugin_name)
        return plugin.get_available_tasks()

    def validate_plugin_config(self, plugin_name: str, config: Dict[str, Any]) -> bool:
        plugin = self.get_plugin(plugin_name)
        return plugin.validate_config(config)

    def cleanup_plugins(self):
        for plugin_name, plugin in self.plugins.items():
            self.logger.info(f"Cleaning up plugin: {plugin_name}")
            try:
                plugin.cleanup()
                self.logger.info(f"Successfully cleaned up plugin: {plugin_name}")
            except Exception as e:
                self.logger.error(f"Error cleaning up plugin {plugin_name}: {str(e)}")

    def reload_plugin(self, plugin_name: str):
        if plugin_name in self.plugins:
            self.logger.info(f"Reloading plugin: {plugin_name}")
            old_plugin = self.plugins[plugin_name]
            try:
                old_plugin.cleanup()
                module = importlib.import_module(f"plugins.{plugin_name}")
                importlib.reload(module)
                for item_name in dir(module):
                    item = getattr(module, item_name)
                    if isinstance(item, type) and issubclass(item, BasePlugin) and item is not BasePlugin:
                        new_plugin = item()
                        new_plugin.initialize()
                        self.plugins[plugin_name] = new_plugin
                        self.logger.info(f"Successfully reloaded plugin: {plugin_name}")
                        return
            except Exception as e:
                self.logger.error(f"Error reloading plugin {plugin_name}: {str(e)}")
                # Restore old plugin instance
                self.plugins[plugin_name] = old_plugin
        else:
            self.logger.error(f"Cannot reload non-existent plugin: {plugin_name}")

    def __del__(self):
        self.cleanup_plugins()