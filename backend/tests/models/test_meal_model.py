from datetime import datetime, timedelta
from nose.tools import eq_, ok_

from app.models.meal import Meal
from app.models.user import User
from tests import BaseDatabaseTestCase


class TestMeal(BaseDatabaseTestCase):

    def create_meal(self, **options):
        props = dict(
            owner_user_id=self.user.id,
            text="Greatest Meal Ever",
            entry_datetime=datetime.now(),
            calorie_count=9001,
        )
        props.update(options)
        return Meal(**props)

    def setup(self):
        super(TestMeal, self).setup()
        self.user = User(
            email="test@email.org",
            password="23k12n312n31nl13bj5",
            name="Slim Jim"
        )
        self.user.save()

    def test_meal_get_by_id(self):
        meal = self.create_meal()
        meal.save()

        queried_meal = Meal.get_by_id(meal.id)

        eq_(queried_meal.id, meal.id)
        eq_(queried_meal.owner_user_id, meal.owner_user_id)
        eq_(queried_meal.text, meal.text)
        eq_(queried_meal.calorie_count, meal.calorie_count)
        eq_(queried_meal.entry_datetime, meal.entry_datetime)

        meal.delete()
        meal.save()

        queried_meal = Meal.get_by_id(meal.id)
        assert queried_meal is None

    def test_meal_delete(self):
        meal = self.create_meal()
        assert meal.deleted_at is None

        meal.delete()
        ok_(meal.deleted_at is not None)

    def test_meal_save(self):
        meal = self.create_meal()

        assert Meal.query.all() == []

        meal.save()

        meals = Meal.query.all()

        eq_(meals[0].owner_user_id, meal.owner_user_id)
        eq_(meals[0].text, meal.text)
        eq_(meals[0].entry_datetime, meal.entry_datetime)
        eq_(meals[0].calorie_count, meal.calorie_count)
