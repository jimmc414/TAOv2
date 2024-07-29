from rich.progress import Progress, TaskID
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from typing import Dict, Any, Optional
import logging

class ProgressReporter:
    def __init__(self, ui_manager, logger: logging.Logger):
        self.ui_manager = ui_manager
        self.logger = logger
        self.console = Console()
        self.progress = Progress()
        self.tasks: Dict[str, TaskID] = {}
        self.task_variables: Dict[str, Dict[str, Any]] = {}
        self.conditional_branches: Dict[str, str] = {}

    def start_task(self, task_name: str, total_steps: int = 100):
        task_id = self.progress.add_task(f"[cyan]{task_name}", total=total_steps)
        self.tasks[task_name] = task_id
        self.task_variables[task_name] = {}
        self.progress.start()
        self.logger.info(f"Started task: {task_name}")

    def update_progress(self, task_name: str, progress_percentage: float, 
                        step_name: Optional[str] = None, 
                        variables: Optional[Dict[str, Any]] = None,
                        branch_taken: Optional[str] = None):
        if task_name in self.tasks:
            self.progress.update(self.tasks[task_name], completed=progress_percentage)
            
            if variables:
                self.task_variables[task_name].update(variables)
            
            if branch_taken:
                self.conditional_branches[task_name] = branch_taken

            log_message = f"Task '{task_name}' progress: {progress_percentage:.2f}%"
            if step_name:
                log_message += f" (Step: {step_name})"
            if branch_taken:
                log_message += f" (Branch taken: {branch_taken})"
            self.logger.info(log_message)

        self.ui_manager.display_progress(task_name, progress_percentage, step_name, variables, branch_taken)

    def complete_task(self, task_name: str):
        if task_name in self.tasks:
            self.progress.update(self.tasks[task_name], completed=100)
            self.progress.remove_task(self.tasks[task_name])
            del self.tasks[task_name]
            self.logger.info(f"Completed task: {task_name}")

        self._display_task_summary(task_name)

    def _display_task_summary(self, task_name: str):
        variables = self.task_variables.get(task_name, {})
        branch_taken = self.conditional_branches.get(task_name)

        table = Table(title=f"Task Summary: {task_name}")
        table.add_column("Attribute", style="cyan")
        table.add_column("Value", style="magenta")

        for var_name, var_value in variables.items():
            table.add_row(var_name, str(var_value))

        if branch_taken:
            table.add_row("Branch Taken", branch_taken)

        self.console.print(Panel(table, expand=False))

    def report_error(self, task_name: str, error_message: str):
        self.logger.error(f"Error in task '{task_name}': {error_message}")
        self.console.print(Panel(f"[bold red]Error in task '{task_name}':[/bold red] {error_message}", 
                                 title="Error", border_style="red"))

    def display_workflow_summary(self, total_tasks: int, completed_tasks: int, 
                                 failed_tasks: int, total_time: float):
        summary_table = Table(title="Workflow Summary")
        summary_table.add_column("Metric", style="cyan")
        summary_table.add_column("Value", style="magenta")

        summary_table.add_row("Total Tasks", str(total_tasks))
        summary_table.add_row("Completed Tasks", str(completed_tasks))
        summary_table.add_row("Failed Tasks", str(failed_tasks))
        summary_table.add_row("Total Execution Time", f"{total_time:.2f} seconds")

        self.console.print(Panel(summary_table, expand=False))
        self.logger.info(f"Workflow completed. Total tasks: {total_tasks}, "
                         f"Completed: {completed_tasks}, Failed: {failed_tasks}, "
                         f"Total time: {total_time:.2f} seconds")

    def stop(self):
        self.progress.stop()