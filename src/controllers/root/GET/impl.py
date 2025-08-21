from flask import Request, Response, render_template
from logging.log_factory.interface import Log_Factory as Logger_Interface

class Controller:
    def __init__(self, logger: Logger_Interface, render_template: render_template, response: Response):
        self.logger=logger
        self.render_template=render_template
        self.response=response
    
    # the method for the flask route to use
    def handle(self, req: Request) -> Response:
        try:
            self.logger \
                .create_log() \
                .add_attribute("log-origin", "route=/:method=GET") \
                .add_attribute("request", req) \
                .commit() 
            
            return self.render_template("index.html")
        except Exception as e:
            self.logger \
                .create_log() \
                .add_attribute("log-origin", "route=/:method=GET") \
                .add_attribute("request", req) \
                .add_attribute("exception-raised", e) \
                .commit() 
                
            return self.response(status=500)