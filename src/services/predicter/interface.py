from abc import ABC, abstractmethod
from typing import TypedDict
from marshmallow import Schema, fields, validate
from static.loader import housing_price_dataset_df

# not enums, because enums doesn't allow referencing iteratible value fields
# and iterating over them.
BEDROOMS=set(housing_price_dataset_df["Bedrooms"].unique())
BATHROOMS=set(housing_price_dataset_df["Bathrooms"].unique())

NEIGHBORHOOD={}
unique_neighborhoods=list(housing_price_dataset_df["Neighborhood"].unique())
for i in range(0, len(unique_neighborhoods)):
    NEIGHBORHOOD[unique_neighborhoods[i]]=i

class PredictionInput(Schema):
    SquareFeet=fields.Integer(required=True)
    Bathrooms=fields.Integer(required=True, validate=validate.OneOf(BATHROOMS))
    Bedrooms=fields.Integer(required=True, validate=validate.OneOf(BEDROOMS))
    Neighborhood=fields.String(required=True, validate=validate.OneOf(NEIGHBORHOOD.keys()))

# no need for a schema because it's outbound; a return value of the functionality within
# the given critical path.
class PredictionOutput(TypedDict):
    price_prediction: float

class Predicter(ABC):
    @abstractmethod
    def predict(self, input: PredictionInput) -> PredictionOutput:
        pass