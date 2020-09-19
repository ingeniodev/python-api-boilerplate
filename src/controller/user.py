from flask_restplus import Namespace, Resource, fields
from flask import Response, request
from src.model.model import Users
from src.dto.user import UserDTO, UserSchema
from src.util.dto import DTOError, DTOBase
from src.util.http_codes import Status
from src.util.database import requires_user

api_user = Namespace('user', description='User Api')


@api_user.route('/<int:user_id>')
class User(Resource):
    @requires_user
    def get(self, user):
        return UserDTO(Status.HTTP_200_OK, user).to_response()

    def delete(self, user_id):
        try:
            user = Users.get(Users.id_user == user_id)
            user.delete_instance()
        except Exception:
            pass

        return DTOBase(Status.HTTP_200_OK,
                       "User deleted!").to_response()

    @requires_user
    def put(self, user):
        u = UserSchema(only=UserSchema.PUT_FIELDS).load(request.json)
        user.name = u['name'] if 'name' in u else user.name
        user.password = u['password'] if 'password' in u else user.password
        user.save()

        return UserDTO(Status.HTTP_200_OK, user).to_response()


@ api_user.route('')
class NewUser(Resource):
    def post(self):
        u = UserSchema(context={'post': True}).load(request.json)

        try:
            user = Users(name=u['name'], email=u['email'],
                         password=u['password'])
            user.save()
        except Exception:
            return DTOError(status_code=Status.HTTP_500_INTERNAL_SERVER_ERROR,
                            message="Error creating user",
                            code="database_error").to_response()

        return UserDTO(Status.HTTP_201_CREATED, user).to_response()
