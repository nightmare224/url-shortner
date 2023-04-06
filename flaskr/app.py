from flask import Flask
from flasgger import Swagger, APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from route.url import url_restapi
from route.shorturl import shorturl_restapi
from route.error_controller import error_controller
from schema.shorturl import ShortURLSchema
from schema.url import URLSchema


app = Flask(__name__)

# For Documatation (flasgger configuration)
spec = APISpec(
    title='Shorten URL APIs',
    version='1.0.0',
    openapi_version='2.0',
    plugins=[
        FlaskPlugin(),
        MarshmallowPlugin(),
    ],
)
template = spec.to_flasgger(app, definitions=[ShortURLSchema, URLSchema])
swagger = Swagger(app, template = template)

app.register_blueprint(url_restapi)
app.register_blueprint(shorturl_restapi)
app.register_blueprint(error_controller)