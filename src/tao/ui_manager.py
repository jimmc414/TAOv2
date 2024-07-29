from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, TaskID
from rich.syntax import Syntax
from rich.tree import Tree
from typing import Dict, Any, Optional, List
import logging

class UIManager:
    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        self.console = Console()
        self.config = config
        self.logger = logger
        self.progress = Progress()
        self.tasks: Dict[str, TaskID] = {}

    def display_welcome(self):
        welcome_message = self.config.get('welcome_message', 'Welcome to TAO Agent v2.0')
        self.console.print(Panel(welcome_message, expand=False, border_style="bold blue"))

    def display_progress(self, task_name: str, progress_percentage: float, 
                         step_name: Optional[str] = None, 
                         variables: Optional[Dict[str, Any]] = None,
                         branch_taken: Optional[str] = None):
        if task_name not in self.tasks:
            self.tasks[task_name] = self.progress.add_task(f"[cyan]{task_name}", total=100)
        
        self.progress.update(self.tasks[task_name], completed=progress_percentage)
        
        status_message = f"Task: {task_name} - Progress: {progress_percentage:.2f}%"
        if step_name:
            status_message += f" (Step: {step_name})"
        if branch_taken:
            status_message += f" (Branch: {branch_taken})"
        
        self.console.print(status_message)
        
        if variables:
            self.display_variables(variables)

    def display_variables(self, variables: Dict[str, Any]):
        table = Table(title="Current Variables")
        table.add_column("Variable", style="cyan")
        table.add_column("Value", style="magenta")
        
        for var, value in variables.items():
            table.add_row(str(var), str(value))
        
        self.console.print(table)

    def display_task_result(self, task_name: str, result: Any):
        self.console.print(f"[bold green]Task Completed:[/bold green] {task_name}")
        if isinstance(result, dict):
            table = Table(title=f"Result for {task_name}")
            table.add_column("Key", style="cyan")
            table.add_column("Value", style="magenta")
            for key, value in result.items():
                table.add_row(str(key), str(value))
            self.console.print(table)
        else:
            self.console.print(Panel(str(result), title=f"Result for {task_name}", expand=False))

    def display_error(self, error_message: str, task_name: Optional[str] = None):
        title = f"Error in task: {task_name}" if task_name else "Error"
        self.console.print(Panel(error_message, title=title, border_style="bold red"))

    def display_warning(self, warning_message: str):
        self.console.print(Panel(warning_message, title="Warning", border_style="bold yellow"))

    def display_info(self, info_message: str):
        self.console.print(Panel(info_message, title="Info", border_style="bold blue"))

    def display_code(self, code: str, language: str = "python"):
        syntax = Syntax(code, language, theme="monokai", line_numbers=True)
        self.console.print(syntax)

    def display_workflow_summary(self, summary: Dict[str, Any]):
        table = Table(title="Workflow Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")
        
        for key, value in summary.items():
            table.add_row(str(key), str(value))
        
        self.console.print(table)

    def display_task_tree(self, tasks: List[Dict[str, Any]]):
        tree = Tree("Workflow")
        for task in tasks:
            task_node = tree.add(f"[bold cyan]{task['name']}[/bold cyan]")
            if 'steps' in task:
                for step in task['steps']:
                    step_node = task_node.add(f"[green]{step['name']}[/green]")
                    if 'conditions' in step:
                        step_node.add("[yellow]Conditional[/yellow]")
            elif 'conditional_logic' in task:
                task_node.add("[yellow]Conditional[/yellow]")
        
        self.console.print(tree)

    def prompt_user(self, message: str) -> str:
        return self.console.input(f"[bold yellow]{message}[/bold yellow] ")

    def display_help(self):
        help_text = self.config.get('help_text', 'No help available.')
        self.console.print(Panel(help_text, title="Help", expand=False))

    def clear_screen(self):
        self.console.clear()

    def start_progress(self):
        self.progress.start()

    def stop_progress(self):
        self.progress.stop()