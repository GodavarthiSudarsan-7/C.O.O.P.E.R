from abc import ABC, abstractmethod

class Plugin(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def can_handle(self, intent: str) -> bool:
        pass

    @abstractmethod
    def execute(self, context: dict) -> str:
        pass
