from cooper.memory.memory_manager import MemoryManager


memory = MemoryManager()

def think(user_input: str) -> str:
 
    memory.remember(
        category="interaction",
        key="user_query",
        value=user_input
    )

    return f"I heard you say {user_input}. How can I help you next?"
