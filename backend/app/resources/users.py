from flask import request
from flask_restful import abort, Resource

from app.models.user import User


class UsersResource(Resource):
    def post(self):
        # get request parameters
        params = request.get_json()

        # get users by email
        existing = User.query.filter(User.email == params['email']).count()

        if existing > 0:
            print("{} exists already...".format(params['email']))
            # if user exists, throw
            abort(http_status_code=409, message="{} exists already".format(params['email']))

        # else create
        user = User(
            name=params['name'],
            email=params['email'],
            password=params['password']
        )

        User.query.session.add(user)
        User.query.session.commit()

        return {
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'password': user.password
            }
        }