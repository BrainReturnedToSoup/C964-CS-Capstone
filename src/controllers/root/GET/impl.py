from http import HTTPStatus
from flask import Request, Response, render_template
from custom_logging.log_factory.interface import LogFactory as LogFactory_Interface
from .errors import NotSecureError
from .enum import LogKeys, LogVals

class Controller:
    def __init__(self, logger: LogFactory_Interface, template_path: str):
        self.logger=logger
        self.template_path=template_path
    
    # the method for the flask route to use
    def handle(self, req: Request) -> Response:
        try:
            if not req.is_secure:
                raise NotSecureError()
            
            self.logger \
                .create_log() \
                .add_attribute(LogKeys.LOG_ORIGIN, LogVals[LogKeys.LOG_ORIGIN]) \
                .add_attribute(LogKeys.ROUTE, LogVals[LogKeys.ROUTE]) \
                .add_attribute(LogKeys.METHOD, LogVals[LogKeys.METHOD]) \
                .add_attribute(LogKeys.REQUEST, str(req)) \
                .commit() 
            
            return self.template_path
        except Exception as e:
            self.logger \
                .create_log() \
                .add_attribute(LogKeys.LOG_ORIGIN, LogVals[LogKeys.LOG_ORIGIN]) \
                .add_attribute(LogKeys.ROUTE, LogVals[LogKeys.ROUTE]) \
                .add_attribute(LogKeys.METHOD, LogVals[LogKeys.METHOD]) \
                .add_attribute(LogKeys.REQUEST, str(req)) \
                .add_attribute(LogKeys.EXCEPTION_RAISED, f"e={e}") \
                .commit() 
                
            if isinstance(e, NotSecureError):
                return Response(status=HTTPStatus.FORBIDDEN)
            else:
                return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
                