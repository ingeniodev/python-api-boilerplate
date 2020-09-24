
from functools import wraps

from src.util.dto import DTOError
from src.model.model import Users
from src.util.http_codes import Status


def requires_user(f):
    @wraps(f)
    def wrap(self, user_id, *args, **kwargs):
        try:
            user = Users.get(Users.id_user == user_id)
        except Users.DoesNotExist:
            return DTOError(status_code=Status.HTTP_404_NOT_FOUND,
                            message="User not found!",
                            code="not_found").to_response()
        return f(self, user, *args, **kwargs)
    return wrap
