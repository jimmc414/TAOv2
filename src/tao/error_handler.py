import logging
from typing import Dict, Any, Optional
from rich.console import Console
from rich.panel import Panel
from rich.traceback import Traceback

class ErrorHandler:
    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.console = Console()
        self.error_count: Dict[str, int] = {}
        self.global_max_retries = config.get('global', {}).get('max_retries', 3)
        self.global_retry_delay = config.get('global', {}).get('retry_delay', 60)

    def handle_error(self, error: Exception, task: str, context: Dict[str, Any]) -> bool:
        self.error_count[task] = self.error_count.get(task, 0) + 1
        
        task_config = self.config.get('tasks', {}).get(task, {})
        max_retries = task_config.get('max_retries', self.global_max_retries)
        retry_delay = task_config.get('retry_delay', self.global_retry_delay)

        error_message = f"Error in task '{task}': {str(error)}"
        self.logger.error(error_message, exc_info=True, extra={'context': context})

        self.console.print(Panel.fit(
            Traceback.from_exception(type(error), error, error.__traceback__),
            title=f"Error in task '{task}'",
            border_style="bold red"
        ))

        if self.error_count[task] <= max_retries:
            self.console.print(f"Retrying... (Attempt {self.error_count[task]}/{max_retries})")
            self.logger.info(f"Retrying task '{task}' (Attempt {self.error_count[task]}/{max_retries})")
            return True
        else:
            self.console.print(f"Max retries reached for task '{task}'. Aborting.")
            self.logger.error(f"Max retries reached for task '{task}'. Aborting.")
            return False

    def log_warning(self, message: str, task: Optional[str] = None, context: Optional[Dict[str, Any]] = None):
        log_message = f"Warning: {message}"
        if task:
            log_message = f"Warning in task '{task}': {message}"
        
        self.logger.warning(log_message, extra={'context': context})
        self.console.print(Panel.fit(log_message, title="Warning", border_style="bold yellow"))

    def log_info(self, message: str, task: Optional[str] = None, context: Optional[Dict[str, Any]] = None):
        log_message = f"Info: {message}"
        if task:
            log_message = f"Info for task '{task}': {message}"
        
        self.logger.info(log_message, extra={'context': context})
        self.console.print(Panel.fit(log_message, title="Info", border_style="bold blue"))

    def reset_error_count(self, task: Optional[str] = None):
        if task:
            self.error_count[task] = 0
        else:
            self.error_count.clear()

    def get_error_count(self, task: str) -> int:
        return self.error_count.get(task, 0)

    def should_abort_workflow(self) -> bool:
        return any(count > self.global_max_retries for count in self.error_count.values())

    def get_error_summary(self) -> Dict[str, int]:
        return self.error_count.copy()