from marshmallow import Schema, fields, post_load
from model.shorturl import ShortURL

class ShortURLSchema(Schema):
    short_url_id = fields.String()
    short_url = fields.String()
    # deserialization
    @post_load
    def __post_load__(self, data, **kwargs):
        return ShortURL(**data)