from nose.tools import eq_, ok_

from app.models.token import Token
from app.models.user import User
from tests.resources import BaseResourceTest


class TestUserResource(BaseResourceTest):

    def setup(self):
        super(TestUserResource, self).setup()

    def _create_user(self, **overrides):
        options = {
            'email': "regularuser@regularuser.com",
            'name': "regularuser",
            'password': "123123123"
        }
        options.update(overrides)
        return User.create(**options)

    def _create_token_for_user(self, user):
        return Token.create(user)

    def test_create_user(self):
        response = self.test_client.post(
            '/api/users',
            json={
                'user': {
                    'email': "regularuser@regularuser.com",
                    'password': "123123",
                    'name': "usrmgr3"
                }
            }
        )

        eq_(response.status_code, 200)
        self.assert_json(
            response.json,
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
        response = self.test_client.post(
            '/api/users',
            json={
                "user": {
                    "email": "regularuser@regularuser.com",
                    "name": "usrmgr3"
                }
            }
        )

        eq_(response.status_code, 400)
        eq_(response.json, {"msg": "no password provided"})

    def test_create_user__email_taken(self):
        EMAIL = "regularuser@regularuser.com"

        self._create_user(email=EMAIL)
        response = self.test_client.post(
            '/api/users',
            json={
                "user": {
                    "email": EMAIL,
                    "password": "123123",
                    "name": "usrmgr3"
                }
            }
        )

        eq_(response.status_code, 409)
        eq_(
            response.json,
            {'message': 'regularuser@regularuser.com exists already'}
        )

    def test_delete_user(self):
        self.user = self._create_user()
        self.user_token = self._create_token_for_user(self.user)

        assert self.user.deleted is False

        response = self.test_client.delete(
            '/api/users/{}'.format(self.user.id),
            headers={
                'Authorization': 'Bearer ' + self.user_token.jwt_token
            }
        )

        eq_(response.status_code, 200)
        ok_(self.user.deleted)
