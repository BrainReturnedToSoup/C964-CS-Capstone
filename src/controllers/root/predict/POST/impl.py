from flask import Request, Response, jsonify
from marshmallow import ValidationError
from custom_logging.log_factory.interface import Log_Factory as Logger_Interface
from services.predict.impl import Predicter

from .interface import RequestBodySchema
from .errors import NotSecureError, InvalidContentTypeError
from .enum import LogKeys, LogVals

# Response constructor is injected so that I can make a mock and make test assertions on the response
class Controller:
    def __init__(self, logger: Logger_Interface, predicter: Predicter, body_schema: RequestBodySchema, response: Response):
        self.logger=logger
        self.predicter=predicter
        self.response=response
        self.body_schema=body_schema
        
    # the method for the flask route to use
    def handle(self, req: Request) -> Response:
        try:
            if not req.is_secure:
                raise NotSecureError()
            
            if not req.is_json:
                raise InvalidContentTypeError()
            
            body=req.get_json()
            
            self.logger \
                .create_log() \
                .add_attribute(LogKeys.log_origin, LogVals[LogKeys.log_origin]) \
                .add_attribute(LogKeys.route, LogVals[LogKeys.route]) \
                .add_attribute(LogKeys.method, LogVals[LogKeys.method]) \
                .add_attribute(LogKeys.request, str(req)) \
                .commit()
            
            # validate the request body schema, this will throw a ValidationError exception if the body does not match the schema
            self.body_schema.load(body)
            
            # run the prediction
            prediction=self.predicter.predict(body)
        
            # return the prediction as part of the response body, 200 OK
            return self.response(response=prediction, content_type="application/json", status=200)
        except Exception as e:
            self.logger \
                .create_log() \
                .add_attribute(LogKeys.log_origin, LogVals[LogKeys.log_origin]) \
                .add_attribute(LogKeys.route, LogVals[LogKeys.route]) \
                .add_attribute(LogKeys.method, LogVals[LogKeys.method]) \
                .add_attribute(LogKeys.request, str(req)) \
                .add_attribute(LogKeys.exception_raised, str(e)) \
                .commit()

            if isinstance(e, NotSecureError):
                return self.response(status=403)
            elif isinstance(e, InvalidContentTypeError):
                return self.response(status=415)
            elif isinstance(e, ValidationError):
                return self.response(status=400)
            else:
                return self.response(status=500)
                    
            
        
        
    
    