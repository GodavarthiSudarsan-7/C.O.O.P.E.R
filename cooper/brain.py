from cooper.memory.memory_manager import MemoryManager
from cooper.memory.vector_memory import VectorMemory
from cooper.intent_router import get_intent
from cooper.work.plugin_registry import registry

memory = MemoryManager()
vector_memory = VectorMemory()

def think(user_input: str) -> str:
    memory.remember(
        category="interaction",
        key="user_query",
        value=user_input
    )

    vector_memory.remember(user_input)

    intent = get_intent(user_input)

    print("INTENT =", intent)

    related_memories = vector_memory.recall(
        user_input,
        limit=3
    )

    print("MEMORIES =", related_memories)

    context = {
        "input": user_input,
        "intent": intent,
        "memory": memory,
        "related_memories": related_memories
    }

    plugins = registry.get_plugins_for_intent(intent)

    print("PLUGINS =", [p.name for p in plugins])

    for plugin in plugins:
        print("RUNNING =", plugin.name)

        result = plugin.execute(context)

        if isinstance(result, dict):
            context.update(result)

        elif isinstance(result, str):
            context["response"] = result

    print("CONTEXT =", context)

    if "response" in context:
        return context["response"]

    return f"I heard you say {user_input}. How can I help you next?"