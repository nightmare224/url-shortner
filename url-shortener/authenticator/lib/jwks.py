from Crypto.PublicKey import RSA
from dbmodel import db, Jwks, JWKSSchema
from base64 import urlsafe_b64encode

def is_jwk_available():
    return db.session.query(Jwks).first() is not None

def query_latest_kid() -> str:
    # read key
    jwk = db.session.query(Jwks).order_by(Jwks.create_date.desc()).first()

    return str(jwk.kid)

def query_jwks() -> list:
    result = []
    kid_list = db.session.query(Jwks.kid).all()
    for kid in kid_list:
        jwk = Jwks.query.get(kid)
        result.append(JWKSSchema().dump(jwk))
    return result

def generate_jwk():
    def encode(val: int):
        val_binary = val.to_bytes((val.bit_length() + 7) // 8, 'big')
        return urlsafe_b64encode(val_binary).decode("utf-8").replace("=", "")
    keypair = RSA.generate(bits=1024)
    jwk = Jwks(
        n = encode(keypair.n),
        e = encode(keypair.e),
        d = encode(keypair.d)
    )
    db.session.add(jwk)
    db.session.commit()