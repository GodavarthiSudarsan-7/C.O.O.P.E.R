from cooper.work.plugin_interface import Plugin
from cooper.planner import plan_steps

class PlannerPlugin(Plugin):

    @property
    def name(self):
        return "Planner"

    def can_handle(self, intent):
        action = intent.get("action")
        return action in [
            "open_website",
            "open_application",
            "youtube_play",
            "write_text"
        ]

    def execute(self, context):
        plan = plan_steps(context["input"])
        context["plan"] = plan
        return context