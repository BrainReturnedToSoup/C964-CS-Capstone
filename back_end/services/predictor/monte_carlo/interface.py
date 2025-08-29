from typing import List, TypedDict
from abc import ABC, abstractmethod
from marshmallow import Schema, fields, validate, post_load, ValidationError
from ..interface import PredictionInput, PredictionOutput


class MonteCarloOutput(TypedDict):
    # the following output lists should be indexed matched
    price_predictions: List[PredictionOutput]
    gaussian_noisy_square_feet: List[float] # noisy Square feet values essentially

class ConstructorArgs(Schema):
    seed=fields.Integer(required=True, validate=validate.Range(min=0, max=None))
    noise_std=fields.Integer(required=True, validate=validate.Range(min=0, max=None))
    num_of_samples_min=fields.Integer(required=True, validate=validate.Range(min=1, max=None))
    num_of_samples_max=fields.Integer(required=True)
        
    @post_load
    def validate_samples_max(self, data, many, **kwargs):
        if data["num_of_samples_max"] < data["num_of_samples_min"]:
            raise ValidationError("'num_of_samples_max' must be greater than or equal to 'num_of_samples_min'")
       
        return data

class PredictArgs(Schema):
    input=fields.Nested(nested=PredictionInput, required=True)
    num_of_samples=fields.Integer(required=True)
    
    def __init__(self, num_of_samples_min: int, num_of_samples_max: int, *args, **kwargs):
        self.num_of_samples_min=num_of_samples_min
        self.num_of_samples_max=num_of_samples_max
        
        super().__init__(*args, **kwargs) 
         # the schema should initialize given the supplied min and max it expects. This allows the constructor arg 
         # schema to be reused, since 'ConstructorArgs'a nd 'PredictArgs' are part of the same class 
    
    # with the initial schema loaded, do the range check
    @post_load
    def validate_num_of_samples(self, data, many, **kwargs):
        num_of_samples=data["num_of_samples"]
        
        if num_of_samples > self.num_of_samples_max or num_of_samples < self.num_of_samples_min:
            raise ValidationError("'num_of_samples' must be within the defined min-max range")

class MonteCarlo(ABC):
    @abstractmethod    
    def predict(self, input: PredictionInput, num_of_samples: int) -> MonteCarloOutput:
        pass