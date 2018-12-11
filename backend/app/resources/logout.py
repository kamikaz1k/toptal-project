from flask import request
from flask_restful import Resource

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

        if token:
            token.revoke()

        return {}
