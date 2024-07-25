import yaml
from pydantic import BaseModel, Field
from typing import List, Dict, Any

class TaskConfig(BaseModel):
    plugin: str
    function: str
    parameters: Dict[str, Any]
    conditional_logic: Any

class PluginConfig(BaseModel):
    name: str
    tasks: Dict[str, TaskConfig]
    workflow: List[str]

class UIConfig(BaseModel):
    type: str
    cli: Dict[str, Any] = Field(default_factory=dict)
    gui: Dict[str, Any] = Field(default_factory=dict)

class WorkflowEngineConfig(BaseModel):
    plugin_directory: str
    default_plugin: str
    state_persistence: Dict[str, Any] = Field(default_factory=dict)

class ConfigModel(BaseModel):
    base_config: Dict[str, Any]
    ui_config: UIConfig
    workflow_engine: WorkflowEngineConfig
    shared_utilities: Dict[str, Dict[str, str]]
    task_interface: Dict[str, List[str]]
    base_task: Dict[str, Any]
    task_templates: Dict[str, Dict[str, Any]]
    global_parameters: Dict[str, Any]
    plugins: List[PluginConfig]

class ConfigurationManager:
    def __init__(self, config_file):
        self.config_file = config_file

    def load_config(self):
        with open(self.config_file, 'r') as file:
            config_data = yaml.safe_load(file)
        try:
            return ConfigModel(**config_data)
        except ValueError as e:
            raise ValueError(f"Configuration validation failed: {e}")