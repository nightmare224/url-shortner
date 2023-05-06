from flask import Blueprint, jsonify, request
from lib.jwks import query_jwks, generate_jwk
from schema.jwt import JWKSchema
from model.jwt import JWK

auth_restapi = Blueprint("auth_restapi", __name__)


@auth_restapi.route("/auth/.well-known/configuration", methods=["GET"])
def get_auth_config():
    """
    Get authenticator well known configuration.
    ---
    tags:
      - Auth APIs
    description: Get authenticator well known configuration.
    responses:
        200:
            description: Get configuration success.
    """
    payload = []
    for jwk in query_jwks():
        jwk = JWK(
            kid = jwk["kid"],
            n = jwk["n"],
            e = jwk["e"]
        )
        payload.append(
            JWKSchema().dump(jwk)
        )

    return jsonify(payload), 200

@auth_restapi.route("/auth/jwk", methods=["POST"])
def refresh_jwk():
    """
    Generate new Json Web Key.
    ---
    tags:
      - Auth APIs
    description: Generate new Json Web Key.
    responses:
        200:
            description: Generate new key success.
    """
    generate_jwk()

    return jsonify({"create": "success"}), 201