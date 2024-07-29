import typer
import yaml
from rich.console import Console
from rich.panel import Panel
import logging
from pathlib import Path

from tao.workflow_engine import WorkflowEngine
from tao.configuration_manager import ConfigurationManager
from tao.plugin_system import PluginSystem
from tao.ui_manager import UIManager
from tao.variable_manager import VariableManager
from tao.conditional_logic import ConditionalLogic
from tao.error_handler import ErrorHandler

app = typer.Typer()
console = Console()

def setup_logging(config):
    logging.basicConfig(
        level=getattr(logging, config.logging.level),
        format=config.logging.format,
        filename=config.logging.file,
        filemode='a'
    )
    return logging.getLogger(__name__)

@app.command()
def run(config_file: Path = typer.Option("config.yaml", help="Path to the configuration file")):
    """
    Run the TAO Agent v2.0 workflow.
    """
    console.print(Panel.fit("TAO Agent v2.0", title="Welcome", border_style="bold blue"))
    
    try:
        # Load configuration
        config_manager = ConfigurationManager(config_file)
        config = config_manager.load_config()
        
        # Setup logging
        logger = setup_logging(config)
        
        # Initialize error handler
        error_handler = ErrorHandler(config.error_handling, logger)
        
        # Initialize plugin system
        plugin_system = PluginSystem(config.workflow_engine.plugin_directory)
        plugins = plugin_system.load_plugins()
        
        # Initialize UI Manager
        ui_manager = UIManager(config.ui_config)
        
        # Initialize Variable Manager
        variable_manager = VariableManager(config.global_variables)
        
        # Initialize Conditional Logic
        conditional_logic = ConditionalLogic()
        
        # Initialize and run workflow engine
        workflow_engine = WorkflowEngine(
            config=config,
            plugins=plugins,
            ui_manager=ui_manager,
            variable_manager=variable_manager,
            conditional_logic=conditional_logic,
            error_handler=error_handler,
            logger=logger
        )
        
        result = workflow_engine.execute_workflow()
        
        if result:
            console.print(Panel.fit("Workflow completed successfully", title="Success", border_style="bold green"))
            for action in config.on_workflow_complete:
                workflow_engine.execute_action(action)
        else:
            console.print(Panel.fit("Workflow completed with errors", title="Warning", border_style="bold yellow"))
            for action in config.on_workflow_failure:
                workflow_engine.execute_action(action)
        
    except Exception as e:
        console.print(Panel.fit(f"An error occurred: {str(e)}", title="Error", border_style="bold red"))
        logger.exception("Unhandled exception in main execution")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()