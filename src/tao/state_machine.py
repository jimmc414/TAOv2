from transitions import Machine
from rich.console import Console
from rich.table import Table
from typing import Dict, Any, List, Optional
import logging

class StateMachine:
    states = ['initialized', 'in_progress', 'completed', 'error', 'paused']

    def __init__(self, logger: logging.Logger):
        self.console = Console()
        self.logger = logger
        self.current_task: Optional[str] = None
        self.task_states: Dict[str, str] = {}
        self.task_variables: Dict[str, Dict[str, Any]] = {}
        self.task_history: Dict[str, List[Dict[str, Any]]] = {}

        # Initialize the state machine
        self.machine = Machine(model=self, states=StateMachine.states, initial='initialized')

        # Define transitions
        self.machine.add_transition('start_task', 'initialized', 'in_progress', after='_log_transition')
        self.machine.add_transition('complete_task', 'in_progress', 'completed', after='_log_transition')
        self.machine.add_transition('error_occurred', '*', 'error', after='_log_transition')
        self.machine.add_transition('pause_task', 'in_progress', 'paused', after='_log_transition')
        self.machine.add_transition('resume_task', 'paused', 'in_progress', after='_log_transition')
        self.machine.add_transition('reset', '*', 'initialized', after='_log_transition')

    def set_task(self, task: str, variables: Optional[Dict[str, Any]] = None):
        self.current_task = task
        if task not in self.task_states:
            self.task_states[task] = 'initialized'
            self.task_variables[task] = {}
            self.task_history[task] = []
        if variables:
            self.task_variables[task].update(variables)
        self.state = self.task_states[task]

    def _log_transition(self):
        if self.current_task:
            transition_info = {
                'from_state': self.task_states[self.current_task],
                'to_state': self.state,
                'variables': self.task_variables[self.current_task].copy()
            }
            self.task_history[self.current_task].append(transition_info)
            self.task_states[self.current_task] = self.state
            
            log_message = f"Task '{self.current_task}' transitioned to state: {self.state}"
            self.logger.info(log_message)
            self.console.print(f"[bold cyan]{log_message}[/bold cyan]")

    def update_variables(self, variables: Dict[str, Any]):
        if self.current_task:
            self.task_variables[self.current_task].update(variables)

    def get_current_state(self) -> str:
        return self.state

    def get_task_state(self, task: str) -> str:
        return self.task_states.get(task, 'unknown')

    def get_task_variables(self, task: str) -> Dict[str, Any]:
        return self.task_variables.get(task, {})

    def get_task_history(self, task: str) -> List[Dict[str, Any]]:
        return self.task_history.get(task, [])

    def get_all_task_states(self) -> Dict[str, str]:
        return self.task_states.copy()

    def display_current_state(self):
        if self.current_task:
            table = Table(title=f"Current State: {self.current_task}")
            table.add_column("Attribute", style="cyan")
            table.add_column("Value", style="magenta")
            table.add_row("State", self.state)
            for var, value in self.task_variables[self.current_task].items():
                table.add_row(var, str(value))
            self.console.print(table)

    def display_all_states(self):
        table = Table(title="All Task States")
        table.add_column("Task", style="cyan")
        table.add_column("State", style="magenta")
        for task, state in self.task_states.items():
            table.add_row(task, state)
        self.console.print(table)

    def task_completed(self):
        self.complete_task()

    def task_failed(self):
        self.error_occurred()

    def task_paused(self):
        self.pause_task()

    def task_resumed(self):
        self.resume_task()

    def reset_task(self, task: str):
        if task in self.task_states:
            self.task_states[task] = 'initialized'
            self.task_variables[task] = {}
            self.task_history[task] = []
            log_message = f"Task '{task}' has been reset"
            self.logger.info(log_message)
            self.console.print(f"[bold yellow]{log_message}[/bold yellow]")