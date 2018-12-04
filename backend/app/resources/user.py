from flask import g, request
from flask_restful import abort, fields, marshal_with, Resource

from app.auth import authorize
from app.models.user import User


user_resource_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'name': fields.String,
    'calories_per_day': fields.Integer,
    'active': fields.Boolean(attribute=lambda m: not m.deleted),
    'is_admin': fields.Boolean,
    'is_user_manager': fields.Boolean,
}


class UserResource(Resource):

    method_decorators = [authorize]

    @marshal_with(user_resource_fields, envelope='user')
    def get(self, user_id):

        user = User.query.filter(User.id == user_id).one_or_none()

        if user is None:
            abort(404)

        if user.id != g.user.id and not g.user.can_update_users:
            abort(401)

        return user

    @marshal_with(user_resource_fields, envelope='user')
    def put(self, user_id):

        user = User.query.filter(User.id == user_id).one_or_none()

        if user is None:
            abort(404)

        if user.id != g.user.id and not g.user.can_update_users:
            abort(401)

        props = request.get_json()
        props = props['user']

        if not g.user.can_update_users:
            del props['is_admin']
            del props['is_user_manager']

        user.update(**props)
        user.save()

        return user

    def delete(self, user_id):

        user = User.query.filter(User.id == user_id).one_or_none()

        if user is None:
            abort(404)

        if user.id != g.user.id and not g.user.can_update_users:
            abort(401)

        user.delete()
        user.save()

        return {}
