from flask import Blueprint, jsonify, request
from model.user import User
from model.jwt import JWTPayload, JWT
from model.error import BadRequest, NotFound, Conflict, Forbidden
from schema.user import UserSchema, UserPwdSchema
from schema.jwt import JWTSchema
from marshmallow import ValidationError
from lib.dbquery import (
    is_user_exist,
    add_user,
    authenticate_user,
    query_user_info,
    update_user_password,
)

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
        409:
            description: The user already existed.
    """
    try:
        request_data = request.get_json()
        user = UserSchema().load(request_data)
    except ValidationError:
        raise BadRequest("Invalid payload.")

    if is_user_exist(user.username):
        raise Conflict("The user already existed.")

    add_user(user.username, user.password)

    return jsonify({"create": "success"}), 201


@user_restapi.route("/users", methods=["PUT"])
def update_user():
    """
    Update the user password.
    ---
    tags:
      - Users APIs
    parameters:
      - name: User
        in: body
        schema:
            $ref: '#/definitions/UserPwd'
    description: Create a new user with username and password.
    responses:
        200:
            description: Update user password success.
        403:
            description: Invalid username or password.
    """
    try:
        request_data = request.get_json()
        user = UserPwdSchema().load(request_data)
    except ValidationError:
        raise BadRequest("Invalid payload.")

    if not authenticate_user(user.username, user.password):
        raise Forbidden("Invalid username or password.")

    update_user_password(user.username, user.new_password)

    return jsonify({"update": "success"}), 200


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
            description: Login success, return access token.
            schema:
                required:
                    - access_token
                properties:
                    access_token:
                        type: string
                        example: eyJhbGciOiJSUzEwMjQiLCJ0eXAiOiJKV1QifQ.eyJleHAiOjE2ODIwMTY4MjQsInN1YiI6IjMifQ.MViPBWVYtnOnc8iQfroltUF6uSdDcQPN5qLCqkkbXXzfe3yzldA5ZZ4lW4H3kpKlnguYiJnUNw_G454G0N2XYJQ9TWQzWkjLw07dvbKvLcIDyXro7wkjw9N9WCMVYDj9wGwGwzcoj3q26cMaBvYNz5GxAoTjQNcgFMAMlsAKWaU
                        description: access token
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

    # retrieve user info
    user_info = query_user_info(user.username)
    jwt = JWT(payload=JWTPayload(sub=user_info["user_id"]))
    payload = JWTSchema().dump(jwt)
    return jsonify(payload), 200
