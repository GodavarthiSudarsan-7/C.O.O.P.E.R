from cooper.work.plugin_interface import Plugin
from cooper.executor import execute_steps

class ExecutorPlugin(Plugin):

    @property
    def name(self):
        return "ExecutorPlugin"

    def can_handle(self, intent):
        return intent.get("action") not in [None, "unknown"]

    def execute(self, context):
        steps = context.get("plan")

        if not steps:
            return context

        execute_steps(steps)

        context["executed"] = True

        return context