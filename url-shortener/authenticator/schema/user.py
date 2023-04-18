from re import match
from marshmallow import (
    Schema,
    fields,
    post_load
)
from model.user import User
from urllib.parse import urlparse, urlunparse

class UserSchema(Schema):
    username = fields.String()
    password = fields.String()

    # deserialization
    @post_load
    def __post_load__(self, data, **kwargs):
        return FullURL(**data)