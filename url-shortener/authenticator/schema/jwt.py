import json
from hashlib import sha512
from base64 import urlsafe_b64encode,urlsafe_b64decode
from Crypto.PublicKey import RSA
from marshmallow import Schema, fields, post_dump
from model.jwt import JWTHeader, JWTPayload
from dbmodel import db, jwks

class JWTHeaderSchema(Schema):
    alg = fields.String()
    typ = fields.String()
    kid = fields.String()
    @post_dump
    def json_dump(self, data, **kwargs):
        return json.dumps(data, separators=(",", ":"))


class JWTPayloadSchema(Schema):
    sub = fields.String()
    exp = fields.Integer()

    @post_dump
    def json_dump(self, data, **kwargs):
        return json.dumps(data, separators=(",", ":"))


class JWTSchema(Schema):
    header: JWTHeader = fields.Raw()
    payload: JWTPayload = fields.Raw()

    @post_dump
    def generate_jwt(self, data, **kwargs):
        def fill_b64_padding(b64msg):
            missing_padding = 4 - len(b64msg) % 4
            b64msg += '=' * missing_padding
            return b64msg
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
        # # read key
        jwk = db.session.query(jwks).order_by(jwks.create_date.desc()).first()
        n = int.from_bytes(urlsafe_b64decode(fill_b64_padding(jwk.n)), 'big')
        d = int.from_bytes(urlsafe_b64decode(fill_b64_padding(jwk.d)), 'big')
        # signature
        header_payload = f"{header_b64}.{payload_b64}".encode("utf-8")
        hash = int.from_bytes(sha512(header_payload).digest(), byteorder='big')
        signature = pow(hash, d, n)
        signature_binary = signature.to_bytes((signature.bit_length() + 7) // 8, 'big')
        signature_b64 = urlsafe_b64encode(signature_binary).decode("utf-8").replace("=", "")

        return {"access_token": f"{header_b64}.{payload_b64}.{signature_b64}"}