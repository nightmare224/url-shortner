from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


# init my cool db
db = SQLAlchemy()

# init sweet marshmallow
ma = Marshmallow()


# url shortner model class
class user_info(db.Model):
    __tablename__ = "user_info"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(256), unique=True)
    password = db.Column(db.String(256))