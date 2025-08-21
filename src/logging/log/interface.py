from abc import ABC, abstractmethod

class Log(ABC):
    @abstractmethod
    def __init__(self, handler):
        pass
    
    @abstractmethod
    def add_attribute(self, key, val) -> "Log":
        pass
    
    @abstractmethod
    def commit(self) -> None:
        pass