from flask_restplus import Namespace, Resource, fields
from src.model.model import Users

api_user = Namespace('user', description='User Api')


@api_user.route('/<user_id>')
@api_user.response(404, 'User not found')
class User(Resource):
    def get(self, user_id):
        user = Users.get(Users.id_user == user_id)
        print(user.__dict__)
        print(user_id)
        print(Users)
        pass

    def delete(self, user_id):
        pass

    def put(self, user_id):
        pass


@api_user.route('/')
class NewUser(Resource):
    def post(self):
        pass
