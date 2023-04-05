from marshmallow import Schema, fields, post_load
from model.id import ID

class IDSchema(Schema):
    id = fields.String()

    # deserialization
    @post_load
    def __post_load__(self, data, **kwargs):
        return ID(**data)