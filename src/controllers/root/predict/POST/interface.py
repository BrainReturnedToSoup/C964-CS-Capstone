from marshmallow import Schema, fields, validate
from static.loader import housing_price_dataset_df

BEDROOMS=set(housing_price_dataset_df["Bedrooms"].unique())
BATHROOMS=set(housing_price_dataset_df["Bathrooms"].unique())
NEIGHBORHOOD={}

unique_neighborhoods=list(housing_price_dataset_df["Neighborhood"].unique())
for i in range(0, len(unique_neighborhoods)):
    NEIGHBORHOOD[unique_neighborhoods[i]]=i
class RequestBodySchema(Schema):
    SquareFeet=fields.Integer(required=True)
    Bathrooms=fields.Integer(required=True, validate=validate.OneOf(BATHROOMS))
    Bedrooms=fields.Integer(required=True, validate=validate.OneOf(BEDROOMS))
    Neighborhood=fields.String(required=True, validate=validate.OneOf(NEIGHBORHOOD.keys()))