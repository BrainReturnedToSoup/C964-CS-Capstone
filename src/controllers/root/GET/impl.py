from flask import Request, Response, render_template
from logging.log_factory.interface import Log_Factory as Logger_Interface

class Controller:
    def __init__(self, logger: Logger_Interface, render_template: render_template):
        self.logger = logger
        self.render_template = render_template
    
    # the method for the flask route to use
    def handle(self, req: Request) -> Response:
        return self.render_template("index.html")