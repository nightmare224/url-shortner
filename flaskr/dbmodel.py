from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.ext.hybrid import hybrid_property


# init my cool db
db = SQLAlchemy()

# init sweet marshmallow
ma = Marshmallow()


# url shortner model class
class URL_MAPPER(db.Model):
    __tablename__ = "URL_MAPPER"
    URL_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    SHORT_URL_ID = db.Column(db.String(7), unique=True)
    SHORT_BASE_URL = db.Column(db.String(200))
    FULL_URL = db.Column(db.String(500))

    def __init__(self, URL_ID, SHORT_URL_ID, SHORT_BASE_URL, FULL_URL):
        self.URL_ID = URL_ID
        self.SHORT_URL_ID = SHORT_URL_ID
        self.SHORT_BASE_URL = SHORT_BASE_URL
        self.FULL_URL = FULL_URL


# url mapper class Schema to serealize
class UrlMapperSchema(ma.Schema):
    class Meta:
        fields = ("URL_ID", "SHORT_URL_ID", "SHORT_BASE_URL", "FULL_URL")


# Initialize the schemas
url_mapper_schema = UrlMapperSchema()
