from work.plugin_interface import Plugin
from planner import create_plan  # use existing function

class PlannerPlugin(Plugin):

    @property
    def name(self):
        return "Planner"

    def can_handle(self, intent: str) -> bool:
        return intent == "complex_task"

    def execute(self, context: dict) -> dict:
        plan = create_plan(context["input"])
        context["plan"] = plan
        return context
