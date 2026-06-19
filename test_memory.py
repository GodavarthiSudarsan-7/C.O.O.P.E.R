from cooper.memory.vector_memory import VectorMemory

memory = VectorMemory()

memory.remember(
    "Boss is building COOPER, a Jarvis-like AI assistant using Python, Ollama, Tavily and plugins."
)

memory.remember(
    "Boss entered third year Computer Science AI specialization."
)

memory.remember(
    "COOPER uses Mistral as the primary model."
)

print(memory.recall("What project am I building?"))