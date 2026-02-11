from cooper.work.plugin_interface import Plugin
from cooper.ai_answer import answer_question

class ResponderPlugin(Plugin):

    @property
    def name(self):
        return "ResponderPlugin"

    def can_handle(self, intent):
        return True

    def execute(self, context):
        if context.get("plan"):
            return context
        response = answer_question(context["input"])
        context["response"] = response
        return context
