from marshmallow import Schema, fields

class RequestBodySchema(Schema):
    SquareFeet=fields.Integer(required=True)
    Bathrooms=fields.Integer(required=True)
    Bedrooms=fields.Integer(required=True)
    Neighborhood=fields.String(required=True)