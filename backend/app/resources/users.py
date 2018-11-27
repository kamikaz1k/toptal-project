import bcrypt
from flask import g, request
from flask_restful import abort, fields, marshal_with, Resource

from app.auth import authorize
from app.models.role import Role, RoleNames
from app.models.user import User
from app.resources.user import user_resource_fields


users_resource_fields = {
    'users': fields.List(fields.Nested(user_resource_fields))
}


class UsersResource(Resource):
    @marshal_with(user_resource_fields, envelope='user')
    def post(self):
        # get request parameters
        params = request.get_json()

        if params is None:
            abort(400)

        params = params['user']

        # get users by email
        existing = User.query.filter(User.email == params['email']).count()

        if existing > 0:
            print("{} exists already...".format(params['email']))
            # if user exists, throw
            abort(http_status_code=409, message="{} exists already".format(params['email']))

        password = params['password']
        hashed_pwd = bcrypt.hashpw(password, bcrypt.gensalt())

        # else create
        user = User(
            name=params['name'],
            email=params['email'],
            password=hashed_pwd
        )

        user_role = Role.get_user_role()
        user.roles.append(user_role)

        User.query.session.add(user)
        User.query.session.commit()

        return user

    @authorize
    @marshal_with(users_resource_fields)
    def get(self):

        if not g.user.is_admin() and not g.user.is_user_manager():
            abort(401)

        query = User.query
        # pagination
        # query.paginate(page, per_page=50, error_out=False)
        return { 'users': query.all() }
