import json

from src.util.dto import DTOBase
from marshmallow import Schema, fields, EXCLUDE


class UserSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    name = fields.String(
        required=True,
        data_key='name',
        error_messages={
            'invalid': 'Name must be a string!'
        })

    email = fields.Email(
        required=True,
        data_key='email',
        error_messages={
            'invalid': 'Email must be a string!'
        })

    password = fields.String(
        required=True,
        data_key='password',
        error_messages={
            'invalid': 'Password must be a string!'
        })

    PUT_FIELDS = [name.data_key, password.data_key]


class UserDTO(DTOBase):

    def __init__(self, status_code, user, is_public=True):
        self.user = user
        self.is_public = is_public

        super().__init__(status_code=status_code, message=None)

    def to_response(self):
        user_json = {
            'id_user': self.user.id_user,
            'name': self.user.name,
        }

        if not self.is_public:
            user_json['email'] = self.user.email

        return user_json,  self.status_code
