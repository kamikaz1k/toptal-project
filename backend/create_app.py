from flask import Flask
from flask_restful import Resource, Api

from app.database import db
from app.resources.meal import MealResource
from app.resources.meals import MealsResource
from app.resources.login import LoginResource
from app.resources.logout import LogoutResource
from app.resources.users import UsersResource


class PingResource(Resource):
    def get(self):
        return {'version': '1'}


def create_api():
    api = Api()
    api.add_resource(
        PingResource,
        '/ping'
    )
    api.add_resource(
        UsersResource,
        '/api/users'
    )
    api.add_resource(
        LoginResource,
        '/auth/login'
    )
    api.add_resource(
        LogoutResource,
        '/auth/logout'
    )
    api.add_resource(
        MealsResource,
        '/api/meals'
    )
    api.add_resource(
        MealResource,
        '/api/meal/<int:meal_id>'
    )

    return api


def get_db_url():
    LOCAL_DEV_URI = "mysql+mysqldb://root@localhost/toptal_project?charset=utf8"
    return LOCAL_DEV_URI


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = get_db_url()
    app.config['JWT_SECRET'] = "JWT_SECRET_KEY"

    api = create_api()

    db.init_app(app)
    api.init_app(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)