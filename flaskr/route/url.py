from flask import Blueprint, jsonify, request
from model.url import URL
from model.error import BadRequest, NotFound
from schema.url import URLSchema
from marshmallow import ValidationError
from shortner import getUrlFromId

url_restapi = Blueprint("url_restapi", __name__)

@url_restapi.route("/<id>", methods=["GET"])
def getUrl(id):
    url = URL(url = getUrlFromId(id))
    try:
        payload = URLSchema().dump(url)
    except ValidationError:
        raise BadRequest("Invalid payload.")
    else:
        return payload, 301

@url_restapi.route("/<id>", methods=["PUT"])
def updateUrlFromId(id):
    try:
        url = request.get_json()
        URLSchema().dump(url)
        # call function of shortner.py
    except ValidationError:
        raise BadRequest("Invalid payload.")
    except:
        raise NotFound("Invalid ID.")
    else:
        payload = {"updated": "true"}
        return jsonify(payload), 200

@url_restapi.route("/<id>", methods=["DELETE"])
def deleteUrlFromId(id):
    try:
        pass
        # call function of shortner.py
    except:
        raise NotFound("Invalid ID.")
    else:
        payload = {"deleted": "true"}
        return jsonify(payload), 204