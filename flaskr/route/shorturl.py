from flask import Blueprint, jsonify, request
from model.shorturl import ShortURL
from model.url import URL
from schema.shorturl import ShortURLSchema
from schema.url import URLSchema
from model.error import BadRequest, NotFound
# from shortner import getShortURL

shorturl_restapi = Blueprint("shorturl_restapi", __name__)


@shorturl_restapi.route("/", methods=["GET"])
def getId():
    """
    Get all shorten URL.
    ---
    tags:
      - Short URL APIs
    description: Get all shorten URL.
    responses:
        200:
            description: Get a list of shorten URL.
            schema:
                type: array
                items:
                    $ref: '#/definitions/ShortURL'
    """
    shorturl = ShortURL(short_url_id = "15", short_url = "https://shortenurl.group12/15")

    # validation and serialization
    try:
        payload = ShortURLSchema().dump(shorturl)
    except:
        raise BadRequest("Invalid payload.")
    return payload, 200

@shorturl_restapi.route("/", methods=["POST"])
def createId():
    """
    Create shorten URL by passing URL in payload.
    ---
    tags:
      - Short URL APIs
    description: Create shorten URL by passing URL in payload.
    parameters:
      - name: URL
        in: body
        schema:
            $ref: '#/definitions/URL'
    responses:
        201:
            description: Create a shorten URL successed and reponse the shorted URL.
            schema:
                $ref: '#/definitions/ShortURL'
        400:
            description: Invalid URL.
    """
    try:
        request_data = request.get_json()
        url = URLSchema().load(request_data)
    except:
        raise BadRequest("Invalid URL")

    # id = getShortURL(url.url)
    shorturl = ShortURL(short_url_id = "15", short_url = "https://shortenurl.group12/15")
    if not shorturl:
        raise BadRequest("Invalid URL")


    # validation and serialization
    try:
        payload = ShortURLSchema().dump(shorturl)
    except:
        raise BadRequest("Invalid payload.")
    return payload, 201

@shorturl_restapi.route("/", methods=["DELETE"])
def deleteId():
    """
    Delete URL (no such method).
    ---
    tags:
      - Short URL APIs
    description: Delete URL (no such method).
    responses:
        404:
            description: Delete Method Not Found.
    """
    raise NotFound("Delete Method Not Found")
