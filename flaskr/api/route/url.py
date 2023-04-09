from flask import Blueprint, jsonify, request
from model.url import FullURL
from model.shorturl import ShortURL
from model.error import BadRequest, NotFound
from schema.url import FullURLSchema
from schema.shorturl import ShortURLSchema
from marshmallow import ValidationError
from shortner import (
    query_url_mapping,
    update_full_url,
    delete_short_url,
    is_full_url_not_found,
    is_short_url_id_not_found
)

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
                $ref: '#/definitions/FullURL'
        404:
            description: Short URL ID not found.
    """
    if is_short_url_id_not_found(short_url_id):
        raise NotFound("Short URL ID not found.")

    url_mapping = query_url_mapping(short_url_id = short_url_id)
    full_url = FullURL(full_url=url_mapping["full_url"])
    short_url = ShortURL(
        short_url_id=url_mapping["short_url_id"],
        short_url=f"{url_mapping['short_base_url']}/{url_mapping['short_url_id']}",
    )

    payload = FullURLSchema().dump(full_url)
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
      - name: FullURL
        in: body
        schema:
            $ref: '#/definitions/FullURL'
    description: Get all shorten URL.
    responses:
        200:
            description: Updated succeed.
        400:
            description: Invalid payload.
        404:
            description: Short URL ID not found.
    """
    
    try:
        request_data = request.get_json()
        full_url = FullURLSchema().load(request_data)
    except ValidationError:
        raise BadRequest("Invalid payload.")
    
    if is_short_url_id_not_found(short_url_id):
        raise NotFound("Short URL ID not found.")

    # the mapping of full url to short url already existed
    if not is_full_url_not_found(full_url.full_url):
        # get the exist mapping and delete (ignore if same)
        url_mapping_old = query_url_mapping(full_url = full_url.full_url)
        if url_mapping_old["short_url_id"] != short_url_id:
            delete_short_url(url_mapping_old["short_url_id"])

    # update mapping
    _ = update_full_url(short_url_id, full_url.full_url)

    # query the update result
    url_mapping = query_url_mapping(full_url = full_url.full_url)
    short_url = ShortURL(
        short_url_id=url_mapping["short_url_id"],
        short_url=f"{url_mapping['short_base_url']}/{url_mapping['short_url_id']}",
    )

    payload = FullURLSchema().dump(full_url)
    payload.update(ShortURLSchema().dump(short_url))
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
    if is_short_url_id_not_found(short_url_id):
        raise NotFound("Short URL ID not found.")
    else:
        delete_short_url(short_url_id)
        return jsonify({}), 204
