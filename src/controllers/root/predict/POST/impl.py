from flask import Request, Response
from http import HTTPStatus
import json
from marshmallow import ValidationError
from custom_logging.log_factory.interface import LogFactory as LogFactory_Interface
from services.predicter.monte_carlo.interface import MonteCarlo as MonteCarlo_Interface
from .interface import RequestBody, ResponseBody
from .errors import NotSecureError, InvalidContentTypeError
from .enums import LogKeys, LogVals

# Response constructor is injected so that I can make a mock and make test assertions on the response
class Controller:
    def __init__(self, logger: LogFactory_Interface, monte_carlo_predicter: MonteCarlo_Interface):
        self.logger=logger
        self.monte_carlo_predicter=monte_carlo_predicter
        self.request_body_schema=RequestBody() # init here to persist and reuse the instance
        
    # the method for the flask route to use
    def handle(self, req: Request) -> Response:
        try:
            if not req.is_secure:
                raise NotSecureError()
            
            if not req.is_json:
                raise InvalidContentTypeError()
            
            request_body=json.loads(req.get_json())
            
            self.logger \
                .create_log() \
                .add_attribute(LogKeys.LOG_ORIGIN, LogVals[LogKeys.LOG_ORIGIN]) \
                .add_attribute(LogKeys.ROUTE, LogVals[LogKeys.ROUTE]) \
                .add_attribute(LogKeys.METHOD, LogVals[LogKeys.METHOD]) \
                .add_attribute(LogKeys.REQUEST, str(req)) \
                .add_attribute("request_body", request_body) \
                .commit()
            
            # validate the request body schema, this will throw a ValidationError exception if the body does not match the schema
            self.request_body_schema.load(request_body)
            
            # run the prediction
            prediction=self.monte_carlo_predicter.predict(request_body, num_of_samples=100)
            
            response_body:ResponseBody={
                "price_predictions": prediction["price_predictions"],
                "noisy_inputs": prediction["noisy_inputs"]
            }
            
            response_body:str=json.dumps(obj=response_body)
        
            # return the prediction as part of the response body, 200 OK
            return Response(response=response_body, content_type="application/json", status=HTTPStatus.OK)
        except Exception as e:
            self.logger \
                .create_log() \
                .add_attribute(LogKeys.LOG_ORIGIN, LogVals[LogKeys.LOG_ORIGIN]) \
                .add_attribute(LogKeys.ROUTE, LogVals[LogKeys.ROUTE]) \
                .add_attribute(LogKeys.METHOD, LogVals[LogKeys.METHOD]) \
                .add_attribute(LogKeys.REQUEST, str(req)) \
                .add_attribute(LogKeys.EXCEPTION_RAISED, str(e)) \
                .commit()

            if isinstance(e, NotSecureError):
                return Response(status=HTTPStatus.FORBIDDEN)
            elif isinstance(e, InvalidContentTypeError):
                return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
            elif isinstance(e, ValidationError):
                return Response(status=HTTPStatus.BAD_REQUEST)
            else:
                return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
                    
            
        
        
    
    