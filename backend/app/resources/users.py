from flask import g, request
from flask_restful import abort, fields, marshal_with, Resource

from app.auth import authorize, authorize_if_token_available
from app.models.user import User
from app.resources.user import user_resource_fields


users_resource_fields = {
    'users': fields.List(fields.Nested(user_resource_fields))
}


class UsersResource(Resource):

    @authorize_if_token_available
    @marshal_with(user_resource_fields, envelope='user')
    def post(self):
        # get request parameters
        params = request.get_json()

        if params is None:
            abort(400)

        params = params['user']

        # get users by email -- doesn't check for active
        existing = User.query.filter(User.email == params['email']).count()

        if existing > 0:
            abort(409, message="{} exists already".format(params['email']))

        if 'password' not in params:
            abort(400, msg="no password provided")

        create_props = params.copy()

        if g.user is None or not g.user.can_update_users:
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

        return {'users': result.items}
