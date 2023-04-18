import os

port = os.environ.get("AUTHENTICATOR_PORT") if os.environ.get("AUTHENTICATOR_PORT") else 5002
bind = f"0.0.0.0:{port}"
workers = 1
reload = os.environ.get("AUTHENTICATOR_DEBUG") if os.environ.get("AUTHENTICATOR_DEBUG") else False
loglevel = "debug"