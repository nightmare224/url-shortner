from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from datetime import datetime

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

class jwks(db.Model):
    __tablename__ = "jwks"
    kid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    n = db.Column(db.String(1024), nullable=False)
    e = db.Column(db.String(1024), nullable=False)
    d = db.Column(db.String(1024), nullable=False)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class JWKSSchema(Schema):
    kid = fields.Integer()
    n = fields.String()
    e = fields.String()
    d = fields.String()
    create_date = fields.DateTime()