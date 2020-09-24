import json

from src.util.dto import DTOBase
from marshmallow import Schema, fields, EXCLUDE, pre_load
from flask_restplus import fields as fields_rest


class UserSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    name = fields.String(
        data_key='name',
        error_messages={
            'invalid': 'Name must be a string!'
        })

    email = fields.Email(
        data_key='email',
        error_messages={
            'invalid': 'Email must follow a correct email format!'
        })

    password = fields.String(
        data_key='password',
        error_messages={
            'invalid': 'Password must be a string!'
        })

    PUT_FIELDS = [name.data_key, password.data_key]
    POST_FIELDS = [name.data_key, password.data_key]

    @pre_load
    def check_context(self, data, **kwargs):
        """ Checks context before deserializing the user data
        """
        # changing required to True if the load request is a POST request
        if 'post' in self.context:
            for field in self.POST_FIELDS:
                self.fields[field].required = True

        return data


class DTOUser(DTOBase):

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

        return user_json, self.status_code

    @staticmethod
    def doc(api):
        return api.model(DTOUser.__name__, {
            'id_user': fields_rest.Integer,
            'name': fields_rest.String,
        })
