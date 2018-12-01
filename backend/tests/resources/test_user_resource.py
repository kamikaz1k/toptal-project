import copy

from nose.tools import eq_, ok_

from app.models.user import User
from tests.resources import BaseResourceTest


class TestUserResource(BaseResourceTest):

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

    def test_update_user(self):
        NEW_NAME = "NEW NAME FOR UPDATE"
        NEW_CALORIES = 9001

        self.user = self._create_user()
        self.user_token = self._create_token_for_user(self.user)

        payload = self.test_client.get(
            '/api/users/{}'.format(self.user.id),
            headers={
                'Authorization': 'Bearer ' + self.user_token.jwt_token
            }
        )

        payload.json['user']['name'] = NEW_NAME
        payload.json['user']['calories_per_day'] = NEW_CALORIES

        response = self.test_client.put(
            '/api/users/{}'.format(self.user.id),
            headers={
                'Authorization': 'Bearer ' + self.user_token.jwt_token
            },
            json=payload.json

        )

        self.assert_json(payload.json, response.json)

    def test_update_user__cannot_make_admin(self):
        self.user = self._create_user()
        self.user_token = self._create_token_for_user(self.user)

        get_response = self.test_client.get(
            '/api/users/{}'.format(self.user.id),
            headers={
                'Authorization': 'Bearer ' + self.user_token.jwt_token
            }
        )
        payload = copy.deepcopy(get_response.json)
        payload['user']['is_admin'] = True

        put_response = self.test_client.put(
            '/api/users/{}'.format(self.user.id),
            headers={
                'Authorization': 'Bearer ' + self.user_token.jwt_token
            },
            json=payload

        )

        self.assert_json(put_response.json, get_response.json)

    def test_update_user__cannot_make_user_manager(self):
        self.user = self._create_user()
        self.user_token = self._create_token_for_user(self.user)

        get_response = self.test_client.get(
            '/api/users/{}'.format(self.user.id),
            headers={
                'Authorization': 'Bearer ' + self.user_token.jwt_token
            }
        )
        payload = copy.deepcopy(get_response.json)
        payload['user']['is_user_manager'] = True

        put_response = self.test_client.put(
            '/api/users/{}'.format(self.user.id),
            headers={
                'Authorization': 'Bearer ' + self.user_token.jwt_token
            },
            json=payload

        )

        self.assert_json(put_response.json, get_response.json)

    def test_user_cannot_get_different_user(self):
        self.user = self._create_user()
        self.user_token = self._create_token_for_user(self.user)

        self.user_two = self._create_user(email="newemail@email.org")
        self.user_two_token = self._create_token_for_user(self.user_two)

        response = self.test_client.get(
            '/api/users/{}'.format(self.user.id),
            headers={
                'Authorization': 'Bearer ' + self.user_two_token.jwt_token
            }
        )

        eq_(response.status_code, 401)

    def test_user_cannot_update_different_user(self):
        NEW_NAME = "NEW NAME FOR UPDATE"
        NEW_CALORIES = 9001

        self.user = self._create_user()
        self.user_token = self._create_token_for_user(self.user)

        self.user_two = self._create_user(email="newemail@email.org")
        self.user_two_token = self._create_token_for_user(self.user_two)

        payload = self.test_client.get(
            '/api/users/{}'.format(self.user.id),
            headers={
                'Authorization': 'Bearer ' + self.user_token.jwt_token
            }
        )

        payload.json['user']['name'] = NEW_NAME
        payload.json['user']['calories_per_day'] = NEW_CALORIES

        response = self.test_client.put(
            '/api/users/{}'.format(self.user.id),
            headers={
                'Authorization': 'Bearer ' + self.user_two_token.jwt_token
            },
            json=payload.json

        )

        eq_(response.status_code, 401)

    def test_user_cannot_delete_different_user(self):
        self.user = self._create_user()
        self.user_token = self._create_token_for_user(self.user)

        self.user_two = self._create_user(email="newemail@email.org")
        self.user_two_token = self._create_token_for_user(self.user_two)

        assert self.user.deleted is False

        response = self.test_client.delete(
            '/api/users/{}'.format(self.user.id),
            headers={
                'Authorization': 'Bearer ' + self.user_two_token.jwt_token
            }
        )

        eq_(response.status_code, 401)
        eq_(self.user.deleted, False)

    def test_update_user__admin_can_make_user_manager(self):
        self.user = self._create_user()
        self.user_token = self._create_token_for_user(self.user)

        self.admin = self._create_admin_user()
        self.admin_token = self._create_token_for_user(self.admin)

        get_response = self.test_client.get(
            '/api/users/{}'.format(self.user.id),
            headers={
                'Authorization': 'Bearer ' + self.admin_token.jwt_token
            }
        )
        payload = get_response.json
        payload['user']['is_user_manager'] = True

        put_response = self.test_client.put(
            '/api/users/{}'.format(self.user.id),
            headers={
                'Authorization': 'Bearer ' + self.admin_token.jwt_token
            },
            json=payload

        )

        self.assert_json(put_response.json, payload)

    def test_update_user__admin_can_make_admin(self):
        self.user = self._create_user()
        self.user_token = self._create_token_for_user(self.user)

        self.admin = self._create_admin_user()
        self.admin_token = self._create_token_for_user(self.admin)

        get_response = self.test_client.get(
            '/api/users/{}'.format(self.user.id),
            headers={
                'Authorization': 'Bearer ' + self.admin_token.jwt_token
            }
        )
        payload = get_response.json
        payload['user']['is_admin'] = True

        put_response = self.test_client.put(
            '/api/users/{}'.format(self.user.id),
            headers={
                'Authorization': 'Bearer ' + self.admin_token.jwt_token
            },
            json=payload

        )

        self.assert_json(put_response.json, payload)

    def test_update_user__user_manager_can_make_user_manager(self):
        self.user = self._create_user()
        self.user_token = self._create_token_for_user(self.user)

        self.user_manager = self._create_user_manager_user()
        self.user_manager_token = self._create_token_for_user(
            self.user_manager
        )

        get_response = self.test_client.get(
            '/api/users/{}'.format(self.user.id),
            headers={
                'Authorization': 'Bearer ' + self.user_manager_token.jwt_token
            }
        )
        payload = get_response.json
        payload['user']['is_user_manager'] = True

        put_response = self.test_client.put(
            '/api/users/{}'.format(self.user.id),
            headers={
                'Authorization': 'Bearer ' + self.user_manager_token.jwt_token
            },
            json=payload

        )

        self.assert_json(put_response.json, payload)

    def test_update_user__user_manager_can_make_admin(self):
        self.user = self._create_user()
        self.user_token = self._create_token_for_user(self.user)

        self.user_manager = self._create_user_manager_user()
        self.user_manager_token = self._create_token_for_user(
            self.user_manager
        )

        get_response = self.test_client.get(
            '/api/users/{}'.format(self.user.id),
            headers={
                'Authorization': 'Bearer ' + self.user_manager_token.jwt_token
            }
        )
        payload = get_response.json
        payload['user']['is_admin'] = True

        put_response = self.test_client.put(
            '/api/users/{}'.format(self.user.id),
            headers={
                'Authorization': 'Bearer ' + self.user_manager_token.jwt_token
            },
            json=payload

        )

        self.assert_json(put_response.json, payload)

    def test_create_user__unauthd_cannot_make_admin(self):
        EMAIL = "unauthd@unauthd.com"
        payload = {
            'user': {
                'email': EMAIL,
                'name': "unauthd",
                'password': "123123123",
                'calories_per_day': 0,
                'active': True,
                'is_admin': True,
                'is_user_manager': False
            }
        }

        response = self.test_client.post(
            '/api/users',
            json=payload
        )

        eq_(response.json['user']['is_admin'], False)

        query = User.query.filter(User.email == EMAIL)
        user = query.first()

        eq_(user.is_admin, False)

    def test_create_user__user_cannot_make_admin(self):
        self.user = self._create_user()
        self.user_jwt_token = self._create_token_for_user(
            self.user
        ).jwt_token
        EMAIL = "unauthd@unauthd.com"

        payload = {
            'user': {
                'email': EMAIL,
                'name': "unauthd",
                'password': "123123123",
                'calories_per_day': 0,
                'active': True,
                'is_admin': True,
                'is_user_manager': False
            }
        }

        response = self.test_client.post(
            '/api/users',
            json=payload,
            headers={
                'Authorization': 'Bearer ' + self.user_jwt_token
            }
        )

        eq_(response.json['user']['is_admin'], False)

        query = User.query.filter(User.email == EMAIL)
        user = query.first()

        eq_(user.is_admin, False)

    def test_create_user__admin_can_make_admin(self):
        self.admin = self._create_admin_user()
        self.admin_jwt_token = self._create_token_for_user(
            self.admin
        ).jwt_token
        EMAIL = "regularuser@regularuser.com"

        payload = {
            'user': {
                'email': EMAIL,
                'name': "regularuser",
                'password': "123123123",
                'calories_per_day': 0,
                'active': True,
                'is_admin': True,
                'is_user_manager': False
            }
        }

        response = self.test_client.post(
            '/api/users',
            json=payload,
            headers={
                'Authorization': 'Bearer ' + self.admin_jwt_token
            }
        )

        eq_(response.json['user']['is_admin'], True)

        query = User.query.filter(User.email == EMAIL)
        user = query.first()

        eq_(user.is_admin, True)

    def test_create_user__user_manager_make_admin(self):
        self.user_manager = self._create_user_manager_user()
        self.user_manager_jwt_token = self._create_token_for_user(
            self.user_manager
        ).jwt_token
        EMAIL = "regularuser@regularuser.com"

        payload = {
            'user': {
                'email': EMAIL,
                'name': "regularuser",
                'password': "123123123",
                'calories_per_day': 0,
                'active': True,
                'is_admin': True,
                'is_user_manager': False
            }
        }

        response = self.test_client.post(
            '/api/users',
            json=payload,
            headers={
                'Authorization': 'Bearer ' + self.user_manager_jwt_token
            }
        )

        eq_(response.json['user']['is_admin'], True)

        query = User.query.filter(User.email == EMAIL)
        user = query.first()

        eq_(user.is_admin, True)
# USER MAANGER

    def test_create_user__unauthd_cannot_make_user_manager(self):
        EMAIL = "unauthd@unauthd.com"
        payload = {
            'user': {
                'email': EMAIL,
                'name': "unauthd",
                'password': "123123123",
                'calories_per_day': 0,
                'active': True,
                'is_admin': False,
                'is_user_manager': True
            }
        }

        response = self.test_client.post(
            '/api/users',
            json=payload
        )

        eq_(response.json['user']['is_user_manager'], False)

        query = User.query.filter(User.email == EMAIL)
        user = query.first()

        eq_(user.is_user_manager, False)

    def test_create_user__user_cannot_make_user_manager(self):
        self.user = self._create_user()
        self.user_jwt_token = self._create_token_for_user(
            self.user
        ).jwt_token
        EMAIL = "unauthd@unauthd.com"

        payload = {
            'user': {
                'email': EMAIL,
                'name': "unauthd",
                'password': "123123123",
                'calories_per_day': 0,
                'active': True,
                'is_admin': False,
                'is_user_manager': True
            }
        }

        response = self.test_client.post(
            '/api/users',
            json=payload,
            headers={
                'Authorization': 'Bearer ' + self.user_jwt_token
            }
        )

        eq_(response.json['user']['is_user_manager'], False)

        query = User.query.filter(User.email == EMAIL)
        user = query.first()

        eq_(user.is_user_manager, False)

    def test_create_user__admin_can_make_user_manager(self):
        self.admin = self._create_admin_user()
        self.admin_jwt_token = self._create_token_for_user(
            self.admin
        ).jwt_token
        EMAIL = "regularuser@regularuser.com"

        payload = {
            'user': {
                'email': EMAIL,
                'name': "regularuser",
                'password': "123123123",
                'calories_per_day': 0,
                'active': True,
                'is_admin': False,
                'is_user_manager': True
            }
        }

        response = self.test_client.post(
            '/api/users',
            json=payload,
            headers={
                'Authorization': 'Bearer ' + self.admin_jwt_token
            }
        )

        eq_(response.json['user']['is_user_manager'], True)

        query = User.query.filter(User.email == EMAIL)
        user = query.first()

        eq_(user.is_user_manager, True)

    def test_create_user__user_manager_make_user_manager(self):
        self.user_manager = self._create_user_manager_user()
        self.user_manager_jwt_token = self._create_token_for_user(
            self.user_manager
        ).jwt_token
        EMAIL = "regularuser@regularuser.com"

        payload = {
            'user': {
                'email': EMAIL,
                'name': "regularuser",
                'password': "123123123",
                'calories_per_day': 0,
                'active': True,
                'is_admin': False,
                'is_user_manager': True
            }
        }

        response = self.test_client.post(
            '/api/users',
            json=payload,
            headers={
                'Authorization': 'Bearer ' + self.user_manager_jwt_token
            }
        )

        eq_(response.json['user']['is_user_manager'], True)

        query = User.query.filter(User.email == EMAIL)
        user = query.first()

        eq_(user.is_user_manager, True)

    def test_query_users(self):
        self.user_manager = self._create_user_manager_user()
        self.user_manager_jwt_token = self._create_token_for_user(
            self.user_manager
        ).jwt_token

        for i in range(15):
            self._create_user(email="regularuser.{}@email.com".format(i + 1))

        assert User.query.count() == 16

        response = self.test_client.get(
            '/api/users',
            headers={
                'Authorization': 'Bearer ' + self.user_manager_jwt_token
            }
        )

        eq_(len(response.json['users']), 10, "does not default to page 1")

        response = self.test_client.get(
            '/api/users',
            headers={
                'Authorization': 'Bearer ' + self.user_manager_jwt_token
            },
            query_string="p=1"
        )
        eq_(len(response.json['users']), 10)

        response = self.test_client.get(
            '/api/users',
            headers={
                'Authorization': 'Bearer ' + self.user_manager_jwt_token
            },
            query_string="p=2"
        )
        eq_(len(response.json['users']), 6)

        response = self.test_client.get(
            '/api/users',
            headers={
                'Authorization': 'Bearer ' + self.user_manager_jwt_token
            },
            query_string="p=3"
        )
        eq_(len(response.json['users']), 0)

    def test_query_users__limited_by_role(self):
        self.user = self._create_user()
        self.user_jwt_token = self._create_token_for_user(
            self.user
        ).jwt_token
        self.user_manager = self._create_user_manager_user()
        self.user_manager_jwt_token = self._create_token_for_user(
            self.user_manager
        ).jwt_token
        self.admin = self._create_admin_user()
        self.admin_jwt_token = self._create_token_for_user(
            self.admin
        ).jwt_token

        assert User.query.count() == 3

        response = self.test_client.get(
            '/api/users',
            headers={
                'Authorization': 'Bearer ' + self.admin_jwt_token
            }
        )
        eq_(response.status_code, 200)

        response = self.test_client.get(
            '/api/users',
            headers={
                'Authorization': 'Bearer ' + self.user_manager_jwt_token
            }
        )
        eq_(response.status_code, 200)

        response = self.test_client.get(
            '/api/users',
            headers={
                'Authorization': 'Bearer ' + self.user_jwt_token
            }
        )
        eq_(response.status_code, 401)
