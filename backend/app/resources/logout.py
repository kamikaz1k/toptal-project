from datetime import datetime

from flask import request
from flask_restful import abort, Resource

from app.models.token import Token


class LogoutResource(Resource):
    def post(self):
        # get request parameters
        auth = request.headers.get('Authorization')
        jwt_token = auth.replace('Bearer ', "")

        # find token
        existing = Token.query.filter(
            Token.jwt_token == jwt_token,
            Token.revoked_on.is_(None)
        ).one_or_none()

        # if it exists, revoke it
        if existing is None:
            abort(http_status_code=400, message="token invalid")

        if existing.expires_on <= datetime.now():
            existing.revoked_on = datetime.now()
            Token.query.session.add(existing)
            Token.query.session.commit()
            abort(http_status_code=401, message="token expired")
            # but it's already expired?
            # will be useful for refresh_token hook later

        existing.revoked_on = datetime.now()
        Token.query.session.add(existing)
        Token.query.session.commit()

        return {}