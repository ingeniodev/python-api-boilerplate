import os
import jwt
import hashlib
from datetime import datetime, timedelta
from flask import request
from functools import wraps

from src.model.model import Tokens
from src.util.dto import DTOError
from src.util.http_codes import Status


class AccessToken:

    def __init__(self):
        self.__secret_token = os.getenv('SECRET_TOKEN', 'shhhh!!')
        self.__exp_delta = os.getenv('TOKEN_EXP_DELTA', 60*60)
        self.__token_algorithm = os.getenv('TOKEN_ALGORITHM', 'HS256')

    def generate(self, payload):
        payload['exp'] = (
            datetime.utcnow() + timedelta(seconds=self.__exp_delta)
        )

        return jwt.encode(
            payload, self.__secret_token,
            self.__token_algorithm).decode('utf-8')

    def validate(self, token):
        if token:
            try:
                payload = jwt.decode(token, self.__secret_token,
                                     algorithms=[self.__token_algorithm])
                return True, payload
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                return False, None

        return False, None

    def update(self, token):
        result, payload = self.validate(token)

        if(not result):
            return False, None

        return True, self.generate(payload)


def requires_auth(f):
    @wraps(f)
    def wrap(self, *args, **kwargs):
        access_token = AccessToken()
        token = request.headers.get('Authorization', None)
        result, payload = access_token.validate(token)

        if result:
            try:
                user_id = payload.get('user_id')
                token = Tokens.get(
                    token=token,
                    id_user=user_id)
            except Tokens.DoesNotExist:
                result = False

        if not result:
            return DTOError(status_code=Status.HTTP_401_UNAUTHORIZED,
                            message="User not authenticated",
                            code="unhautorized").to_response()

        return f(self, *args, **kwargs)
    return wrap


def generate_salt():
    return hashlib.md5(os.urandom(29)).hexdigest()


def encode_password(password, salt):
    return hashlib.sha512((password + salt).encode()).hexdigest()


def check_passwords(password_db, password_user, salt):
    return password_db == encode_password(password_user, salt)
