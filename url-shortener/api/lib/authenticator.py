from functools import wraps
from flask import request
from model.error import Forbidden

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
        #TODO: User public key to verify the token, if valid return true
        return True
    

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
