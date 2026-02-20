from cooper.work.plugin_interface import Plugin
from cooper.ai_answer import answer_question
from cooper.actions import google_search

class ResponderPlugin(Plugin):

    @property
    def name(self):
        return "ResponderPlugin"

    def can_handle(self, intent):
        return True

    def execute(self, context):
        if context.get("plan"):
            return context

        user_input = context["input"].lower()

        if user_input.startswith("search "):
            query = user_input.replace("search ", "", 1)
            google_search(query)
            context["response"] = "Searching on Google."
            return context

        response = answer_question(context["input"])

        if any(x in response.lower() for x in [
            "i don't know",
            "not sure",
            "no information",
            "cannot find"
        ]):
            google_search(context["input"])
            context["response"] = "I couldn't find a confident answer, so I searched it on Google."
            return context

        context["response"] = response
        return context