import os
from Crypto.PublicKey import RSA
from dbmodel import db, jwks
from base64 import urlsafe_b64encode
from datetime import datetime

# filepath=os.path.dirname(os.path.abspath(__file__))

# keypair = RSA.generate(bits=1024)
# with open(f'{filepath}/public_key.pem', 'wb') as f:
#     f.write(keypair.publickey().exportKey(format='PEM'))

# with open(f'{filepath}/private_key.pem', 'wb') as f:
#     f.write(keypair.exportKey(format='PEM'))

def is_jwk_available():
    return db.session.query(jwks).first() is not None

def generate_jwk():
    def encode(val: int):
        val_binary = val.to_bytes((val.bit_length() + 7) // 8, 'big')
        return urlsafe_b64encode(val_binary).decode("utf-8").replace("=", "")
    keypair = RSA.generate(bits=1024)
    jwk = jwks(
        n = encode(keypair.n),
        e = encode(keypair.e),
        d = encode(keypair.d)
    )
    db.session.add(jwk)
    db.session.commit()