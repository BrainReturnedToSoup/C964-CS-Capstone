from abc import ABC, abstractmethod
from typing import TypedDict
from marshmallow import Schema, fields, validate

SQUARE_FEET_RANGE=[1000,2999]
BEDROOMS=frozenset([2,3,4,5])
BATHROOMS=frozenset([1,2,3])
NEIGHBORHOOD={
    "Rural": int(0),
    "Suburb": int(1),
    "Urban": int(2)
}

class PredictionInput(Schema):
    SquareFeet=fields.Integer(required=True)
    Bathrooms=fields.Integer(required=True, validate=validate.OneOf(BATHROOMS))
    Bedrooms=fields.Integer(required=True, validate=validate.OneOf(BEDROOMS))
    Neighborhood=fields.String(required=True, validate=validate.OneOf(NEIGHBORHOOD.keys()))

# no need for a schema because it's outbound; a return value of the functionality within
# the given critical path.
class PredictionOutput(TypedDict):
    price_prediction: float

class Preprocessor(ABC):
    pass
class Predicter(ABC):
    @abstractmethod
    def predict(self, input: PredictionInput) -> PredictionOutput:
        pass