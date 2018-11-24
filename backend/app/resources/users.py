from flask_restful import Resource


class UsersResource(Resource):
    def post(self):
        # get request parameters

        # get users by email

        # if user exists, throw

        # else create
        return {
            'user': {
                'id': 9090,
                'email': 'no@email.ca',
                'name': "",
                'password': "12bws09s0dnj11899xcsdsa12"
            }
        }