from cooper.work.plugin_interface import Plugin
from cooper.planner import plan_steps

class CriticPlugin(Plugin):
    @property
    def name(self):
        return "CriticPlugin"

    def can_handle(self, intent):
        return True

    def execute(self, context):
        if not context.get("plan"):
            return context

        if not isinstance(context["plan"], list) or len(context["plan"]) == 0:
            new_plan = plan_steps(context["input"])
            context["plan"] = new_plan
            context["replanned"] = True

        return context
