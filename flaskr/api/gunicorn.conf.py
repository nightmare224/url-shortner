import os

port = os.environ.get("API_PORT") if os.environ.get("API_PORT") else 5001
bind = f"0.0.0.0:{port}"
workers = 1
reload = os.environ.get("API_DEBUG") if os.environ.get("API_DEBUG") else False
loglevel = "debug"