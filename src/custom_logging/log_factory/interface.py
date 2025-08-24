from abc import ABC, abstractmethod
from custom_logging.log.interface import Log as Log_Interface
from custom_logging.handler.interface import Handler as Handler_Interface

class LogFactory(ABC):
    @abstractmethod
    def __init__(self, handler: Handler_Interface) -> None:
        pass
    
    @abstractmethod
    def create_log(self) -> Log_Interface:
        pass