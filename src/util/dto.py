

class DTOBase:

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


class DTOError(DTOBase):

    def __init__(self, status_code, message, code):
        super().__init__(status_code, message)
        self.code = code
