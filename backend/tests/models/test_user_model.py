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
        eq_(users[0].email, user.email)
        eq_(users[0].password, user.password)

    def test_user_delete(self):

        user = self.create_user()
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

        user = self.create_user(deleted_at=datetime.now())
        user.save()

        users = User.query.all()
        assert users[0].deleted_at is not None

        user.reactivate()
        user.save()

        users = User.query.all()
        eq_(users[0].deleted_at, None)


    def test_user_is_user(self):
        user = self.create_user()

        eq_(user.is_user, True)

        user.roles.append(self.create_role(RoleNames.user))

        eq_(user.is_user, True)
        eq_(user.is_user_manager, False)
        eq_(user.is_admin, False)

    def test_user_is_user_manager(self):
        user_manager = self.create_user()
        user_manager.roles.append(self.create_role(RoleNames.user_manager))

        eq_(user_manager.is_user, False)
        eq_(user_manager.is_user_manager, True)
        eq_(user_manager.is_admin, False)

    def test_user_is_admin(self):
        admin = self.create_user()
        admin.roles.append(self.create_role(RoleNames.admin))

        eq_(admin.is_user, False)
        eq_(admin.is_user_manager, False)
        eq_(admin.is_admin, True)

