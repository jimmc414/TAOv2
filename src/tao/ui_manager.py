from rich.console import Console
from rich.table import Table

class UIManager:
    def __init__(self, ui_config):
        self.console = Console()
        self.ui_config = ui_config

    def display_progress(self, task, progress):
        self.console.print(f"Task: {task} - Progress: {progress}%")

    def display_summary(self, final_state):
        table = Table(title="Workflow Summary")
        table.add_column("Task", style="cyan")
        table.add_column("Status", style="magenta")
        
        for task, status in final_state.items():
            table.add_row(task, status)
        
        self.console.print(table)