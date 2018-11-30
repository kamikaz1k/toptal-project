from nose.tools import eq_

from app.resources.user import User
from tests.resources import BaseResourceTest

class TestUserResource(BaseResourceTest):

    def _create_user(self, **overrides):
        options = {
            'email': "regularuser@regularuser.com",
            'name': "regularuser",
            'password': "123123123"
        }
        options.update(overrides)
        return User.create(**options)

    def test_create_user(self):
        result = self.test_client.post(
            '/api/users',
            json={
                'user': {
                    'email': "regularuser@regularuser.com",
                    'password': "123123",
                    'name': "usrmgr3"
                }
            }
        )

        eq_(result.status_code, 200)
        self.assert_json(
            result.json,
            {
                'user': {
                    'id': 1,
                    'email': 'regularuser@regularuser.com',
                    'name': 'usrmgr3',
                    'calories_per_day': 0,
                    'active': True,
                    'is_admin': False,
                    'is_user_manager': False
                }
            }
        )

    def test_create_user__no_password(self):
        result = self.test_client.post(
            '/api/users',
            json={
                "user": {
                    "email": "regularuser@regularuser.com",
                    "name": "usrmgr3"
                }
            }
        )

        eq_(result.status_code, 400)
        eq_(result.json, { "msg": "no password provided" })

    def test_create_user__email_taken(self):
        EMAIL = "regularuser@regularuser.com"

        self._create_user(email=EMAIL)
        result = self.test_client.post(
            '/api/users',
            json={
                "user": {
                    "email": EMAIL,
                    "password": "123123",
                    "name": "usrmgr3"
                }
            }
        )

        eq_(result.status_code, 409)
        eq_(result.json, { "msg": "no password provided" })

