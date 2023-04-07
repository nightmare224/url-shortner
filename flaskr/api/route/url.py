from flask import Blueprint, jsonify, request
from model.url import URL
from model.shorturl import ShortURL
from model.error import BadRequest, NotFound
from schema.url import URLSchema
from schema.shorturl import ShortURLSchema
from marshmallow import ValidationError
from shortner import (
    query_url_mapping,
    update_full_url,
    delete_short_url,
    is_full_url_not_found,
)
from sqlalchemy.orm.exc import UnmappedInstanceError

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
        name: short_url_id
        type: string
        required: true
        description: The result of Base 62 encode of URL ID
    description: Get all shorten URL.
    responses:
        301:
            description: Get the full URL.
            schema:
                $ref: '#/definitions/URL'
    """
    try:
        url_mapping = query_url_mapping(short_url_id = short_url_id)
    except:
        raise NotFound("Short URL ID not found.")
    url = URL(url=url_mapping["full_url"])
    short_url = ShortURL(
        short_url_id=url_mapping["short_url_id"],
        short_url=f"{url_mapping['short_base_url']}/{url_mapping['short_url_id']}",
    )

    payload = URLSchema().dump(url)
    payload.update(ShortURLSchema().dump(short_url))
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
        name: short_url_id
        type: string
        required: true
        description: The result of Base 62 encode of URL ID
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
        # the mapping of full url to short url already existed
        if not is_full_url_not_found(url.url):
            raise BadRequest("The URL already has short URL.")
        result = update_full_url(short_url_id, url.url)

    except ValidationError:
        raise BadRequest("Invalid payload.")
    except UnmappedInstanceError:
        raise NotFound("Invalid ID.")
    else:
        payload = {"updated": "true", "id": result}
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
        name: short_url_id
        type: string
        required: true
        description: The result of Base 62 encode of URL ID
    description: Get all shorten URL.
    responses:
        204:
            description: Delete succeed.
        404:
            description: Short URL ID not found.
    """
    try:
        delete_short_url(short_url_id)
    except UnmappedInstanceError:
        raise NotFound("Invalid ID.")
    else:
        return jsonify({}), 204
