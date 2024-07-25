from abc import ABC, abstractmethod

class BasePlugin(ABC):
    @abstractmethod
    def initialize(self):
        """Initialize the plugin. This method should be called when the plugin is loaded."""
        pass

    @abstractmethod
    def execute_task(self, task_name: str, parameters: dict):
        """Execute a task defined by this plugin."""
        pass

    @abstractmethod
    def cleanup(self):
        """Perform any necessary cleanup operations when the plugin is unloaded."""
        pass

    def validate_config(self, config: dict) -> bool:
        """Validate the plugin configuration. Return True if valid, False otherwise."""
        return True

    def get_available_tasks(self) -> list:
        """Return a list of available tasks provided by this plugin."""
        return []