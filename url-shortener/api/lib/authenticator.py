from functools import wraps
from flask import request
from hashlib import sha512
from Crypto.PublicKey import RSA
from model.error import Forbidden
from base64 import urlsafe_b64decode

def require_login(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if verify_token():
            return func(*args, **kwargs)
        else:
            raise Forbidden("Invalid access token.")
        
    return decorated
    
def verify_token():
    access_token = retrive_token()
    if access_token is None:
        return False
    else:
        with open('key/public_key.pem','r') as f:
            public_key = RSA.import_key(f.read())
        
        # get the hash value from header and payload
        header, payload, signature = access_token.split('.')
        header_payload = f"{header}.{payload}".encode("utf-8")
        hash = int.from_bytes(sha512(header_payload).digest(), byteorder='big')

        # get hash value from signature and public key
        signature = urlsafe_b64decode(fill_b64_padding(signature))
        signature_decimal = int.from_bytes(signature, 'big')
        hash_from_signature = pow(signature_decimal, public_key.e, public_key.n)

        # same hash value means valid token
        return hash == hash_from_signature
    
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
