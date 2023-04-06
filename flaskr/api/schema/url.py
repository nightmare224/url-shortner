from marshmallow import Schema, fields, post_load
from model.url import URL

class URLSchema(Schema):
    url = fields.Url()

    # deserialization
    @post_load
    def __post_load__(self, data, **kwargs):
        return URL(**data)