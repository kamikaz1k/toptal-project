from flask import Flask
from flask_restful import Resource, Api

from app.database import db
from app.resources.users import UsersResource


class PingResource(Resource):
    def get(self):
        return {'version': '1'}


api = Api()


api.add_resource(
    PingResource,
    '/ping'
)


api.add_resource(
    UsersResource,
    '/api/users'
)


def get_db_url():
    LOCAL_DEV_URI = "mysql+mysqldb://root@localhost/toptal_project?charset=utf8"
    return LOCAL_DEV_URI


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = get_db_url()

    db.init_app(app)
    api.init_app(app)

    return app


if __name__ == '__main__':
    app = create_app()
    # import pdb; pdb.set_trace()
    # with app.app_context():
    #     # import models...
    #     db.create_all()
    app.run(debug=True)