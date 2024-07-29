from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BasePlugin(ABC):
    @abstractmethod
    def initialize(self) -> None:
        """
        Initialize the plugin. This method should be called when the plugin is loaded.
        """
        pass

    @abstractmethod
    def execute_task(self, task_name: str, parameters: Dict[str, Any], variables: Dict[str, Any]) -> Any:
        """
        Execute a task defined by this plugin.

        Args:
            task_name (str): The name of the task to execute.
            parameters (Dict[str, Any]): The parameters for the task.
            variables (Dict[str, Any]): Task-specific variables.

        Returns:
            Any: The result of the task execution.
        """
        pass

    @abstractmethod
    def cleanup(self) -> None:
        """
        Perform any necessary cleanup operations when the plugin is unloaded.
        """
        pass

    def validate_config(self, config: Dict[str, Any]) -> bool:
        """
        Validate the plugin configuration.

        Args:
            config (Dict[str, Any]): The configuration to validate.

        Returns:
            bool: True if the configuration is valid, False otherwise.
        """
        return True

    def get_available_tasks(self) -> List[str]:
        """
        Return a list of available tasks provided by this plugin.

        Returns:
            List[str]: A list of task names available in this plugin.
        """
        return []

    def set_variable(self, name: str, value: Any) -> None:
        """
        Set a variable in the plugin's context.

        Args:
            name (str): The name of the variable.
            value (Any): The value to set.
        """
        pass

    def get_variable(self, name: str) -> Any:
        """
        Get the value of a variable from the plugin's context.

        Args:
            name (str): The name of the variable.

        Returns:
            Any: The value of the variable, or None if not found.
        """
        pass