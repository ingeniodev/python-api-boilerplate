
from flask import Response, request
from flask_restplus import Namespace, Resource
from src.util.http_codes import Status
from src.dto.login import LoginSchema
from src.model.model import Users
from src.util.dto import DTOError


api_auth = Namespace('auth', description='User Auth Api')


@api_auth.route('/login')
class Login(Resource):
    @api_auth.response(Status.HTTP_200_OK, 'Access token')
    @api_auth.response(Status.HTTP_401_UNAUTHORIZED, 'unauthorized')
    def post(self):
        credentials = LoginSchema().load(request.json)
        print(credentials)

        try:
            user = Users.get(
                Users.email == credentials['email'] and
                Users.password == credentials['password'])

        except Exception:
            return DTOError(status_code=Status.HTTP_401_UNAUTHORIZED,
                            message="Bad credentials",
                            code="unauthorized").to_response()


@api_auth.route('/logout')
class Logout(Resource):

    @api_auth.response(200, 'Logout')
    def get(self):
        pass
