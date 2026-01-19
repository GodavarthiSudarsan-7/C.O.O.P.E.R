from cooper.memory.memory_manager import MemoryManager

memory = MemoryManager()

class ModeManager:
    def set_mode(self, mode: str):
        memory.remember("system", "mode", mode)

    def get_mode(self):
        return memory.recall("mode") or "normal"
