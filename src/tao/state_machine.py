from transitions import Machine
from rich.console import Console

class StateMachine:
    states = ['initialized', 'in_progress', 'completed', 'error']

    def __init__(self):
        self.console = Console()
        self.current_task = None
        self.task_states = {}

        # Initialize the state machine
        self.machine = Machine(model=self, states=StateMachine.states, initial='initialized')

        # Define transitions
        self.machine.add_transition('start_task', 'initialized', 'in_progress', after='log_transition')
        self.machine.add_transition('complete_task', 'in_progress', 'completed', after='log_transition')
        self.machine.add_transition('error_occurred', '*', 'error', after='log_transition')
        self.machine.add_transition('reset', '*', 'initialized', after='log_transition')

    def set_state(self, task):
        self.current_task = task
        if task not in self.task_states:
            self.task_states[task] = 'initialized'
        self.state = self.task_states[task]

    def log_transition(self):
        self.console.print(f"Task '{self.current_task}' transitioned to state: {self.state}")
        self.task_states[self.current_task] = self.state

    def get_final_state(self):
        return self.task_states

    def task_completed(self):
        self.complete_task()

    def task_failed(self):
        self.error_occurred()