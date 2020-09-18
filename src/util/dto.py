import json
from flask import Response


class DTOBase():

    def __init__(self, status_code, message, type='application/json'):
        self.status_code = status_code
        self.message = message
        self.type = type

    def to_response(self):
        return self.message, self.status_code


class DTOError(DTOBase):

    def __init__(self, status_code, message, code):
        super().__init__(status_code, message)
        self.code = code

    def to_response(self):
        error = {
            'message': self.message,
            'code': self.message,
        }

        return error, self.status_code
