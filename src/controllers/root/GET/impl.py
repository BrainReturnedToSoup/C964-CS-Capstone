from http import HTTPStatus
from flask import Request, Response, render_template
from custom_logging.log_factory.interface import LogFactory as LogFactory_Interface
from .errors import NotSecureError

class Controller:
    def __init__(self, logger: LogFactory_Interface):
        self.logger=logger
        self.render_template=render_template
        self.response=Response
    
    # the method for the flask route to use
    def handle(self, req: Request) -> Response:
        try:
            if not req.is_secure:
                raise NotSecureError()
            
            self.logger \
                .create_log() \
                .add_attribute("log-origin", "controllers.root.GET.impl") \
                .add_attribute("route", "/") \
                .add_attribute("method", "GET") \
                .add_attribute("request", req) \
                .commit() 
            
            return self.render_template("index.html")
        except Exception as e:
            self.logger \
                .create_log() \
                .add_attribute("log-origin", "controllers.root.GET.impl") \
                .add_attribute("route", "/") \
                .add_attribute("method", "GET") \
                .add_attribute("request", req) \
                .add_attribute("exception-raised", e) \
                .commit() 
                
            if isinstance(e, NotSecureError):
                return self.response(status=HTTPStatus.FORBIDDEN)
            else:
                return self.response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
                