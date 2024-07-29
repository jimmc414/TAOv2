from typing import Dict, Any, Optional
import logging
from tao.plugin_system import PluginSystem
from tao.variable_manager import VariableManager
from tao.conditional_logic import ConditionalLogic
from tao.error_handler import ErrorHandler

class TaskExecutor:
    def __init__(self, plugin_system: PluginSystem, variable_manager: VariableManager, 
                 conditional_logic: ConditionalLogic, error_handler: ErrorHandler, 
                 logger: logging.Logger):
        self.plugin_system = plugin_system
        self.variable_manager = variable_manager
        self.conditional_logic = conditional_logic
        self.error_handler = error_handler
        self.logger = logger

    def execute_task(self, task_name: str, task_config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        self.logger.info(f"Executing task: {task_name}")
        
        # Resolve variables in task parameters
        resolved_params = self._resolve_variables(task_config.get('parameters', {}))
        
        # Evaluate conditional logic
        if not self._evaluate_condition(task_config.get('conditional_logic')):
            self.logger.info(f"Skipping task {task_name} due to conditional logic")
            return None

        try:
            plugin_name = task_config['plugin']
            function_name = task_config['function']
            
            # Execute the task
            result = self.plugin_system.execute_task(plugin_name, function_name, resolved_params)
            
            # Update variables based on task output
            self._update_variables(task_config.get('set_variables', {}), result)
            
            self.logger.info(f"Task {task_name} executed successfully")
            return result
        except Exception as e:
            self.logger.error(f"Error executing task {task_name}: {str(e)}")
            self.error_handler.handle_error(e, task_name, resolved_params)
            return None

    def _resolve_variables(self, params: Dict[str, Any]) -> Dict[str, Any]:
        resolved_params = {}
        for key, value in params.items():
            if isinstance(value, str) and value.startswith('${') and value.endswith('}'):
                var_name = value[2:-1]
                resolved_params[key] = self.variable_manager.get_variable(var_name)
            else:
                resolved_params[key] = value
        return resolved_params

    def _evaluate_condition(self, condition: Optional[Dict[str, Any]]) -> bool:
        if condition is None:
            return True
        
        variables = self.variable_manager.get_all_variables()
        self.conditional_logic.update_context(variables)
        return self.conditional_logic.evaluate(condition)

    def _update_variables(self, variable_updates: Dict[str, str], task_result: Dict[str, Any]):
        for var_name, value_expr in variable_updates.items():
            try:
                value = eval(value_expr, {"__builtins__": None}, task_result)
                self.variable_manager.set_variable(var_name, value)
            except Exception as e:
                self.logger.error(f"Error updating variable {var_name}: {str(e)}")

    def execute_step(self, step_config: Dict[str, Any], task_context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        step_name = step_config.get('name', 'Unnamed Step')
        self.logger.info(f"Executing step: {step_name}")

        # Resolve variables in step parameters
        resolved_params = self._resolve_variables(step_config.get('parameters', {}))
        resolved_params.update(task_context)

        # Evaluate conditional logic for the step
        if not self._evaluate_condition(step_config.get('conditions')):
            self.logger.info(f"Skipping step {step_name} due to conditional logic")
            return None

        try:
            function_name = step_config['function']
            plugin_name = step_config.get('plugin', 'core_plugin')  # Default to core_plugin if not specified
            
            # Execute the step
            result = self.plugin_system.execute_task(plugin_name, function_name, resolved_params)
            
            # Update variables based on step output
            self._update_variables(step_config.get('set_variables', {}), result)
            
            self.logger.info(f"Step {step_name} executed successfully")
            return result
        except Exception as e:
            self.logger.error(f"Error executing step {step_name}: {str(e)}")
            self.error_handler.handle_error(e, step_name, resolved_params)
            return None

    def execute_task_with_steps(self, task_name: str, task_config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        self.logger.info(f"Executing task with steps: {task_name}")
        
        task_context = {}
        for step_config in task_config.get('steps', []):
            step_result = self.execute_step(step_config, task_context)
            if step_result is None:
                self.logger.warning(f"Step execution failed in task {task_name}")
                return None
            task_context.update(step_result)
        
        return task_context