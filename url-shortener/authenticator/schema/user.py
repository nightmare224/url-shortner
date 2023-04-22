from re import match
from marshmallow import (
    Schema,
    fields,
    post_load
)
from model.user import User, UserPwd

class UserSchema(Schema):
    username = fields.String()
    password = fields.String()

    # deserialization
    @post_load
    def __post_load__(self, data, **kwargs):
        return User(**data)
    
class UserPwdSchema(UserSchema):
    new_password = fields.String()

    # deserialization
    @post_load
    def __post_load__(self, data, **kwargs):
        return UserPwd(**data)