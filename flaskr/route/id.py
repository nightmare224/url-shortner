from flask import Blueprint, jsonify, request
from model.id import ID
from model.url import URL
from model.error import BadRequest, NotFound
from shortner import getShortURL


id_restapi = Blueprint("id_restapi", __name__)


@id_restapi.route("/", methods=["GET"])
def getId():

    id = "123"
    # id = 123 # this raise exception, the type has to be string

    payload = ID(id = id)
    return jsonify(payload), 200


@id_restapi.route("/", methods=["POST"])
def createId():

    try:
        request_data = request.get_json()
        url_obj = URL(**request_data)
    except:
        raise BadRequest("Invalid URL")


    id = getShortURL(url_obj.url)
    if not id:
        raise BadRequest("Invalid URL")

    payload = ID(id = id)
    return jsonify(payload), 201

@id_restapi.route("/", methods=["DELETE"])
def deleteId():

    raise NotFound("Delete Method Not Found")
