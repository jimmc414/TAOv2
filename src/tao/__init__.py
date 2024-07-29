# TAO Agent v2.0

from .workflow_engine import WorkflowEngine
from .configuration_manager import ConfigurationManager
from .plugin_system import PluginSystem
from .ui_manager import UIManager
from .task_executor import TaskExecutor
from .variable_manager import VariableManager
from .conditional_logic import ConditionalLogic
from .error_handler import ErrorHandler
from .state_machine import StateMachine
from .progress_reporter import ProgressReporter
from .base_plugin import BasePlugin

__all__ = [
    'WorkflowEngine',
    'ConfigurationManager',
    'PluginSystem',
    'UIManager',
    'TaskExecutor',
    'VariableManager',
    'ConditionalLogic',
    'ErrorHandler',
    'StateMachine',
    'ProgressReporter',
    'BasePlugin',
]

__version__ = '2.0.0'

def get_version():
    return __version__

def initialize_logging():
    import logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        filename='tao_agent.log',
                        filemode='a')
    return logging.getLogger(__name__)

def create_workflow_engine(config_file: str):
    """
    Create and initialize a WorkflowEngine instance with all necessary components.
    
    Args:
    config_file (str): Path to the configuration file.
    
    Returns:
    WorkflowEngine: An initialized WorkflowEngine instance.
    """
    logger = initialize_logging()
    
    config_manager = ConfigurationManager(config_file)
    config = config_manager.load_config()
    
    plugin_system = PluginSystem(config.workflow_engine.plugin_directory, logger)
    ui_manager = UIManager(config.ui_config, logger)
    variable_manager = VariableManager(config.global_variables)
    conditional_logic = ConditionalLogic()
    error_handler = ErrorHandler(config.error_handling, logger)
    
    workflow_engine = WorkflowEngine(
        config=config_manager,
        plugins=plugin_system,
        ui_manager=ui_manager,
        variable_manager=variable_manager,
        conditional_logic=conditional_logic,
        error_handler=error_handler,
        logger=logger
    )
    
    return workflow_engine