from flask import Blueprint, jsonify, request
from model.id import ID
from model.url import URL
from model.error import BadRequest, NotFound

url_restapi = Blueprint("url_restapi", __name__)

@url_restapi.route("/<id>", methods=["GET"])
def getUrlFromId(id):

    url = "https://www.youtube.com"

    payload = URL(url = url)
    return jsonify(payload), 301

@url_restapi.route("/<id>", methods=["PUT"])
def updateUrlFromId(id):


    payload = {
        "success": "updated"
    }
    return jsonify(payload), 200

@url_restapi.route("/<id>", methods=["DELETE"])
def deleteUrlFromId(id):


    payload = None
    return jsonify(payload), 204