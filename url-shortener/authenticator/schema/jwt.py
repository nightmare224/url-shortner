import json
import os
from base64 import urlsafe_b64encode
import hashlib
import hmac
from marshmallow import Schema, fields, post_dump
from model.jwt import JWTHeader, JWTPayload


class JWTHeaderSchema(Schema):
    alg = fields.String()
    typ = fields.String()

    @post_dump
    def json_dump(self, data, **kwargs):
        return json.dumps(data, separators=(",", ":"))


class JWTPayloadSchema(Schema):
    sub = fields.String()
    sid = fields.String()
    exp = fields.Integer()

    @post_dump
    def json_dump(self, data, **kwargs):
        return json.dumps(data, separators=(",", ":"))


class JWTSchema(Schema):
    header: JWTHeader = fields.Raw()
    payload: JWTPayload = fields.Raw()

    @post_dump
    def generate_jwt(self, data, **kwargs):
        # header
        header_json = JWTHeaderSchema().dump(data["header"])
        header_b64 = (
            urlsafe_b64encode(header_json.encode("utf-8"))
            .decode("utf-8")
            .replace("=", "")
        )

        # payload
        payload_json = JWTPayloadSchema().dump(data["payload"])
        payload_b64 = (
            urlsafe_b64encode(payload_json.encode("utf-8"))
            .decode("utf-8")
            .replace("=", "")
        )

        # signature
        header_payload = f"{header_b64}.{payload_b64}".encode("utf-8")
        secret = os.environ.get("ACCESS_TOKEN_SECRET").encode("utf-8")
        signature = hmac.new(secret, header_payload, hashlib.sha256).digest()
        signature_b64 = urlsafe_b64encode(signature).decode("utf-8").replace("=", "")

        return {"access_token": f"{header_b64}.{payload_b64}.{signature_b64}"}
