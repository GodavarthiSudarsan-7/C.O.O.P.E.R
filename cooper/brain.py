from cooper.memory.memory_manager import MemoryManager
from cooper.intent.intent_router import detect_intent
from cooper.work.plugin_registry import PluginRegistry

memory = MemoryManager()
registry = PluginRegistry()

def think(user_input: str) -> str:
    memory.remember(
        category="interaction",
        key="user_query",
        value=user_input
    )

    intent = detect_intent(user_input)

    context = {
        "input": user_input,
        "intent": intent,
        "memory": memory
    }

    plugins = registry.get_plugins_for_intent(intent)

    for plugin in plugins:
        result = plugin.execute(context)
        if isinstance(result, dict):
            context.update(result)
        elif isinstance(result, str):
            context["response"] = result

    if "response" in context:
        return context["response"]

    return f"I heard you say {user_input}. How can I help you next?"
