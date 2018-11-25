from dateutil.parser import parse
from flask import g, request
from flask_restful import abort, fields, marshal_with, Resource

from app.auth import authorize
from app.models.user import User


user_resource_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'name': fields.String,
    'deleted': fields.Boolean
}


class UserResource(Resource):

    method_decorators = [authorize]

    @marshal_with(user_resource_fields, envelope='user')
    def get(self, user_id):

        user = User.query.filter(User.id == user_id).one_or_none()

        if user is None:
            abort(404)

        if user.id != g.user.id and not (g.user.is_user_manager() or g.user.is_user_manager()):
            abort(401)

        return user
