import time
from typing import Dict, Any, List
import logging
from tao.configuration_manager import ConfigurationManager
from tao.plugin_system import PluginSystem
from tao.ui_manager import UIManager
from tao.task_executor import TaskExecutor
from tao.variable_manager import VariableManager
from tao.conditional_logic import ConditionalLogic
from tao.error_handler import ErrorHandler
from tao.state_machine import StateMachine

class WorkflowEngine:
    def __init__(self, config: ConfigurationManager, plugins: PluginSystem, 
                 ui_manager: UIManager, variable_manager: VariableManager, 
                 conditional_logic: ConditionalLogic, error_handler: ErrorHandler, 
                 logger: logging.Logger):
        self.config = config
        self.plugins = plugins
        self.ui_manager = ui_manager
        self.variable_manager = variable_manager
        self.conditional_logic = conditional_logic
        self.error_handler = error_handler
        self.logger = logger
        self.state_machine = StateMachine(logger)
        self.task_executor = TaskExecutor(plugins, variable_manager, conditional_logic, error_handler, logger)

    def execute_workflow(self) -> bool:
        workflow_config = self.config.get_workflow_config()
        self.ui_manager.display_welcome()
        self.ui_manager.display_task_tree(workflow_config.tasks)
        self.ui_manager.start_progress()

        start_time = time.time()
        total_tasks = len(workflow_config.tasks)
        completed_tasks = 0
        failed_tasks = 0

        try:
            for task_config in workflow_config.tasks:
                task_name = task_config.name
                self.logger.info(f"Starting task: {task_name}")
                self.state_machine.set_task(task_name)
                self.state_machine.start_task()

                try:
                    if task_config.steps:
                        result = self.task_executor.execute_task_with_steps(task_name, task_config.dict())
                    else:
                        result = self.task_executor.execute_task(task_name, task_config.dict())

                    if result is not None:
                        self.ui_manager.display_task_result(task_name, result)
                        self.state_machine.task_completed()
                        completed_tasks += 1
                    else:
                        self.state_machine.task_failed()
                        failed_tasks += 1

                except Exception as e:
                    self.logger.error(f"Error in task {task_name}: {str(e)}")
                    self.ui_manager.display_error(str(e), task_name)
                    self.state_machine.task_failed()
                    failed_tasks += 1

                    if self.error_handler.should_abort_workflow():
                        self.logger.error("Workflow aborted due to excessive errors")
                        self.ui_manager.display_error("Workflow aborted due to excessive errors")
                        return False

                self.ui_manager.display_progress(task_name, 100)

            end_time = time.time()
            execution_time = end_time - start_time

            summary = {
                "Total Tasks": total_tasks,
                "Completed Tasks": completed_tasks,
                "Failed Tasks": failed_tasks,
                "Execution Time": f"{execution_time:.2f} seconds"
            }
            self.ui_manager.display_workflow_summary(summary)

            return completed_tasks == total_tasks

        except Exception as e:
            self.logger.error(f"Unexpected error in workflow execution: {str(e)}")
            self.ui_manager.display_error(f"Unexpected error in workflow execution: {str(e)}")
            return False

        finally:
            self.ui_manager.stop_progress()

    def execute_action(self, action_config: Dict[str, Any]):
        action_name = action_config.get('function', 'Unknown Action')
        self.logger.info(f"Executing action: {action_name}")
        try:
            plugin_name = action_config.get('plugin', 'core_plugin')
            function_name = action_config['function']
            parameters = action_config.get('parameters', {})

            result = self.plugins.execute_task(plugin_name, function_name, parameters, {})
            self.ui_manager.display_info(f"Action {action_name} executed successfully")
            return result
        except Exception as e:
            self.logger.error(f"Error executing action {action_name}: {str(e)}")
            self.ui_manager.display_error(f"Error in action {action_name}: {str(e)}")
            return None

    def handle_data_flow(self, data_flow_config: List[Dict[str, str]]):
        for flow in data_flow_config:
            source = flow['from'].split('.')
            destination = flow['to'].split('.')

            if len(source) == 3 and len(destination) == 3:  # task.output.variable format
                source_task, source_output, source_var = source
                dest_task, dest_input, dest_var = destination

                # Retrieve the value from the source
                source_value = self.variable_manager.get_variable(f"{source_task}.{source_output}.{source_var}")

                # Set the value in the destination
                self.variable_manager.set_variable(f"{dest_task}.{dest_input}.{dest_var}", source_value)

            self.logger.info(f"Data flow: {flow['from']} -> {flow['to']}")

    def execute_plugin_task(self, plugin_name: str, task_name: str, parameters: Dict[str, Any]) -> Any:
        return self.plugins.execute_task(plugin_name, task_name, parameters, self.variable_manager.get_all_variables())

    def get_workflow_variables(self) -> Dict[str, Any]:
        return self.variable_manager.get_all_variables()

    def set_workflow_variable(self, name: str, value: Any):
        self.variable_manager.set_variable(name, value)

    def get_task_state(self, task_name: str) -> str:
        return self.state_machine.get_task_state(task_name)

    def get_all_task_states(self) -> Dict[str, str]:
        return self.state_machine.get_all_task_states()

    def pause_workflow(self):
        self.logger.info("Workflow paused")
        self.ui_manager.display_info("Workflow paused")
        self.state_machine.pause_task()

    def resume_workflow(self):
        self.logger.info("Workflow resumed")
        self.ui_manager.display_info("Workflow resumed")
        self.state_machine.resume_task()

    def abort_workflow(self):
        self.logger.warning("Workflow aborted")
        self.ui_manager.display_warning("Workflow aborted")
        return False