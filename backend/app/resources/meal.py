from flask import g, request
from flask_restful import abort, fields, marshal_with, Resource

from app.auth import authorize
from app.models.meal import Meal


meal_resource_fields = {
    'id': fields.Integer,
    'owner_user_id': fields.Integer,
    'text': fields.String,
    'entry_datetime': fields.DateTime(dt_format='iso8601'),
    'calories': fields.Integer(attribute='calorie_count')
}


class MealResource(Resource):

    method_decorators = [authorize]

    @marshal_with(meal_resource_fields, envelope='meal')
    def get(self, meal_id):

        meal = Meal.query.filter(
            Meal.id == meal_id
        ).one_or_none()

        if meal is None:
            abort(404)

        if meal.owner_user_id != g.user.id:
            abort(401)

        return meal