from nose.tools import eq_, ok_

from app.models.role import Role, RoleNames
from app.models.user import User
from tests import BaseDatabaseTestCase


class TestUserModel(BaseDatabaseTestCase):

    def _create_role(self, role_type=RoleNames.user):
        return Role(name=role_type)

    def test_user_save(self):

        assert User.query.all() == []

        user = self._create_user()
        user.save()

        users = User.query.all()
        eq_(users[0].email, user.email)
        eq_(users[0].password, user.password)

    def test_user_delete(self):

        user = self._create_user()
        user.save()

        assert User.query.count() == 1

        user.delete()
        user.save()

        users = User.query.all()

        eq_(users[0].email, user.email)
        eq_(users[0].password, user.password)
        eq_(users[0].deleted, True)
        assert users[0].deleted_at is not None

    def test_user_reactivate(self):

        user = self._create_user()
        user.delete()
        user.save()

        users = User.query.all()
        assert users[0].deleted_at is not None

        user.reactivate()
        user.save()

        users = User.query.all()
        eq_(users[0].deleted_at, None)

    def test_user_is_user(self):
        user = self._create_user()

        eq_(user.is_user, True)

        user.roles.append(self._create_role(RoleNames.user))

        eq_(user.is_user, True)
        eq_(user.is_user_manager, False)
        eq_(user.is_admin, False)

    def test_user_is_user_manager(self):
        user_manager = self._create_user()
        user_manager.roles.append(self._create_role(RoleNames.user_manager))

        eq_(user_manager.is_user, True)
        eq_(user_manager.is_user_manager, True)
        eq_(user_manager.is_admin, False)

    def test_user_is_admin(self):
        admin = self._create_user()
        admin.roles.append(self._create_role(RoleNames.admin))

        eq_(admin.is_user, True)
        eq_(admin.is_user_manager, False)
        eq_(admin.is_admin, True)

    def test_create_user(self):
        EMAIL = "someemail@ee.ca"
        NAME = "name name"
        PWD = "123123"
        CALORIES = 1000
        IS_ADMIN = True
        IS_USER_MANAGER = True

        User.create(
            email=EMAIL,
            name=NAME,
            password=PWD,
            calories_per_day=CALORIES,
            is_admin=IS_ADMIN,
            is_user_manager=IS_USER_MANAGER
        )

        user_record = User.query.filter(User.email == EMAIL).first()

        eq_(user_record.email, EMAIL)
        eq_(user_record.name, NAME)
        eq_(user_record.calories_per_day, CALORIES)
        eq_(user_record.is_admin, IS_ADMIN)
        eq_(user_record.is_user_manager, IS_USER_MANAGER)

    def test_create_user__hashes_password(self):
        PWD = "123123"
        user = User.create(
            email="someemail@ee.ca",
            name="name name",
            password=PWD,
            calories_per_day=1000,
            is_admin=True,
            is_user_manager=True
        )

        ok_(User.verify_password(password=PWD, hashed_password=user.password))
        ok_(user.password != PWD)

    def test_update_user__does_not_update_password(self):
        NEW_NAME = "new_name"
        user = self._create_user()
        old_password = user.password

        assert NEW_NAME != user.name

        user.update(password="somenewpassword", name=NEW_NAME)
        user.save()

        eq_(user.password, old_password)
        eq_(user.name, NEW_NAME)

    def test_find_by_credentials(self):
        EMAIL = "username@email.org"
        PASSWORD = "mysecurepass"

        self._create_user(email=EMAIL, password=PASSWORD)

        user = User.find_by_credentials(
            email=EMAIL,
            password=PASSWORD
        )

        ok_(user is not None)
        eq_(user.email, EMAIL)

    def test_find_by_credentials__nonexitent_account(self):
        EMAIL = "username@email.org"
        PASSWORD = "mysecurepass"

        user = User.find_by_credentials(
            email=EMAIL,
            password=PASSWORD
        )

        ok_(user is None)
