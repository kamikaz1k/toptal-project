from datetime import date, datetime, time, timedelta
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
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

    def test_build_date_time_range_query__time(self):
        start_time = time(11).isoformat()
        end_time = time(13).isoformat()

        self.create_meal(
            entry_datetime=datetime.combine(date.today(), time(9)).isoformat()
        )

        self.create_meal(
            entry_datetime=datetime.combine(date.today(), time(10, 59)).isoformat()
        )
        self.create_meal(
            entry_datetime=datetime.combine(date.today() - timedelta(days=3), time(11)).isoformat()
        )
        self.create_meal(
            entry_datetime=datetime.combine(date.today() - timedelta(days=3), time(12)).isoformat()
        )
        self.create_meal(
            entry_datetime=datetime.combine(date.today(), time(12, 59)).isoformat()
        )
        self.create_meal(
            entry_datetime=datetime.combine(date.today(), time(13)).isoformat()
        )
        self.create_meal(
            entry_datetime=datetime.combine(date.today() + timedelta(days=3), time(13)).isoformat()
        )
        self.create_meal(
            entry_datetime=datetime.combine(date.today(), time(13, 1)).isoformat()
        )

        query = Meal.build_date_time_range_query(
            self.user.id,
            start_time=start_time,
            end_time=end_time
        )

        eq_(len(query.all()), 5)
        eq_(len(Meal.query.all()), 8)

    def test_build_date_time_range_query__time_across_midnight(self):
        start_time = time(23).isoformat()
        end_time = time(1).isoformat()

        self.create_meal(
            entry_datetime=datetime.combine(date.today(), time(2)).isoformat()
        )

        self.create_meal(
            entry_datetime=datetime.combine(date.today(), time(1, 1)).isoformat()
        )
        self.create_meal(
            entry_datetime=datetime.combine(date.today() - timedelta(days=3), time(1)).isoformat()
        )
        self.create_meal(
            entry_datetime=datetime.combine(date.today() - timedelta(days=3), time(0,59)).isoformat()
        )
        self.create_meal(
            entry_datetime=datetime.combine(date.today(), time(23, 1)).isoformat()
        )
        self.create_meal(
            entry_datetime=datetime.combine(date.today(), time(23)).isoformat()
        )
        self.create_meal(
            entry_datetime=datetime.combine(date.today() + timedelta(days=3), time(22, 59)).isoformat()
        )
        self.create_meal(
            entry_datetime=datetime.combine(date.today(), time(0, 0)).isoformat()
        )

        query = Meal.build_date_time_range_query(
            self.user.id,
            start_time=start_time,
            end_time=end_time
        )

        eq_(len(query.all()), 5)
        eq_(len(Meal.query.all()), 8)

    def test_build_date_time_range_query__datetime(self):
        start_datetime = parse('2018-11-26T23:01:52')
        end_datetime = parse('2018-11-27T23:01:52')

        self.create_meal(
            entry_datetime=parse('2018-11-26T23:59:59').isoformat()
        )
        self.create_meal(
            entry_datetime=parse('2018-11-26T00:00:00').isoformat()
        )
        self.create_meal(
            entry_datetime=parse('2018-11-27T00:00:00').isoformat()
        )
        self.create_meal(
            entry_datetime=parse('2018-11-27T23:01:52').isoformat()
        )
        self.create_meal(
            entry_datetime=parse('2018-11-27T23:59:59').isoformat()
        )
        self.create_meal(
            entry_datetime=parse('2018-11-28T00:59:59').isoformat()
        )

        query = Meal.build_date_time_range_query(
            self.user.id,
            start_datetime=start_datetime.isoformat(),
            end_datetime=end_datetime.isoformat()
        )

        eq_(len(query.all()), 3)
        eq_(len(Meal.query.all()), 6)

    def test_meal_query_by_datetime_and_time_range(self):
        start_datetime = parse('2018-11-25T09:00:00')
        end_datetime = parse('2018-11-27T18:00:00')

        start_time = time(11)
        end_time = time(15)

        test_date = parse('2018-11-24T09:00:00').date()
        for d in range(4):
            datetimes = [
                datetime.combine(test_date + relativedelta(days=d), time(0, 0)),
                datetime.combine(test_date + relativedelta(days=d), time(10, 59)),
                datetime.combine(test_date + relativedelta(days=d), time(11, 0)),
                datetime.combine(test_date + relativedelta(days=d), time(12, 59)),
                datetime.combine(test_date + relativedelta(days=d), time(14, 59)),
                datetime.combine(test_date + relativedelta(days=d), time(15, 0)),
                datetime.combine(test_date + relativedelta(days=d), time(15, 59)),
                datetime.combine(test_date + relativedelta(days=d), time(23, 59))
            ]

            for idx, data_datetime in enumerate(datetimes):
                self.create_meal(
                    text="Test Meal {}-{}".format(d + 1, idx + 1),
                    entry_datetime=data_datetime.isoformat()
                )


        result = Meal.build_date_time_range_query(
            self.user.id,
            start_datetime=start_datetime.isoformat(),
            end_datetime=end_datetime.isoformat(),
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat()
        )

        eq_(len(result.all()), 12)
        eq_(len(Meal.query.all()), 32)
