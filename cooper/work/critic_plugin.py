from cooper.work.plugin_interface import Plugin
from cooper.planner import plan_steps

VALID_ACTIONS = {
    "open_website",
    "open_application",
    "google_search",
    "youtube_search",
    "youtube_play",
    "write_text"
}

class CriticPlugin(Plugin):

    @property
    def name(self):
        return "CriticPlugin"

    def can_handle(self, intent):
        return True

    def execute(self, context):
        plan = context.get("plan")

        if not plan or not isinstance(plan, list):
            new_plan = plan_steps(context["input"])
            context["plan"] = new_plan
            context["replanned"] = True
            return context

        for step in plan:
            if step.get("action") not in VALID_ACTIONS:
                context.pop("plan", None)
                context["invalid_plan"] = True
                return context

        return context