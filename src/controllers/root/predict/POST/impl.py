from flask import Request, Response, jsonify
from marshmallow import ValidationError
from logging.log_factory.interface import Log_Factory as Logger_Interface
from services.predict.impl import Predicter
from .interface import RequestBodySchema
class Controller:
    def __init__(self, logger: Logger_Interface, predicter: Predicter, response: Response, body_schema: RequestBodySchema):
        self.logger=logger
        self.predicter=predicter
        self.response=response
        self.body_schema=body_schema
        
    # the method for the flask route to use
    def handle(self, req: Request) -> Response:
        try:
            # check for proper request content type (necessary for the body)
            content_type = req.headers.get("Content-Type")
        
            if not content_type or "application/json" not in content_type:
                raise Exception(f"controllers.root.predict.POST.impl.Controller.handle():invalid content type:expected={'application/json'}:received={content_type}")
            
            req_json=req.get_json()
            
            self.logger \
                .create_log() \
                .add_attribute("log-origin", "route=/predict:method=POST") \
                .add_attribute("request-body-json", req_json) \
                .commit()
            
            # validate the request body schema
            self.body_schema.load(req_json)
            
            # run the prediction
            prediction=self.predicter.predict(req_json)
        
            # return the prediction as part of the response body, 200 OK
            return self.response(response=jsonify(prediction), content_type="application/json", status=200)
        except Exception as e:
            self.logger \
                .create_log() \
                .add_attribute("log-origin", "route=/predict:method=POST" ) \
                .add_attribute("exception-raised", str(e)) \
                .commit()

            if isinstance(e, ValidationError):
                return self.response(status=400)
            else:
                return self.response(status=500)
                    
            
        
        
    
    