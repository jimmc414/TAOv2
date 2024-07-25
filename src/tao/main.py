import typer
import yaml
from rich.console import Console
from rich.panel import Panel

from tao.workflow_engine import WorkflowEngine
from tao.configuration_manager import ConfigurationManager
from tao.plugin_system import PluginSystem
from tao.ui_manager import UIManager

app = typer.Typer()
console = Console()

@app.command()
def run(config_file: str = typer.Option("config.yaml", help="Path to the configuration file")):
    """
    Run the TAO Agent workflow.
    """
    console.print(Panel.fit("TAO Agent v2.0", title="Welcome", border_style="bold blue"))
    
    try:
        # Load configuration
        config_manager = ConfigurationManager(config_file)
        config = config_manager.load_config()
        
        # Initialize plugin system
        plugin_system = PluginSystem(config['workflow_engine']['plugin_directory'])
        plugins = plugin_system.load_plugins()
        
        # Initialize UI Manager
        ui_manager = UIManager(config['ui_config'])
        
        # Initialize and run workflow engine
        workflow_engine = WorkflowEngine(config, plugins, ui_manager)
        workflow_engine.execute_workflow()
        
        console.print(Panel.fit("Workflow completed successfully", title="Success", border_style="bold green"))
    except Exception as e:
        console.print(Panel.fit(f"An error occurred: {str(e)}", title="Error", border_style="bold red"))
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()

