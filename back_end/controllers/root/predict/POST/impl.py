from flask import Request, Response
from http import HTTPStatus
import json
from marshmallow import ValidationError
from back_end.custom_logging.log_factory.interface import LogFactory as LogFactory_Interface
from back_end.services.predictor.monte_carlo.interface import MonteCarlo as MonteCarlo_Interface
from .interface import RequestBody, ResponseBody
from .errors import NotSecureError, InvalidContentTypeError
from .enums import LogKeys, LogVals

# Response constructor is injected so that I can make a mock and make test assertions on the response
class Controller:
    def __init__(self, logger: LogFactory_Interface, monte_carlo_predictor: MonteCarlo_Interface, num_of_samples: int):
        self.logger=logger
        self.monte_carlo_predictor=monte_carlo_predictor
        self.num_of_samples=num_of_samples
        self.request_body_schema=RequestBody() # init here to persist and reuse the instance
        
    # the method for the flask route to use
    def handle(self, req: Request) -> Response:
        try:
            if not req.is_secure:
                raise NotSecureError()
            
            if not req.is_json:
                raise InvalidContentTypeError()
            
            request_body=req.get_json()
            
            self.logger \
                .create_log() \
                .add_attribute(LogKeys.LOG_ORIGIN.value, LogVals[LogKeys.LOG_ORIGIN.value]) \
                .add_attribute(LogKeys.ROUTE.value, LogVals[LogKeys.ROUTE.value]) \
                .add_attribute(LogKeys.METHOD.value, LogVals[LogKeys.METHOD.value]) \
                .add_attribute(LogKeys.REQUEST.value, f"req={req.__repr__()}") \
                .add_attribute(LogKeys.REQUEST_BODY.value, request_body) \
                .commit()
            
            # validate the request body schema, this will throw a ValidationError exception if the body does not match the schema
            self.request_body_schema.load(request_body)
            
            # run the prediction
            prediction=self.monte_carlo_predictor.predict(request_body, num_of_samples=self.num_of_samples)
            
            
            
            response_body:ResponseBody={
                "price_predictions": prediction["price_predictions"],
                "gaussian_noisy_square_feet": prediction["gaussian_noisy_square_feet"]
            }
            
            response_body_jsonified:str=json.dumps(obj=response_body)
        
            # return the prediction as part of the response body, 200 OK
            return Response(response=response_body_jsonified, content_type="application/json", status=HTTPStatus.OK)
        except Exception as e:
            self.logger \
                .create_log() \
                .add_attribute(LogKeys.LOG_ORIGIN.value, LogVals[LogKeys.LOG_ORIGIN.value]) \
                .add_attribute(LogKeys.ROUTE.value, LogVals[LogKeys.ROUTE.value]) \
                .add_attribute(LogKeys.METHOD.value, LogVals[LogKeys.METHOD.value]) \
                .add_attribute(LogKeys.REQUEST.value, f"req={req.__repr__()}") \
                .add_attribute(LogKeys.EXCEPTION_RAISED.value, f"e={e.__repr__()}") \
                .commit()

            if isinstance(e, NotSecureError):
                return Response(status=HTTPStatus.FORBIDDEN)
            elif isinstance(e, InvalidContentTypeError):
                return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
            elif isinstance(e, ValidationError):
                return Response(status=HTTPStatus.BAD_REQUEST)
            else:
                return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
                    
            
        
        
    
    