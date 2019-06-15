from tests import BaseDatabaseTestCase


class BaseResourceTest(BaseDatabaseTestCase):

    @classmethod
    def setup_class(cls):
        super(BaseResourceTest, cls).setup_class()
        cls.test_client = cls.app.test_client()

    def setup_method(self, method=None):
        super(BaseResourceTest, self).setup_method()
