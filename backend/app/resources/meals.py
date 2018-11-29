from dateutil.parser import parse
from flask import g, request
from flask_restful import abort, fields, marshal_with, Resource

from app.auth import authorize
from app.models.meal import Meal
from app.resources.meal import meal_resource_fields


meals_resource_fields = {
   'meals': fields.List(fields.Nested(meal_resource_fields))
}


class MealsResource(Resource):

    method_decorators = [authorize]

    @marshal_with(meal_resource_fields, envelope='meal')
    def post(self):
        # who are you?
        current_user = g.user

        params = request.get_json()

        if params is None:
            abort(400, message="invalid params")

        props = params['meal'].copy()
        props['calorie_count'] = props['calories']
        props['owner_user_id'] = current_user.id

        new_meal = Meal.create(**props)

        return new_meal

    @marshal_with(meals_resource_fields)
    def get(self):

        current_user = g.user

        page = int(request.args.get('p', 1))

        keys = [
            'start_datetime',
            'end_datetime',
            'start_time',
            'end_time',
        ]

        query_options = {
            key: request.args.get(key, None)
            for key in keys
        }

        query = Meal.build_date_time_range_query(
            owner_user_id=current_user.id,
            **query_options
        )

        result = query.paginate(page, per_page=10, error_out=False)
        return { 'meals': result.items }
