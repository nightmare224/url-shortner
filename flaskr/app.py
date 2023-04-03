from flask import Flask
from route.url import url_restapi
from route.id import id_restapi
from route.error_controller import error_controller


app = Flask(__name__)


app.register_blueprint(url_restapi)
app.register_blueprint(id_restapi)
app.register_blueprint(error_controller)


# @app.route("/")
# def getShortenedURL():
#     shortUrl = "helloworld"
#     return shortUrl


# @app.route("/:<id>", methods=(["GET"]))
# def getIdFromUrl(id):
#     if request.method == "GET":
#         return id, 301
