import os
from flask import Blueprint, request
from model.shorturl import ShortURL
from model.url import FullURL, URL
from schema.shorturl import ShortURLSchema
from schema.url import FullURLSchema, URLSchema
from model.error import BadRequest, NotFound, InternalServer
from lib.dbquery import query_url_mapping, create_short_url, is_full_url_not_found
from lib.authenticator import require_login, decode_token

shorturl_restapi = Blueprint("shorturl_restapi", __name__)

@shorturl_restapi.route("/", methods=["GET"])
@require_login
def get_short_url_api():
    """
    Get all shorten URL.
    ---
    tags:
      - Short URL APIs
    description: Get all URL information.
    parameters:
      - in: header
        name: Authorization
        required: true
        type: string
        description: The format is `Bearer <access_token>`.
    responses:
        200:
            description: Get a list of URL information.
            schema:
                type: array
                items:
                    $ref: '#/definitions/URL'
        403:
            description: Invalid access token.
    """
    # get user_id from token
    _, token_payload, _ = decode_token()
    user_id = token_payload["sub"]

    payload = []
    url_mapping_all = query_url_mapping(user_id = user_id)
    short_base_url = os.environ.get("BASE_URL_FOR_SHORT_URL")
    for url_mapping in url_mapping_all:
        url = URL(
            short_url_id=url_mapping["short_url_id"],
            short_url=f"{short_base_url}/{url_mapping['short_url_id']}",
            full_url=url_mapping["full_url"]
        )
        payload.append(URLSchema().dump(url))

    return payload, 200


@shorturl_restapi.route("/", methods=["POST"])
@require_login
def create_short_url_api():
    """
    Create shorten URL by passing a full URL in the payload.
    ---
    tags:
      - Short URL APIs
    description: Create shorten URL by passing a full URL in the payload.
    parameters:
      - in: header
        name: Authorization
        required: true
        type: string
        description: The format is `Bearer <access_token>`.
      - name: FullURL
        in: body
        schema:
            $ref: '#/definitions/FullURL'
    responses:
        201:
            description: Create a shorten URL successed and reponse the shorted URL.
            schema:
                $ref: '#/definitions/ShortURL'
        400:
            description: Invalid payload.
        403:
            description: Invalid access token.
    """
    try:
        request_data = request.get_json()
        full_url = FullURLSchema().load(request_data)
    except:
        raise BadRequest("Invalid payload.")

    # get user_id from token
    _, token_payload, _ = decode_token()
    user_id = token_payload["sub"]

    # the mapping of full url to short url already existed
    if not is_full_url_not_found(full_url.full_url, user_id):
        raise BadRequest("The URL already has short URL.")

    url_mapping = create_short_url(full_url.full_url, user_id)
    short_base_url = os.environ.get("BASE_URL_FOR_SHORT_URL")
    data = ShortURL(
        short_url_id=url_mapping["short_url_id"],
        short_url=f"{short_base_url}/{url_mapping['short_url_id']}",
    )
    
    payload = ShortURLSchema().dump(data)
    return payload, 201


@shorturl_restapi.route("/", methods=["DELETE"])
@require_login
def delete_short_url_api():
    """
    Delete URL (no such method).
    ---
    tags:
      - Short URL APIs
    description: Delete URL (no such method).
    parameters:
      - in: header
        name: Authorization
        required: true
        type: string
        description: The format is `Bearer <access_token>`.
    responses:
        403:
            description: Invalid access token.
        404:
            description: Delete method not found.
    """
    raise NotFound("Delete method not found")
