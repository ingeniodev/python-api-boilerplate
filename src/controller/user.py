import marshmallow
from flask_restplus import Namespace, Resource, fields, Model
from flask import Response, request
from src.model.model import Users
from src.dto.user import DTOUser, UserSchema
from src.util.dto import DTOError, DTOBase
from src.util.http_codes import Status
from src.util.database import requires_user
from src.util.authentication import requires_auth, \
    encode_password, generate_salt

api_user = Namespace('user', description='User Api')


@api_user.route('/<int:user_id>')
@api_user.doc(params={'user_id': {'description': 'An user ID', 'type': 'int'}})
class User(Resource):

    @requires_auth
    @requires_user
    @api_user.response(Status.HTTP_200_OK, 'User information',
                       DTOUser.doc(api_user))
    @api_user.response(Status.HTTP_404_NOT_FOUND, 'not_found',
                       DTOError.doc(api_user))
    def get(self, user):
        return DTOUser(Status.HTTP_200_OK, user).to_response()

    @requires_auth
    @api_user.response(200, 'User deleted')
    def delete(self, user_id):
        try:
            user = Users.get(Users.id_user == user_id)
            user.delete_instance()
        except Exception:
            pass

        return DTOBase(Status.HTTP_200_OK,
                       "User deleted!").to_response()

    @requires_auth
    @requires_user
    @api_user.response(Status.HTTP_200_OK, 'User information updated',
                       DTOUser.doc(api_user))
    @api_user.response(Status.HTTP_404_NOT_FOUND, 'not_found',
                       DTOError.doc(api_user))
    def put(self, user):
        u = UserSchema(only=UserSchema.PUT_FIELDS).load(request.json)
        user.name = u['name'] if 'name' in u else user.name
        user.password = encode_password(
            u['password'], user.salt)if 'password' in u else user.password
        user.save()

        return DTOUser(Status.HTTP_200_OK, user).to_response()


@api_user.route('')
class NewUser(Resource):
    # @requires_auth
    @api_user.response(Status.HTTP_201_CREATED, 'New user information',
                       DTOUser.doc(api_user))
    @api_user.response(Status.HTTP_400_BAD_REQUEST, 'database_error',
                       DTOError.doc(api_user))
    def post(self):
        try:
            u = UserSchema(context={'post': True}).load(request.json)
        except marshmallow.ValidationError:
            return DTOError(status_code=Status.HTTP_400_BAD_REQUEST,
                            message='Required fields are not satisfied',
                            code="bad_request").to_response()

        try:
            salt = generate_salt()
            user = Users(
                name=u['name'], email=u['email'],
                password=encode_password(u['password'], salt),
                salt=salt
            )
            user.save()
        except Exception:
            return DTOError(status_code=Status.HTTP_500_INTERNAL_SERVER_ERROR,
                            message="Error creating user",
                            code="database_error").to_response()

        return DTOUser(Status.HTTP_201_CREATED, user).to_response()
