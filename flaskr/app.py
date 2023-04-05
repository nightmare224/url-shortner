from flask import Flask
from flasgger import Swagger
from route.url import url_restapi
from route.id import id_restapi
from route.error_controller import error_controller


app = Flask(__name__)
# For Documatation
swagger = Swagger(app)

app.register_blueprint(url_restapi)
app.register_blueprint(id_restapi)
app.register_blueprint(error_controller)