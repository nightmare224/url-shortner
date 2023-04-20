from functools import wraps
from flask import request
from hashlib import sha512
from Crypto.PublicKey import RSA
from model.error import Forbidden
from base64 import urlsafe_b64decode
from time import time
import json

def require_login(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if verify_token():
            return func(*args, **kwargs)
        else:
            raise Forbidden("Invalid access token.")
        
    return decorated
    
def verify_token(token = None):
    access_token = retrive_token() if token is None else token
    if access_token is None:
        return False
    
    with open('key/public_key.pem','r') as f:
        public_key = RSA.import_key(f.read())
    
    # get the hash value from header and payload
    header, payload, signature = access_token.split('.')
    header_payload = f"{header}.{payload}".encode("utf-8")
    hash = int.from_bytes(sha512(header_payload).digest(), byteorder='big')

    # get hash value from signature and public key
    _, payload, signature = decode_token(access_token)
    hash_from_signature = pow(signature, public_key.e, public_key.n)
    # verify signature
    if hash != hash_from_signature:
        return False
    
    # expiration time verify
    if int(time()) > payload["exp"]:
        return False

    # valid token
    return True

def decode_token(token = None):
    access_token = retrive_token() if token is None else token
    header, payload, signature = access_token.split('.')
    header_decode = json.loads(urlsafe_b64decode(fill_b64_padding(header)))
    payload_decode = json.loads(urlsafe_b64decode(fill_b64_padding(payload)))
    signature_decode = int.from_bytes(urlsafe_b64decode(fill_b64_padding(signature)), 'big')

    return (header_decode, payload_decode, signature_decode)

def fill_b64_padding(b64msg):
    missing_padding = 4 - len(b64msg) % 4
    b64msg += '=' * missing_padding
    return b64msg

def retrive_token() -> str:
    # check field in header
    header = request.headers
    if "Authorization" not in header:
        return None
    
    # check schema
    if not header["Authorization"].lower().startswith("bearer "):
        return None
    else:
        _, token = header["Authorization"].split()
        return token
