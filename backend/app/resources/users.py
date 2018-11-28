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

        create_props = params.copy()
        create_props['password'] = hashed_pwd

        create_props.pop('is_admin', None)
        create_props.pop('is_user_manager', None)

        user = User.create(**create_props)

        return user

    @authorize
    @marshal_with(users_resource_fields)
    def get(self):

        if not g.user.can_update_users:
            abort(401)

        page = int(request.args.get('p', 1))

        query = User.query_active_users()

        result = query.paginate(page, per_page=50, error_out=False)

        return { 'users': result.items }
