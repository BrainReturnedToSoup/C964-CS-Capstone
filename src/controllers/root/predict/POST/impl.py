from flask import Request, Response
from logging.log_factory.interface import Log_Factory as Logger_Interface
from services.predict.impl import Predicter

class Controller:
    def __init__(self, logger: Logger_Interface, predicter: Predicter):
        self.logger = logger
        self.predicter = predicter
        
    # the method for the flask route to use
    def handle(self, req: Request) -> Response:
        
        
        
        return