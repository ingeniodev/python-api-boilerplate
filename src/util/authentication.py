import os
import jwt
from datetime import datetime, timedelta


class AccessToken:

    def __init__(self, user_id):
        self.__user_id = user_id
        self.__secret_token = os.getenv('SECRET_TOKEN', 'shhhh!!')
        self.__exp_delta = os.getenv('TOKEN_EXP_DELTA', 10*60*60)
        self.__token_algorithm = os.getenv('TOKEN_ALGORITHM', 'HS256')

    def generate(self):
        payload = {
            'user_id': self.__user_id,
            'exp': datetime.utcnow() + timedelta(seconds=self.__exp_delta)
        }

        return jwt.encode(
            payload, self.__secret_token, self.__token_algorithm).decode('utf-8')

    def validate(self, token):
        if token:
            try:
                payload = jwt.decode(token, self.__secret_token,
                                     algorithms=[self.__token_algorithm])
                return True, payload
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                return False, None

        return False, None

    def update(self):
        pass
