from marshmallow import Schema, fields


class LoginSchema(Schema):

    email = fields.Email(
        required=True,
        data_key='email',
        error_messages={
            'invalid': 'Email must follow a correct email format!'
        })

    password = fields.String(
        required=True,
        data_key='password',
        error_messages={
            'invalid': 'Password must be a string!'
        })
