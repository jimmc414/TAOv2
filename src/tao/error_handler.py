from rich.console import Console
from rich.panel import Panel

class ErrorHandler:
    def __init__(self, max_retries=3):
        self.console = Console()
        self.max_retries = max_retries
        self.error_count = 0

    def handle_error(self, error, task):
        self.error_count += 1
        self.console.print(Panel.fit(
            f"Error in task '{task}': {str(error)}",
            title="Error",
            border_style="bold red"
        ))

        if self.error_count >= self.max_retries:
            self.console.print("Max retries reached. Aborting workflow.")
            return False
        else:
            self.console.print(f"Retrying... (Attempt {self.error_count}/{self.max_retries})")
            return True

    def should_abort(self):
        return self.error_count >= self.max_retries

    def reset(self):
        self.error_count = 0