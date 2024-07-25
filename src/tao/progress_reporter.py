from rich.progress import Progress, TaskID
from rich.console import Console

class ProgressReporter:
    def __init__(self, ui_manager):
        self.ui_manager = ui_manager
        self.console = Console()
        self.progress = Progress()
        self.tasks = {}

    def start_task(self, task_name):
        task_id = self.progress.add_task(f"[cyan]{task_name}", total=100)
        self.tasks[task_name] = task_id
        self.progress.start()

    def update_progress(self, task_name, progress_percentage):
        if task_name in self.tasks:
            self.progress.update(self.tasks[task_name], completed=progress_percentage)
        self.ui_manager.display_progress(task_name, progress_percentage)

    def complete_task(self, task_name):
        if task_name in self.tasks:
            self.progress.update(self.tasks[task_name], completed=100)
            self.progress.remove_task(self.tasks[task_name])
            del self.tasks[task_name]

    def stop(self):
        self.progress.stop()