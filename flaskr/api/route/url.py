from flask import Blueprint, jsonify, request
from model.url import URL
from model.error import BadRequest, NotFound
from schema.url import URLSchema
from marshmallow import ValidationError
from shortner import query_full_url, delete_short_url
# from shortner import update_full_url

url_restapi = Blueprint("url_restapi", __name__)


@url_restapi.route("/<short_url_id>", methods=["GET"])
def get_url(short_url_id):
    """
    Get the full URL through short URL ID.
    ---
    tags:
      - Full URL APIs
    parameters:
      - in: path
        name: Short URL ID
        type: string
        required: true
    description: Get all shorten URL.
    responses:
        301:
            description: Get the full URL.
            schema:
                $ref: '#/definitions/URL'
    """
    url = URL(url=query_full_url(short_url_id))
    try:
        payload = URLSchema().dump(url)
    except ValidationError:
        raise BadRequest("Invalid payload.")
    else:
        return payload, 301


@url_restapi.route("/<short_url_id>", methods=["PUT"])
def update_url(short_url_id):
    """
    Update the mapping of short URL ID and full URL.
    ---
    tags:
      - Full URL APIs
    parameters:
      - in: path
        name: Short URL ID
        type: string
        required: true
      - name: URL
        in: body
        schema:
            $ref: '#/definitions/URL'
    description: Get all shorten URL.
    responses:
        200:
            description: Updated succeed.
        400:
            description: Invalid input.
        404:
            description: Short URL ID not found.
    """
    try:
        request_data = request.get_json()
        url = URLSchema().load(request_data)
        # result = update_full_url(short_url_id, url.url)
        result = None
    except ValidationError:
        raise BadRequest("Invalid payload.")
    except KeyError:
        raise NotFound("Invalid ID.")
    else:
        payload = {"deleted": "true", "id": result}
        return jsonify(payload), 200


@url_restapi.route("/<short_url_id>", methods=["DELETE"])
def delete_url(short_url_id):
    """
    Delete the mapping of short URL ID and full URL.
    ---
    tags:
      - Full URL APIs
    parameters:
      - in: path
        name: Short URL ID
        type: string
        required: true
    description: Get all shorten URL.
    responses:
        204:
            description: Delete succeed.
        404:
            description: Short URL ID not found.
    """
    try:
        result = delete_short_url(short_url_id)
    except KeyError:
        raise NotFound("Invalid ID.")
    else:
        payload = {"deleted": "true", "id": result}
        return jsonify(payload), 204
