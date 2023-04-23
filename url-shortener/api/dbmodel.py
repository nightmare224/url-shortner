from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

# init my cool db
db = SQLAlchemy()

# url shortner model class
class url_mapper(db.Model):
    __tablename__ = "url_mapper"
    url_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    short_url_id = db.Column(db.String(2048), unique=True)
    full_url = db.Column(db.String(2048))


class url_user_mapper(db.Model):
    __tablename__ = "url_user_mapper"
    url_id = db.Column(db.Integer, db.ForeignKey("url_mapper.url_id", ondelete="CASCADE"), primary_key=True)
    user_id = db.Column(db.Integer)
    # user_id = db.Column(db.Integer, db.ForeignKey("user_info.user_id", ondelete="CASCADE"))

# url mapper class Schema to serealize
class UrlMapperSchema(Schema):
    url_id = fields.Integer()
    short_url_id = fields.String()
    full_url = fields.String()


# Initialize the schemas
url_mapper_schema = UrlMapperSchema()
