from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

# init my cool db
db = SQLAlchemy()

# url shortner model class
class user_info(db.Model):
    __tablename__ = "user_info"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(256), unique=True)
    password = db.Column(db.String(256))


class UserInfoSchema(Schema):
    user_id = fields.Integer()
    username = fields.String()
    password = fields.String()