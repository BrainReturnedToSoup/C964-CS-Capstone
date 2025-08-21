from .interface import Log as Log_Interface
from logging.handler.interface import Handler as Handler_Interface

class Log(Log_Interface):
    def __init__(self, handler: Handler_Interface):
        self.handler = handler
        self.data = {}
        self.commited = False
        
    def add_attribute(self, key: str, val: any) -> "Log":
        if self.commited:
            raise Exception()
        
        if key in self.data:
            raise Exception()
        
        self.data[key] = val
        
        return self
    
    def commit(self) -> None:
        if self.commited:
            raise Exception()
        
        self.commited = True
        self.handler(self.data)