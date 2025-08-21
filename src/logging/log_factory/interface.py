from abc import ABC, abstractmethod

from logging.log.interface import Log as Log_Interface
from logging.handler.interface import Handler as Handler_Interface

class Log_Factory_Interface(ABC):
    @abstractmethod
    def __init__(self, handler: Handler_Interface) -> None:
        pass
    
    @abstractmethod
    def create_log() -> Log_Interface:
        pass