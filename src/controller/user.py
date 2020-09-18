from flask_restplus import Namespace, Resource, fields
from flask import Response, request
from src.model.model import Users
from src.dto.user import UserDTO, UserSchema
from src.util.dto import DTOError, DTOBase
from src.util.http_codes import Status

api_user = Namespace('user', description='User Api')


@api_user.route('/<int:user_id>')
class User(Resource):
    def get(self, user_id):
        try:
            user = Users.get(Users.id_user == user_id)
        except Users.DoesNotExist:
            return DTOError(status_code=Status.HTTP_404_NOT_FOUND,
                            message="User not found!",
                            code="not_found").to_response()

        return UserDTO(Status.HTTP_200_OK, user).to_response()

    def delete(self, user_id):
        try:
            user = Users.get(Users.id_user == user_id)
            user.delete_instance()
        except Exception:
            pass

        return DTOBase(Status.HTTP_200_OK,
                       "User deleted!").to_response()

    def put(self, user_id):
        try:
            user = Users.get(Users.id_user == user_id)
        except Users.DoesNotExist:
            return DTOError(status_code=Status.HTTP_404_NOT_FOUND,
                            message="User not found!",
                            code="not_found").to_response()

        u = UserSchema(only=('name', )).load(request.json)
        print(u)
        return
        user.name = u['name'] if 'name' in u else user.name
        user.password = u['password'] if 'password' in u else user.password
        user.save()

        return UserDTO(Status.HTTP_200_OK, user).to_response()


@ api_user.route('/')
class NewUser(Resource):
    def post(self):
        u = UserSchema().load(request.json)
        user = Users(name=u['name'], email=u['email'], password=u['password'])
        # user.save()
        print(user)
        pass
