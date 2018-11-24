from functools import wraps

from flask import g, request
from flask_restful import abort

from app.models.token import Token


def authorize(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        user = None
        if auth_header:
            jwt_token = auth_header.replace('Bearer ', "")
            token = Token.find_by_token(jwt_token)
            if token is not None:
                user = token.user

        if user is None:
            abort(401)

        g.user = user

        return func(*args, **kwargs)

    return wrapper