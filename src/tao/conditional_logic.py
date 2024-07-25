class ConditionalLogic:
    def __init__(self):
        self.context = {}

    def evaluate(self, condition):
        if isinstance(condition, str):
            return self._evaluate_string_condition(condition)
        elif isinstance(condition, dict):
            return self._evaluate_dict_condition(condition)
        elif isinstance(condition, list):
            return self._evaluate_list_condition(condition)
        else:
            raise ValueError(f"Unsupported condition type: {type(condition)}")

    def _evaluate_string_condition(self, condition):
        return eval(condition, {"__builtins__": None}, self.context)

    def _evaluate_dict_condition(self, condition):
        operator = list(condition.keys())[0]
        operands = condition[operator]

        if operator == "and":
            return all(self.evaluate(op) for op in operands)
        elif operator == "or":
            return any(self.evaluate(op) for op in operands)
        elif operator == "not":
            return not self.evaluate(operands)
        else:
            raise ValueError(f"Unsupported operator: {operator}")

    def _evaluate_list_condition(self, conditions):
        return all(self.evaluate(condition) for condition in conditions)

    def update_context(self, new_context):
        self.context.update(new_context)