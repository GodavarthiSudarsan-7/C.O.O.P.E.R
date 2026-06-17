from cooper.work.plugin_interface import Plugin

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
        return intent.get("action") not in [None, "unknown"]

    def execute(self, context):
        plan = context.get("plan")

        if not plan:
            return context

        if not isinstance(plan, list):
            context.pop("plan", None)
            return context

        for step in plan:
            if step.get("action") not in VALID_ACTIONS:
                context.pop("plan", None)
                return context

        return context