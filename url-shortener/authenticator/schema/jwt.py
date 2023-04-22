import json
from hashlib import sha512
from base64 import urlsafe_b64encode
from Crypto.PublicKey import RSA
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
        with open('key/private_key.pem','r') as f:
            private_key = RSA.import_key(f.read())
        header_payload = f"{header_b64}.{payload_b64}".encode("utf-8")
        hash = int.from_bytes(sha512(header_payload).digest(), byteorder='big')
        signature = pow(hash, private_key.d, private_key.n)
        signature_binary = signature.to_bytes((signature.bit_length() + 7) // 8, 'big')
        signature_b64 = urlsafe_b64encode(signature_binary).decode("utf-8").replace("=", "")

        return {"access_token": f"{header_b64}.{payload_b64}.{signature_b64}"}