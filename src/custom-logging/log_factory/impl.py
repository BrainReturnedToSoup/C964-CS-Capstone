from .interface import Log_Factory as Log_Factory_Interface
from custom_logging.handler.interface import Handler as Handler_Interface
from custom_logging.log.interface import Log as Log_Interface
from custom_logging.log.impl import Log as Log
class Log_Factory(Log_Factory_Interface):
    def __init__(self, handler: Handler_Interface):
        self.handler = handler
    
    def create_log(self) -> Log_Interface:
        return Log(self.handler)