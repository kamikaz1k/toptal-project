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


def update_user(props, user):
    user.email = props.get('email', user.email)
    user.name = props.get('name', user.name)

    # DELETE to be handled by `delete` method
    # SENTINEL = "NOTHING WAS PASSED"
    # deleted = props.get('deleted', SENTINEL)
    # if deleted is not SENTINEL:
    #     if deleted:
    #         user.delete()
    #     else:
    #         user.reactivate()


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

    @marshal_with(user_resource_fields, envelope='user')
    def put(self, user_id):

        user = User.query.filter(User.id == user_id).one_or_none()

        if user is None:
            abort(404)

        if user.id != g.user.id and not (g.user.is_user_manager() or g.user.is_user_manager()):
            abort(401)

        update_user(request.get_json(), user)
        user.save()

        return user

    def delete(self, user_id):

        user = User.query.filter(User.id == user_id).one_or_none()

        if user is None:
            abort(404)

        if user.id != g.user.id and not (g.user.is_user_manager() or g.user.is_user_manager()):
            abort(401)

        user.delete()
        user.save()

        return {}
