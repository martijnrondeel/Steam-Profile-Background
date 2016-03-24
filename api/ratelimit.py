from flask import request
from flask_limiter import Limiter


def getIP():
    """Returns IP from user behind proxy, needed for rate-limiting"""
    return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)


def Enable(app):
    limiter = Limiter(
        app,
        key_func=getIP)
    return limiter
