from marshmallow import Schema, fields, validate
from abc import ABC
from abc import ABC, abstractmethod
from .static import housing_price_dataset_df

BEDROOMS=set(housing_price_dataset_df["Bedrooms"].unique())
BATHROOMS=set(housing_price_dataset_df["Bathrooms"].unique())
NEIGHBORHOOD={}

unique_neighborhoods=list(housing_price_dataset_df["Neighborhood"].unique())
for i in range(0, len(unique_neighborhoods)):
    NEIGHBORHOOD[unique_neighborhoods[i]]=i
class Prediction_Input(Schema):
    SquareFeet=fields.Integer(required=True)
    Bathrooms=fields.Integer(required=True, validate=validate.OneOf(BATHROOMS))
    Bedrooms=fields.Integer(required=True, validate=validate.OneOf(BEDROOMS))
    Neighborhood=fields.String(required=True, validate=validate.OneOf(NEIGHBORHOOD.keys()))
class Prediction_Output():
    PricePrediction: float
class Predicter(ABC):
    @abstractmethod
    def predict(input: Prediction_Input) -> Prediction_Output:
        pass