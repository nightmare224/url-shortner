from flask import Blueprint
from model.error import BadRequest, NotFound

url_restapi = Blueprint("url_restapi", __name__)

@url_restapi.route("/<id>", methods=["GET"])
def getUrlFromId(id):

    return id, 301

@url_restapi.route("/<id>", methods=["PUT"])
def updateUrlFromId(id):


    return id, 200

@url_restapi.route("/<id>", methods=["DELETE"])
def deleteUrlFromId(id):


    return id, 204