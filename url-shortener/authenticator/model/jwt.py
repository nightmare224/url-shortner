import os
from dataclasses import dataclass
from time import time

@dataclass
class JWTHeader():
    kid: str
    alg: str = "RS1024"
    typ: str = "JWT"

@dataclass
class JWTPayload():
    sub: str
    exp: int = ""
    def __post_init__(self):
        if self.exp == "":
            lifespan = os.environ.get("ACCESS_TOKEN_LIFESPAN")
            self.exp = str(int(time()) + int(lifespan))

@dataclass
class JWT():
    payload: JWTPayload
    header: JWTHeader

@dataclass
class JWK():
    n: str
    e: str
    kid: str
    alg: str = "RS1024"
    kty: str = "RSA"
    use: str = "sig"