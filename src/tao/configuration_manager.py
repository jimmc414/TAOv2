import yaml
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union

class VariableConfig(BaseModel):
    name: str
    value: Any
    type: Optional[str] = None
    description: Optional[str] = None

class ConditionConfig(BaseModel):
    type: str
    expression: str
    true_branch: str
    false_branch: str

class StepConfig(BaseModel):
    name: str
    description: Optional[str] = None
    function: str
    parameters: Dict[str, Any]
    timeout: Optional[int] = None
    on_success: Optional[Dict[str, Any]] = None
    on_failure: Optional[Dict[str, Any]] = None
    conditions: Optional[List[ConditionConfig]] = None
    variables: Optional[Dict[str, Any]] = None
    set_variables: Optional[Dict[str, str]] = None

class TaskConfig(BaseModel):
    name: str
    description: Optional[str] = None
    plugin: str
    function: str
    parameters: Dict[str, Any]
    dependencies: Optional[List[str]] = None
    timeout: Optional[int] = None
    retry: Optional[Dict[str, int]] = None
    on_success: Optional[Dict[str, Any]] = None
    on_failure: Optional[Dict[str, Any]] = None
    steps: Optional[List[StepConfig]] = None
    variables: Optional[Dict[str, Any]] = None
    set_variables: Optional[Dict[str, str]] = None
    conditional_logic: Optional[Union[str, Dict[str, Any]]] = None

class PluginConfig(BaseModel):
    name: str
    module: str
    description: Optional[str] = None

class WorkflowConfig(BaseModel):
    name: str
    description: Optional[str] = None
    flags: Optional[List[str]] = None
    variables: Dict[str, Any] = Field(default_factory=dict)
    data_flow: Optional[List[Dict[str, str]]] = None
    tasks: List[TaskConfig]

class LoggingConfig(BaseModel):
    level: str
    file: str
    format: str

class ErrorHandlingConfig(BaseModel):
    on_task_error: str
    on_workflow_failure: str

class ConfigModel(BaseModel):
    config_version: str
    name: str
    description: Optional[str] = None
    global_variables: Dict[str, Any] = Field(default_factory=dict)
    workflow_engine: Dict[str, Any]
    logging: LoggingConfig
    plugins: List[PluginConfig]
    workflow: WorkflowConfig
    error_handling: ErrorHandlingConfig
    on_workflow_complete: List[Dict[str, Any]]
    on_workflow_failure: List[Dict[str, Any]]

class ConfigurationManager:
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.config: Optional[ConfigModel] = None

    def load_config(self) -> ConfigModel:
        with open(self.config_file, 'r') as file:
            config_data = yaml.safe_load(file)
        try:
            self.config = ConfigModel(**config_data)
            return self.config
        except ValueError as e:
            raise ValueError(f"Configuration validation failed: {e}")

    def get_plugin_config(self, plugin_name: str) -> Optional[PluginConfig]:
        if self.config:
            for plugin in self.config.plugins:
                if plugin.name == plugin_name:
                    return plugin
        return None

    def get_task_config(self, task_name: str) -> Optional[TaskConfig]:
        if self.config:
            for task in self.config.workflow.tasks:
                if task.name == task_name:
                    return task
        return None

    def get_global_variables(self) -> Dict[str, Any]:
        return self.config.global_variables if self.config else {}

    def get_workflow_variables(self) -> Dict[str, Any]:
        return self.config.workflow.variables if self.config else {}

    def get_error_handling_config(self) -> ErrorHandlingConfig:
        return self.config.error_handling if self.config else ErrorHandlingConfig(on_task_error="log_and_continue", on_workflow_failure="notify_admin")

    def get_logging_config(self) -> LoggingConfig:
        return self.config.logging if self.config else LoggingConfig(level="INFO", file="tao.log", format="%(asctime)s - %(levelname)s - %(message)s")

    def validate_config(self) -> bool:
        # Implement additional validation logic here
        return True if self.config else False