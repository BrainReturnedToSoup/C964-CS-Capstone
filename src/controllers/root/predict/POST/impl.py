from flask import Request
from flask import Response

from logging.log_factory.interface import Log_Factory as Logger_Interface

class Controller:
    def __init__(self, logger: Logger_Interface):
        
        return
    
    # the method for the flask route to use
    def handle(self, req: Request) -> Response:
        
        return