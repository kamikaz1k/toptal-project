from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from nose.tools import eq_, ok_

from app.models.meal import Meal
from app.models.user import User
from tests import BaseDatabaseTestCase


class TestMeal(BaseDatabaseTestCase):

    def create_meal(self, **options):
        props = dict(
            owner_user_id=self.user.id,
            text="Greatest Meal Ever",
            entry_datetime=datetime.now().isoformat(),
            calorie_count=9001,
        )
        props.update(options)
        return Meal.create(**props)

    def setup(self):
        super(TestMeal, self).setup()

        self.user = User(
            email="test@email.org",
            password="23k12n312n31nl13bj5",
            name="Slim Jim"
        )
        self.user.save()

    def test_meal_create(self):
        DATETIME = datetime.now().replace(microsecond=0)
        meal = Meal.create(
            owner_user_id=self.user.id,
            text="Greatest Meal Ever",
            entry_datetime=DATETIME.isoformat(),
            calorie_count=9001
        )

        meal = Meal.get_by_id(meal.id)

        eq_(meal.owner_user_id, self.user.id)
        eq_(meal.text, "Greatest Meal Ever")
        eq_(meal.entry_datetime, DATETIME)
        eq_(meal.entry_time, DATETIME.time())
        eq_(meal.entry_date, DATETIME.date())
        eq_(meal.calorie_count, 9001)

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

        eq_(meal.text, "Greatest Meal Ever")

        meal.text = "Not Greatest Meal Ever"
        meal.save()

        meals = Meal.query.all()

        eq_(meals[0].owner_user_id, meal.owner_user_id)
        eq_(meals[0].text, "Not Greatest Meal Ever")
        eq_(meals[0].entry_datetime, meal.entry_datetime)
        eq_(meals[0].calorie_count, meal.calorie_count)

    def test_meal_update(self):

        meal = self.create_meal()

        new_text = "It could be any meal"
        new_entry_datetime = datetime.now() + timedelta(days=5)
        new_entry_datetime = new_entry_datetime.replace(microsecond=0)
        new_calories = 9090

        meal.update(
            text=new_text,
            entry_datetime=new_entry_datetime.isoformat(),
            calorie_count=new_calories,
        )

        queries_meal = Meal.get_by_id(meal.id)

        eq_(queries_meal.owner_user_id, meal.owner_user_id)
        eq_(queries_meal.text, new_text)
        eq_(queries_meal.entry_datetime, new_entry_datetime)
        eq_(queries_meal.calorie_count, new_calories)

    def test_meal_query_by_date_range(self):

        start_date = datetime.now().date() - timedelta(days=10)
        end_date = start_date + timedelta(days=20)

        for i in range(5):
            entry_datetime = datetime.now() + timedelta(days=3 * i)
            self.create_meal(
                text="Include Meal {}".format(i + 1),
                entry_datetime=entry_datetime.isoformat()
            )

        result = Meal.query_by_date_time_range(
            self.user.id,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat()
        )

        eq_(len(result), 4)
        eq_(len(Meal.query.all()), 5)

    def test_meal_query_by_time_range(self):

        start_time = datetime.now() - relativedelta(hours=8)
        end_time = start_time + relativedelta(hours=16)

        for i in range(9):
            entry_datetime = datetime.now() + relativedelta(hours=3 * i - 10)
            self.create_meal(
                text="Include Meal {}".format(i + 1),
                entry_datetime=entry_datetime.isoformat()
            )

        start_time = start_time.time().replace(microsecond=0).isoformat()
        end_time = end_time.time().replace(microsecond=0).isoformat()
        result = Meal.query_by_date_time_range(
            self.user.id,
            start_time=start_time,
            end_time=end_time
        )

        eq_(len(result), 6)
        eq_(len(Meal.query.all()), 9)

    def test_meal_query_by_date_time_range(self):
        start_date = datetime.now().date() - timedelta(days=5)
        end_date = datetime.now().date() + timedelta(days=5)

        start_time = datetime.now() - relativedelta(hours=2)
        end_time = datetime.now() + relativedelta(hours=2)
        start_time = start_time.replace(microsecond=0)
        end_time = end_time.replace(microsecond=0)

        for d in range(3):
            for t in range(3):
                entry_date = start_date + timedelta(days=(7 * d) + 1)
                entry_time = start_time + relativedelta(hours=(4 * t) + 2)

                entry_datetime = datetime.combine(entry_date, entry_time.time())
                self.create_meal(
                    text="Test Meal {}-{}".format(d + 1, t + 1),
                    entry_datetime=entry_datetime.isoformat()
                )

        start_time = start_time.time().replace(microsecond=0)
        end_time = end_time.time().replace(microsecond=0)

        result = Meal.query_by_date_time_range(
            self.user.id,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat()
        )

        eq_(len(result), 2)
        eq_(len(Meal.query.all()), 9)
