
from flask import Response, request
from flask_restplus import Namespace, Resource
from src.util.http_codes import Status
from src.dto.login import LoginSchema
from src.model.model import Users, Tokens
from src.util.dto import DTOError
from src.util.authentication import AccessToken
from datetime import datetime

api_auth = Namespace('auth', description='User Auth Api')


@api_auth.route('/login')
class Login(Resource):
    @api_auth.response(Status.HTTP_200_OK, 'access_token')
    @api_auth.response(Status.HTTP_401_UNAUTHORIZED, 'not_authorized',
                       DTOError.doc(api_auth))
    def post(self):
        credentials = LoginSchema().load(request.json)
        try:
            user = Users.get(
                Users.email == credentials['email'],
                Users.password == credentials['password'])

            access_token = AccessToken()
            token = Tokens(token=access_token.generate(user.id_user),
                           id_user=user.id_user)
            token.save()

            return token.token, Status.HTTP_200_OK
        except Users.DoesNotExist:
            pass

        return DTOError(status_code=Status.HTTP_401_UNAUTHORIZED,
                            message="Bad credentials",
                            code="unauthorized").to_response()


@api_auth.route('/refresh')
class Refresh(Resource):
    @api_auth.response(Status.HTTP_200_OK, 'new_access_token')
    @api_auth.response(Status.HTTP_401_UNAUTHORIZED, 'not_valid_token',
                       DTOError.doc(api_auth))
    def get(self):
        token = request.headers.get('Authorization', None)
        access_token = AccessToken()
        result, payload = access_token.validate(token)
        result, new_token = access_token.update(token)

        if result:
            try:
                user_id = payload.get('user_id')

                token = Tokens.get(token=token, id_user=user_id)
                token.delete_instance()

                token = Tokens(token=new_token, id_user=user_id)
                token.save()

                return token.token, Status.HTTP_200_OK
            except Tokens.DoesNotExist:
                pass

        return (DTOError(status_code=Status.HTTP_401_UNAUTHORIZED,
                        message="Bad token",
                        code="unauthorized").to_response(),
                Status.HTTP_401_UNAUTHORIZED)


@api_auth.route('/logout')
class Logout(Resource):
    @api_auth.response(Status.HTTP_200_OK, 'logout')
    def get(self):
        token = request.headers.get('Authorization', None)
        access_token = AccessToken()
        result, payload = access_token.validate(token)

        if result:
            try:
                token = Tokens.get(
                            token=token,
                            id_user=payload.get('user_id'))
                token.delete_instance()
            except Exception:
                pass

        return "", Status.HTTP_200_OK
