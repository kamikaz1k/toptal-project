from flask import g, request

from app.models.token import Token


def authorize(*args):

    auth_header = request.headers.get('Authorization')

    user = None
    if auth_header:
        jwt_token = auth_header.replace('Bearer ', "")
        token = Token.find_by_token(jwt_token)
        if token is not None:
            user = token.user

    g.user = user

    method = args[0]
    return method(*args[1:])