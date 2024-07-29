from typing import Dict, Any, Optional
import re
from jinja2 import Template, Environment, meta

class VariableManager:
    def __init__(self, initial_variables: Optional[Dict[str, Any]] = None):
        self.variables: Dict[str, Any] = initial_variables or {}
        self.jinja_env = Environment()

    def set_variable(self, name: str, value: Any):
        """
        Set a variable with the given name and value.

        Args:
            name (str): The name of the variable.
            value (Any): The value to assign to the variable.
        """
        if isinstance(value, str) and self._is_dynamic_expression(value):
            self.variables[name] = self._evaluate_expression(value)
        else:
            self.variables[name] = value

    def get_variable(self, name: str) -> Any:
        """
        Get the value of a variable by name.

        Args:
            name (str): The name of the variable.

        Returns:
            Any: The value of the variable.

        Raises:
            KeyError: If the variable is not found.
        """
        if name not in self.variables:
            raise KeyError(f"Variable '{name}' not found")
        return self.variables[name]

    def get_all_variables(self) -> Dict[str, Any]:
        """
        Get all variables as a dictionary.

        Returns:
            Dict[str, Any]: A dictionary containing all variables.
        """
        return self.variables.copy()

    def update_variables(self, new_variables: Dict[str, Any]):
        """
        Update multiple variables at once.

        Args:
            new_variables (Dict[str, Any]): A dictionary of variable names and values to update.
        """
        for name, value in new_variables.items():
            self.set_variable(name, value)

    def resolve_variables(self, template: str) -> str:
        """
        Resolve variables within a string template.

        Args:
            template (str): A string template containing variable placeholders.

        Returns:
            str: The template with variables resolved.
        """
        return Template(template).render(self.variables)

    def _is_dynamic_expression(self, value: str) -> bool:
        """
        Check if a string value is a dynamic expression.

        Args:
            value (str): The string to check.

        Returns:
            bool: True if the string is a dynamic expression, False otherwise.
        """
        return value.strip().startswith('{{') and value.strip().endswith('}}')

    def _evaluate_expression(self, expression: str) -> Any:
        """
        Evaluate a dynamic expression.

        Args:
            expression (str): The expression to evaluate.

        Returns:
            Any: The result of evaluating the expression.

        Raises:
            ValueError: If the expression is invalid or contains undefined variables.
        """
        template = self.jinja_env.from_string(expression)
        try:
            return template.render(self.variables)
        except Exception as e:
            raise ValueError(f"Error evaluating expression '{expression}': {str(e)}")

    def get_undefined_variables(self, template: str) -> set:
        """
        Get a set of undefined variables in a template string.

        Args:
            template (str): The template string to check for undefined variables.

        Returns:
            set: A set of undefined variable names.
        """
        ast = self.jinja_env.parse(template)
        undefined = meta.find_undeclared_variables(ast)
        return undefined - set(self.variables.keys())

    def clear_variables(self):
        """
        Clear all variables.
        """
        self.variables.clear()

    def delete_variable(self, name: str):
        """
        Delete a variable by name.

        Args:
            name (str): The name of the variable to delete.

        Raises:
            KeyError: If the variable is not found.
        """
        if name not in self.variables:
            raise KeyError(f"Variable '{name}' not found")
        del self.variables[name]