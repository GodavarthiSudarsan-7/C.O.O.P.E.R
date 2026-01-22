from cooper.memory.memory_manager import MemoryManager

memory = MemoryManager()

class TaskManager:
    def set_task(self, task: str):
        memory.remember("task", "current", task)

    def get_task(self):
        return memory.recall("current")

    def clear_task(self):
        memory.remember("task", "current", "")
