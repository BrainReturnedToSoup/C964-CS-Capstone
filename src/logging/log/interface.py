from abc import ABC, abstractmethod
from logging.handler.interface import Handler as Handler_Interface

class Log(ABC):
    @abstractmethod
    def __init__(self, handler: Handler_Interface):
        pass
    
    @abstractmethod
    def add_attribute(self, key: str, val: any) -> "Log":
        pass
    
    @abstractmethod
    def commit(self) -> None:
        pass