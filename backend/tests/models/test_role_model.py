from nose.tools import eq_

from app.models.role import Role, RoleNames
from tests import BaseDatabaseTestCase


class TestRole(BaseDatabaseTestCase):

    def setup(self):
        super(TestRole, self).setup()
        Role.create_user_roles()

    def test_get_user_role(self):
        role = Role.get_user_role()
        eq_(role.name, RoleNames.user)

    def test_get_user_manager_role(self):
        role = Role.get_user_manager_role()
        eq_(role.name, RoleNames.user_manager)

    def test_get_admin_role(self):
        role = Role.get_admin_role()
        eq_(role.name, RoleNames.admin)
