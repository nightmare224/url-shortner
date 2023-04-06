from flask import Flask
from flasgger import Swagger, APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from route.url import url_restapi
from route.shorturl import shorturl_restapi
from route.error_controller import error_controller
from schema.shorturl import ShortURLSchema
from schema.url import URLSchema
import os
from dbmodel import db


app = Flask(__name__, instance_relative_config=True)

app.config.from_mapping(
    SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI"),
    # SQLALCHEMY_DATABASE_URI="postgresql://postgresadmin:admin123@127.0.0.1:5432/postgres",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)
db.app = app
db.init_app(app)

# For Documatation (flasgger configuration)
spec = APISpec(
    title="Shorten URL APIs",
    version="1.0.0",
    openapi_version="2.0",
    plugins=[
        FlaskPlugin(),
        MarshmallowPlugin(),
    ],
)
template = spec.to_flasgger(app, definitions=[ShortURLSchema, URLSchema])
swagger = Swagger(app, template=template)

app.register_blueprint(url_restapi)
app.register_blueprint(shorturl_restapi)
app.register_blueprint(error_controller)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
