from dateutil.parser import parse
from flask import g, request
from flask_restful import abort, Resource

from app.auth import authorize
from app.models.meal import Meal


class MealsResource(Resource):

    method_decorators = [authorize]

    def post(self):
        # who are you?
        user = g.user

        params = request.get_json()

        if params is None:
            abort(400, message="invalid params")

        date = params.get('date')
        time = params.get('time')

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

        return {
            'meal': {
                'id': new_meal.id,
                'owner_user_id': new_meal.owner_user_id,
                'text': new_meal.text,
                'entry_datetime': new_meal.entry_datetime,
                'calories': new_meal.calorie_count
            }
        }