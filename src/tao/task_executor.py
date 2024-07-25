from tao.conditional_logic import ConditionalLogic
from tao.shared_utilities import SharedUtilities

class TaskExecutor:
    def __init__(self, plugins):
        self.plugins = plugins
        self.conditional_logic = ConditionalLogic()
        self.shared_utilities = SharedUtilities()

    def execute_task(self, task_name, task_config):
        plugin = self.plugins[task_config['plugin']]
        task_function = getattr(plugin, task_config['function'])
        
        if self.conditional_logic.evaluate(task_config['conditional_logic']):
            return task_function(**task_config['parameters'])
        else:
            return None