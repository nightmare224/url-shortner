import json
from hashlib import sha512
from base64 import urlsafe_b64encode,urlsafe_b64decode
from Crypto.PublicKey import RSA
from marshmallow import Schema, fields, post_dump, post_load
from model.jwt import JWTHeader, JWTPayload, JWK
from dbmodel import db, Jwks

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
        
        # read key
        jwk = db.session.query(Jwks).order_by(Jwks.create_date.desc()).first()
        n = int.from_bytes(urlsafe_b64decode(fill_b64_padding(jwk.n)), 'big')
        d = int.from_bytes(urlsafe_b64decode(fill_b64_padding(jwk.d)), 'big')
        # signature
        header_payload = f"{header_b64}.{payload_b64}".encode("utf-8")
        hash_token = int.from_bytes(sha512(header_payload).digest(), byteorder='big')
        signature = pow(hash_token, d, n)
        signature_binary = signature.to_bytes((signature.bit_length() + 7) // 8, 'big')
        signature_b64 = urlsafe_b64encode(signature_binary).decode("utf-8").replace("=", "")

        return {"access_token": f"{header_b64}.{payload_b64}.{signature_b64}"}

class JWKSchema(Schema):
    n = fields.String()
    e = fields.String()
    kid = fields.String()
    alg = fields.String()
    kty = fields.String()
    use = fields.String()

    # deserialization
    @post_load
    def __post_load__(self, data, **kwargs):
        return JWK(**data)