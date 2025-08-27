from .interface import LogFactory as Log_Factory_Interface
from ..handler.interface import Handler as Handler_Interface
from ..log.interface import Log as Log_Interface
from ..log.impl import Log as Log

class LogFactory(Log_Factory_Interface):
    def __init__(self, handler: Handler_Interface):
        self.handler = handler
    
    def create_log(self) -> Log_Interface:
        return Log(self.handler)