from dateutil.parser import parse
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

        datetime = params.get('datetime') # utc datetime
        datetime = parse(datetime)

        new_meal = Meal(
            owner_user_id=current_user.id,
            text=params.get('text', ""),
            entry_datetime=datetime,
            calorie_count=params.get('calories')
        )

        Meal.query.session.add(new_meal)
        Meal.query.session.commit()

        return new_meal

    @marshal_with(meals_resource_fields)
    def get(self):

        current_user = g.user
        # for later
        # parser = reqparse.RequestParser()
        page = int(request.args.get('p', 1))

        query = Meal.query.filter(
            Meal.owner_user_id == current_user.id,
            Meal.deleted_at.is_(None)
        )

        result = query.paginate(page, per_page=50, error_out=False)
        return { 'meals': result.items }

