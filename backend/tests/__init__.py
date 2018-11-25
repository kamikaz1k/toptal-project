from app import create_app, db

class BaseDatabaseTestCase(object):

    def __init__(self):
        super(BaseDatabaseTestCase, self).__init__()
        test_config = {
            'SQLALCHEMY_DATABASE_URI': "mysql+mysqldb://root@localhost/toptal_project_test?charset=utf8"
        }
        self.app = create_app(test_config)

        with self.app.app_context():
            # db.drop_all_tables()
            db.engine.execute('SET FOREIGN_KEY_CHECKS = 0;')
            for table in db.metadata.sorted_tables:
                db.engine.execute('DROP TABLE IF EXISTS {};'.format(table.name))
            db.engine.execute('SET FOREIGN_KEY_CHECKS = 1;')
            # ---------
            db.create_all()

    def setup(self):
        self._ctx = self.app.test_request_context()
        self._ctx.push()

    def teardown(self):
        self._ctx.pop()

