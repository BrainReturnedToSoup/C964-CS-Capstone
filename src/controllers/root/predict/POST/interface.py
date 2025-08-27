from marshmallow import Schema, fields, validate
from typing import TypedDict, List

SQUARE_FEET_RANGE=[1000,2999]
BEDROOMS=frozenset([2,3,4,5])
BATHROOMS=frozenset([1,2,3])
NEIGHBORHOOD={
    "Rural": int(0),
    "Suburb": int(1),
    "Urban": int(2)
}

class RequestBody(Schema):
    SquareFeet=fields.Integer(required=True, validate=validate.Range(min=1, max=None))
    Bathrooms=fields.Integer(required=True, validate=validate.OneOf(BATHROOMS))
    Bedrooms=fields.Integer(required=True, validate=validate.OneOf(BEDROOMS))
    Neighborhood=fields.String(required=True, validate=validate.OneOf(NEIGHBORHOOD.keys()))

class ResponseBody(TypedDict):
    # the following output lists should be indexed matched
    price_predictions: List[float]
    noisy_inputs: List[float] # noisy Square feet values essentially