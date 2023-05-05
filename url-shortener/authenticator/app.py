import os
from flask import Flask
from flasgger import Swagger, APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from route.user import user_restapi
from route.error_controller import error_controller
from schema.user import UserSchema, UserPwdSchema
from dbmodel import db
from lib.jwks import generate_jwk, is_jwk_available

app = Flask(__name__, instance_relative_config=True)

app.config.from_mapping(
    # SQLALCHEMY_DATABASE_URI="postgresql://postgres:efreet224@localhost:5432/postgres",
    SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI"),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)
db.app = app
db.init_app(app)
# create table in database
with app.app_context():
    db.create_all()
    # jwks init
    if not is_jwk_available():
        generate_jwk()

# For Documatation (flasgger configuration)
spec = APISpec(
    title="Authenticator APIs",
    version="1.0.0",
    openapi_version="2.0",
    plugins=[
        FlaskPlugin(),
        MarshmallowPlugin(),
    ]
)
template = spec.to_flasgger(app, definitions=[UserSchema, UserPwdSchema])
app.config["SWAGGER"] = {
    "static_url_path": "/users/flasgger_static",
    "specs_route": "/users/apidocs/",
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/users/apispec_1.json",
        }
    ],
}
swagger = Swagger(app, template=template)

app.register_blueprint(error_controller)
app.register_blueprint(user_restapi)