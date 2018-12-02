from email.utils import format_datetime

from json_delta import udiff
from nose.tools import eq_

from app import create_app, db
from app.models.role import Role, RoleNames
from app.models.token import Token
from app.models.user import User


class BaseDatabaseTestCase(object):
    # Having a global app saves on test cleanup and instantiation
    # Also, since connection pools are bound to engines
    # this allows connections to be pooled correctly
    # instead of having idle connections

    # Ran 77 tests in 45.646s
    # vs 51.197s
    app = None

    def __init__(self):
        super(BaseDatabaseTestCase, self).__init__()
        test_config = {
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': "mysql+mysqldb://root@localhost/toptal_project_test?charset=utf8"
        }

        if BaseDatabaseTestCase.app is None:
            BaseDatabaseTestCase.app = create_app(test_config)

        self.app = BaseDatabaseTestCase.app

    def setup(self):

        with self.app.app_context():
            db.engine.execute('SET FOREIGN_KEY_CHECKS = 0;')
            for table in db.metadata.sorted_tables:
                # DROP Ran 77 tests in 65.791s
                # db.engine.execute('DROP TABLE IF EXISTS {};'.format(table.name))
                # TRUNCATE Ran 77 tests in 51.197s
                db.engine.execute('TRUNCATE TABLE {};'.format(table.name))
            db.engine.execute('SET FOREIGN_KEY_CHECKS = 1;')
            # ---------
            db.create_all()

            self._insert_user_role_data()

        self._ctx = self.app.test_request_context()
        self._ctx.push()

    def _insert_user_role_data(self):
        for role in RoleNames:
            db.session.add(Role(name=role))
            db.session.commit()

    def assert_json(self, expected, actual):
        diff = "\n".join(udiff(expected, actual))
        eq_(diff, ' {...}', diff)

    def assert_datetime(self, expected, actual):
        if not isinstance(expected, str):
            expected = format_datetime(expected)

        if not isinstance(actual, str):
            actual = format_datetime(actual)

        return eq_(actual, expected)

    def teardown(self):
        self._ctx.pop()

    def _create_user(self, **overrides):
        options = {
            'email': "regularuser@regularuser.com",
            'name': "regularuser",
            'password': "123123123"
        }
        options.update(overrides)
        return User.create(**options)

    def _create_admin_user(self, **overrides):
        options = {
            'email': "adminuser@adminuser.com",
            'name': "adminuser",
            'password': "123123123",
            'is_admin': True,
            'is_user_manager': False
        }
        options.update(overrides)
        return self._create_user(**options)

    def _create_user_manager_user(self, **overrides):
        options = {
            'email': "usermanager@usermanager.com",
            'name': "usermanager",
            'password': "123123123",
            'is_admin': False,
            'is_user_manager': True
        }
        options.update(overrides)
        return self._create_user(**options)

    def _create_token_for_user(self, user):
        return Token.create(user)
