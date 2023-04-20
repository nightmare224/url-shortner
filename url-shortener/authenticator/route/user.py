from flask import Blueprint, jsonify, request
from model.user import User
from model.jwt import JWTPayload, JWT
from model.error import BadRequest, NotFound, Conflict, Forbidden
from schema.user import UserSchema
from schema.jwt import JWTSchema
from marshmallow import ValidationError
from lib.dbquery import is_user_exist, add_user, authenticate_user

user_restapi = Blueprint("user_restapi", __name__)


@user_restapi.route("/users", methods=["POST"])
def create_user():
    """
    Create a new user with username and password.
    ---
    tags:
      - Users APIs
    parameters:
      - name: User
        in: body
        schema:
            $ref: '#/definitions/User'
    description: Create a new user with username and password.
    responses:
        201:
            description: Create new user success.
            schema:
                $ref: '#/definitions/User'
        409:
            description: The user have already existed.
    """
    try:
        request_data = request.get_json()
        user = UserSchema().load(request_data)
    except ValidationError:
        raise BadRequest("Invalid payload.")

    if is_user_exist(user.username):
        raise Conflict("The user with same username already existed.")

    add_user(user.username, user.password)

    return jsonify({}), 201


@user_restapi.route("/users/login", methods=["POST"])
def login_user():
    """
    User login with username and password.
    ---
    tags:
      - Users APIs
    parameters:
      - name: User
        in: body
        schema:
            $ref: '#/definitions/User'
    description: User login with username and password.
    responses:
        200:
            description: Login success, return JWT.
            schema:
                $ref: '#/definitions/User'
        403:
            description: Login failed.
    """
    try:
        request_data = request.get_json()
        user = UserSchema().load(request_data)
    except ValidationError:
        raise BadRequest("Invalid payload.")

    if not authenticate_user(user.username, user.password):
        raise Forbidden("Invalid username or password.")

    jwt = JWT(
        payload = JWTPayload(
            sub = "1",
            sid = "12"
        )
    )

    payload = JWTSchema().dump(jwt)
    return jsonify(payload), 200