from flask import request
from flask_restful import abort, Resource

from app.models.user import User
from app.models.token import Token


class LoginResource(Resource):
    def post(self):
        # get request parameters
        params = request.get_json()

        if 'email' not in params or 'password' not in params:
            abort(400, msg="missing email and password")

        existing_user = User.find_by_credentials(
            email=params['email'],
            password=params['password']
        )

        if existing_user is None:
            abort(401, msg="username and password do not match")

        token = Token.create(existing_user)

        return {'token': token.jwt_token}
