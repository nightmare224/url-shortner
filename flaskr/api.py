from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def getShortenedURL():
    shortUrl = "helloworld"
    return shortUrl


@app.route("/:<id>", methods=(["GET"]))
def getIdFromUrl(id):
    if request.method == "GET":
        return id, 301
