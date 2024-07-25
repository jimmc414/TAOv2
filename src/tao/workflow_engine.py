from tao.task_executor import TaskExecutor
from tao.state_machine import StateMachine
from tao.error_handler import ErrorHandler
from tao.progress_reporter import ProgressReporter

class WorkflowEngine:
    def __init__(self, config, plugins, ui_manager):
        self.config = config
        self.plugins = plugins
        self.ui_manager = ui_manager
        self.task_executor = TaskExecutor(plugins)
        self.state_machine = StateMachine()
        self.error_handler = ErrorHandler()
        self.progress_reporter = ProgressReporter(ui_manager)

    def execute_workflow(self):
        workflow = self.config['workflow']
        for task in workflow:
            try:
                self.state_machine.set_state(task)
                task_config = self.config['tasks'][task]
                result = self.task_executor.execute_task(task, task_config)
                self.progress_reporter.update_progress(task, result)
            except Exception as e:
                self.error_handler.handle_error(e, task)
                if self.error_handler.should_abort():
                    break
        self.ui_manager.display_summary(self.state_machine.get_final_state())