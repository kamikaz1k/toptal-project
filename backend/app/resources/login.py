from builtins import dict
from datetime import datetime, timedelta

import bcrypt
import jwt
from flask import current_app, request
from flask_restful import abort, Resource

from app.models.user import User
from app.models.token import Token


class LoginResource(Resource):
    def post(self):
        # get request parameters
        params = request.get_json()

        assert params['email']
        assert params['password']

        # get users by email
        existing_user = User.query.filter(User.email == params['email']).one_or_none()

        if existing_user is None or not bcrypt.checkpw(params['password'], existing_user.password):
            print("username and password do not match")
            # if user does not exist, throw
            abort(http_status_code=400, message="username and password do not match")

        password = params['password']
        hashed_pwd = bcrypt.hashpw(password, bcrypt.gensalt())

        # else create
        expiry = datetime.now() + timedelta(days=30)
        jwt_token = jwt.encode(
            dict(
                email=existing_user.email,
                roles={
                    'is_user_manager': existing_user.is_user_manager(),
                    'is_admin': existing_user.is_admin()
                },
                exp=round(expiry.timestamp())),
            current_app.config['JWT_SECRET']
        )
        token = Token(user_id=existing_user.id, jwt_token=jwt_token, expires_on=expiry)

        User.query.session.add(token)
        User.query.session.commit()

        return { 'token': token.jwt_token }