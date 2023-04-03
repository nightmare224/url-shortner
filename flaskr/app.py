from flask import Flask, request
from route.url import url_restapi
from route.id import id_restapi


app = Flask(__name__)
app.register_blueprint(url_restapi)
app.register_blueprint(id_restapi)

# @app.route("/")
# def getShortenedURL():
#     shortUrl = "helloworld"
#     return shortUrl


# @app.route("/:<id>", methods=(["GET"]))
# def getIdFromUrl(id):
#     if request.method == "GET":
#         return id, 301
