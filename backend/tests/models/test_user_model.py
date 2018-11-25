from datetime import datetime

from nose.tools import eq_

from app.models.role import Role, RoleNames
from app.models.user import User
from tests import BaseDatabaseTestCase


class TestUser(BaseDatabaseTestCase):

    def create_user(self, **options):
        props = dict(
            email="test@email.org",
            password="23k12n312n31nl13bj5",
            name="Slim Jim"
        )
        props.update(options)
        return User(**props)

    def create_role(self, role_type=RoleNames.user):
        return Role(name=role_type)

    def test_user_save(self):

        assert User.query.all() == []

        user = self.create_user()
        user.save()

        users = User.query.all()
        assert users[0].email == user.email
        assert users[0].password == user.password

    def test_user_delete(self):

        user = self.create_user()
        user.save()

        assert User.query.count() == 1

        user.delete()
        user.save()

        users = User.query.all()

        assert users[0].email == user.email
        assert users[0].password == user.password
        assert users[0].deleted_at is not None
        assert users[0].deleted

    def test_user_reactivate(self):

        user = self.create_user(deleted_at=datetime.now())
        user.save()

        users = User.query.all()
        assert users[0].deleted_at is not None

        user.reactivate()
        user.save()

        users = User.query.all()
        assert users[0].deleted_at is None


    def test_user_is_user(self):
        user = self.create_user()

        assert user.is_user()

        user.roles.append(self.create_role(RoleNames.user))

        assert user.is_user()
        assert not user.is_user_manager()
        assert not user.is_admin()

    def test_user_is_user_manager(self):
        user_manager = self.create_user()
        user_manager.roles.append(self.create_role(RoleNames.user_manager))

        assert not user_manager.is_user()
        assert user_manager.is_user_manager()
        assert not user_manager.is_admin()

    def test_user_is_admin(self):
        admin = self.create_user()
        admin.roles.append(self.create_role(RoleNames.admin))

        assert not admin.is_user()
        assert not admin.is_user_manager()
        assert admin.is_admin()

