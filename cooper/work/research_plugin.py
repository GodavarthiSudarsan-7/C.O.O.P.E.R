from cooper.work.plugin_interface import Plugin
from cooper.web_search import search_web
import ollama

class ResearchPlugin(Plugin):

    @property
    def name(self):
        return "ResearchPlugin"

    def can_handle(self, intent):
        return intent.get("action") == "research"

    def execute(self, context):
        query = context["input"]

        search_results = search_web(query)

        prompt = f"""
Answer the user's question using the web search results.

Question:
{query}

Search Results:
{search_results}
"""

        response = ollama.chat(
            model="mistral",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        context["response"] = response["message"]["content"]

        return context