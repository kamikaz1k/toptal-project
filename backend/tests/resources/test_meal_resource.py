from email.utils import format_datetime

from dateutil.parser import parse
from nose.tools import eq_, ok_

from app.models.meal import Meal
from tests.resources import BaseResourceTest


class TestMealResource(BaseResourceTest):

    def setup_method(self, method=None):
        super(TestMealResource, self).setup_method()
        self.user = self._create_user()
        self.user_token = self._create_token_for_user(self.user)

    def _create_meal(self, **overrides):
        params = {
            'owner_user_id': self.user.id,
            'text': "yummy yummy",
            'entry_datetime': '2018-11-25T09:00:00',
            'calorie_count': 400,
        }
        params.update(overrides)
        return Meal.create(**params)

    def _create_meal_request_payload(self, **overrides):
        payload = {
            'meal': {
                'owner_user_id': self.user.id,
                'text': "yummy yummy",
                'entry_datetime': "Mon, 26 Nov 2018 04:00:00 -0000",
                'calories': 400,
            }
        }
        payload['meal'].update(overrides)
        return payload

    def test_create_meal(self):
        ENTRY_DATETIME = "Mon, 26 Nov 2018 04:00:00 -0000"
        response = self.test_client.post(
            '/api/meals',
            headers={
                'Authorization': 'Bearer ' + self.user_token.jwt_token
            },
            json={
                'meal': {
                    'owner_user_id': self.user.id,
                    'text': "yummy yummy",
                    'entry_datetime': ENTRY_DATETIME,
                    'calories': 400,
                }
            }
        )

        eq_(response.status_code, 200)
        self.assert_json(
            response.json,
            {
                'meal': {
                    'id': response.json['meal']['id'],
                    'owner_user_id': self.user.id,
                    'text': "yummy yummy",
                    'entry_datetime': ENTRY_DATETIME,
                    'calories': 400,
                }
            }
        )

        meal = Meal.get_by_id(response.json['meal']['id'])
        ok_(meal)
        eq_(
            format_datetime(meal.entry_datetime),
            ENTRY_DATETIME
        )

    def test_get_meal(self):
        meal = self._create_meal()
        response = self.test_client.get(
            '/api/meals/{}'.format(meal.id),
            headers={
                'Authorization': 'Bearer ' + self.user_token.jwt_token
            }
        )

        eq_(response.status_code, 200)
        self.assert_json(
            response.json,
            {
                'meal': {
                    'id': meal.id,
                    'owner_user_id': self.user.id,
                    'text': meal.text,
                    'entry_datetime': format_datetime(meal.entry_datetime),
                    'calories': meal.calorie_count,
                }
            }
        )

    def test_update_meal(self):
        meal = self._create_meal()
        old_meal_text = meal.text
        old_entry_datetime = meal.entry_datetime
        old_calories = meal.calorie_count
        old_owner_user_id = meal.owner_user_id

        new_owner_user_id = 5
        new_text = "Yabadaba doo"
        new_entry_datetime = "Tue, 27 Nov 2018 04:00:00 -0000"
        new_calories = 808

        assert old_meal_text != new_text
        assert old_entry_datetime != new_entry_datetime
        assert old_calories != new_calories
        assert meal.owner_user_id != new_owner_user_id

        update_payload = self._create_meal_request_payload(
            id=meal.id,
            owner_user_id=new_owner_user_id,
            text=new_text,
            entry_datetime=new_entry_datetime,
            calories=new_calories,
        )

        response = self.test_client.put(
            '/api/meals/{}'.format(meal.id),
            headers={
                'Authorization': 'Bearer ' + self.user_token.jwt_token
            },
            json=update_payload
        )

        expected_payload = self._create_meal_request_payload(
            **update_payload['meal']
        )
        expected_payload['meal']['owner_user_id'] = old_owner_user_id

        eq_(response.status_code, 200)
        self.assert_json(
            response.json,
            expected_payload
        )

        meal_record = Meal.get_by_id(meal.id)
        eq_(meal_record.text, new_text)
        eq_(meal_record.calorie_count, new_calories)
        eq_(meal_record.owner_user_id, old_owner_user_id)
        self.assert_datetime(meal_record.entry_datetime, new_entry_datetime)

    def test_delete_meal(self):
        meal = self._create_meal()

        assert meal.deleted_at is None

        response = self.test_client.delete(
            '/api/meals/{}'.format(meal.id),
            headers={
                'Authorization': 'Bearer ' + self.user_token.jwt_token
            }
        )

        eq_(response.status_code, 200)

        meal_record = Meal.query.filter(Meal.id == meal.id).first()
        ok_(meal_record.deleted_at is not None)

    def test_create_meal__unauthd(self):
        response = self.test_client.post(
            '/api/meals',
            json=self._create_meal_request_payload()
        )

        eq_(response.status_code, 401)

    def test_get_meal__different_user(self):
        meal = self._create_meal()
        user_two = self._create_user(email="something@email.com")
        user_two_token = self._create_token_for_user(user_two)

        response = self.test_client.get(
            '/api/meals/{}'.format(meal.id),
            headers={
                'Authorization': 'Bearer ' + user_two_token.jwt_token
            }
        )

        eq_(response.status_code, 401)

    def test_get_meal__different_user_manager_user(self):
        meal = self._create_meal()
        user_two = self._create_user_manager_user(email="something@email.com")
        user_two_token = self._create_token_for_user(user_two)

        response = self.test_client.get(
            '/api/meals/{}'.format(meal.id),
            headers={
                'Authorization': 'Bearer ' + user_two_token.jwt_token
            }
        )

        eq_(response.status_code, 401)

    def test_get_meal__different_admin_user(self):
        meal = self._create_meal()
        user_two = self._create_admin_user(email="something@email.com")
        user_two_token = self._create_token_for_user(user_two)

        response = self.test_client.get(
            '/api/meals/{}'.format(meal.id),
            headers={
                'Authorization': 'Bearer ' + user_two_token.jwt_token
            }
        )

        eq_(response.status_code, 200)

    def test_get_meal__unauthd(self):
        meal = self._create_meal()

        response = self.test_client.get(
            '/api/meals/{}'.format(meal.id)
        )

        eq_(response.status_code, 401)

    def test_update_meal__different_user(self):
        meal = self._create_meal()
        user_two = self._create_user(email="something@email.com")
        user_two_token = self._create_token_for_user(user_two)

        update_payload = self._create_meal_request_payload(id=meal.id)

        response = self.test_client.put(
            '/api/meals/{}'.format(meal.id),
            headers={
                'Authorization': 'Bearer ' + user_two_token.jwt_token
            },
            json=update_payload
        )

        eq_(response.status_code, 401)

    def test_update_meal__different_user_manager_user(self):
        meal = self._create_meal()
        user_two = self._create_user_manager_user(email="something@email.com")
        user_two_token = self._create_token_for_user(user_two)

        update_payload = self._create_meal_request_payload(id=meal.id)

        response = self.test_client.put(
            '/api/meals/{}'.format(meal.id),
            headers={
                'Authorization': 'Bearer ' + user_two_token.jwt_token
            },
            json=update_payload
        )

        eq_(response.status_code, 401)

    def test_update_meal__different_admin_user(self):
        meal = self._create_meal()
        user_two = self._create_admin_user(email="something@email.com")
        user_two_token = self._create_token_for_user(user_two)

        update_payload = self._create_meal_request_payload(id=meal.id)

        response = self.test_client.put(
            '/api/meals/{}'.format(meal.id),
            headers={
                'Authorization': 'Bearer ' + user_two_token.jwt_token
            },
            json=update_payload
        )

        eq_(response.status_code, 200)

    def test_update_meal__unauthd(self):
        meal = self._create_meal()

        update_payload = self._create_meal_request_payload(id=meal.id)

        response = self.test_client.put(
            '/api/meals/{}'.format(meal.id),
            json=update_payload
        )

        eq_(response.status_code, 401)

    def test_delete_meal__different_user(self):
        meal = self._create_meal()
        user_two = self._create_user(email="something@email.com")
        user_two_token = self._create_token_for_user(user_two)

        response = self.test_client.delete(
            '/api/meals/{}'.format(meal.id),
            headers={
                'Authorization': 'Bearer ' + user_two_token.jwt_token
            },
        )

        eq_(response.status_code, 401)

    def test_delete_meal__different_user_manager_user(self):
        meal = self._create_meal()
        user_two = self._create_user_manager_user(email="something@email.com")
        user_two_token = self._create_token_for_user(user_two)

        response = self.test_client.delete(
            '/api/meals/{}'.format(meal.id),
            headers={
                'Authorization': 'Bearer ' + user_two_token.jwt_token
            },
        )

        eq_(response.status_code, 401)

    def test_delete_meal__different_admin_user(self):
        meal = self._create_meal()
        user_two = self._create_admin_user(email="something@email.com")
        user_two_token = self._create_token_for_user(user_two)

        response = self.test_client.delete(
            '/api/meals/{}'.format(meal.id),
            headers={
                'Authorization': 'Bearer ' + user_two_token.jwt_token
            },
        )

        eq_(response.status_code, 200)

    def test_delete_meal__unauthd(self):
        meal = self._create_meal()
        response = self.test_client.delete(
            '/api/meals/{}'.format(meal.id)
        )

        eq_(response.status_code, 401)

    def test_query_meals(self):

        for i in range(15):
            self._create_meal(name="Test Meal #{}".format(i + 1))

        assert Meal.query.count() == 15

        response = self.test_client.get(
            '/api/meals',
            headers={
                'Authorization': 'Bearer ' + self.user_token.jwt_token
            }
        )
        eq_(response.status_code, 200)
        eq_(len(response.json['meals']), 10)

        response = self.test_client.get(
            '/api/meals',
            headers={
                'Authorization': 'Bearer ' + self.user_token.jwt_token
            },
            query_string="p=1"
        )
        eq_(response.status_code, 200)
        eq_(len(response.json['meals']), 10)

        response = self.test_client.get(
            '/api/meals',
            headers={
                'Authorization': 'Bearer ' + self.user_token.jwt_token
            },
            query_string="p=2"
        )
        eq_(response.status_code, 200)
        eq_(len(response.json['meals']), 5)

        response = self.test_client.get(
            '/api/meals',
            headers={
                'Authorization': 'Bearer ' + self.user_token.jwt_token
            },
            query_string="p=3"
        )
        eq_(response.status_code, 200)
        eq_(len(response.json['meals']), 0)

    def test_query_meals__different_user(self):
        self._create_meal()
        user_two = self._create_user(email="something@email.com")
        user_two_token = self._create_token_for_user(user_two)

        response = self.test_client.get(
            '/api/meals',
            headers={
                'Authorization': 'Bearer ' + user_two_token.jwt_token
            },
            query_string="p=2"
        )
        eq_(response.status_code, 200)
        eq_(len(response.json['meals']), 0)

    def test_query_meals__different_user_manager_user(self):
        self._create_meal()
        user_two = self._create_user_manager_user(email="something@email.com")
        user_two_token = self._create_token_for_user(user_two)

        response = self.test_client.get(
            '/api/meals',
            headers={
                'Authorization': 'Bearer ' + user_two_token.jwt_token
            },
            query_string="p=2"
        )
        eq_(response.status_code, 200)
        eq_(len(response.json['meals']), 0)

    def test_query_meals__different_admin_user(self):
        self._create_meal()
        user_two = self._create_admin_user(email="something@email.com")
        user_two_token = self._create_token_for_user(user_two)

        response = self.test_client.get(
            '/api/meals',
            headers={
                'Authorization': 'Bearer ' + user_two_token.jwt_token
            },
            query_string="p=2"
        )
        eq_(response.status_code, 200)
        eq_(len(response.json['meals']), 0)

    def test_query_meals__unauthd(self):
        self._create_meal()
        response = self.test_client.get(
            '/api/meals'
        )

        eq_(response.status_code, 401)
