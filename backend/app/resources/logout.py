from datetime import datetime

from flask import request
from flask_restful import abort, Resource

from app.auth import extract_token_from_request
from app.models.token import Token


class LogoutResource(Resource):
    def post(self):
        # get request parameters
        jwt_token = extract_token_from_request(request)

        # find token
        token = Token.query.filter(
            Token.jwt_token == jwt_token,
            Token.revoked_on.is_(None)
        ).one_or_none()

        # if it exists, revoke it
        if token is None:
            abort(http_status_code=400, message="token invalid")

        if token.expires_on <= datetime.now():
            token.revoke()
            abort(http_status_code=401, message="token expired")
            # but it's already expired?
            # will be useful for refresh_token hook later

        token.revoke()

        return {}
