from lx_scanner_backend.api import exceptions
from lx_scanner_backend.db.models import User
from lx_scanner_backend.db.query import Query


class UserService:
    query = Query()

    @classmethod
    def create_user(cls, username: str, password: str):
        user = User(username=username, password=password)
        user.hash_password()

        result = cls.query.register_account(user.username, user.password)

        if not result:
            raise exceptions.UserAlreadyExists()

    @classmethod
    def login_user(cls, username: str, password: str):
        data = cls.query.get_user(username)

        if not data:
            raise exceptions.InvalidCredentials()

        data = data[0]

        user = User(**data)

        is_pw_matched = user.decrypt_password(password)

        if not is_pw_matched:
            raise exceptions.InvalidCredentials()
