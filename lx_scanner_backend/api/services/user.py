import logging
import typing
from datetime import datetime, timedelta

import jwt

from lx_scanner_backend import exceptions
from lx_scanner_backend.db.query import Query
from lx_scanner_backend.models import User
from settings import JWT_SECRET


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
    def login_user(cls, username: str, password: str) -> typing.Tuple[str, datetime]:
        data = cls.query.get_user(username)

        if not data:
            raise exceptions.InvalidCredentials()

        data = data[0]

        user = User(**data)

        is_pw_matched = user.decrypt_password(password)

        if not is_pw_matched:
            raise exceptions.InvalidCredentials()

        if user.id is None:
            logging.error("User ID is missing check the data: %s", user.model_dump())
            raise exceptions.InvalidCredentials("User ID is missing")

        return cls.generate_jwt_token(user.id)

    @classmethod
    def generate_jwt_token(cls, user_id: int) -> typing.Tuple[str, datetime]:
        payload = {
            "user_id": user_id,
            "exp": datetime.now() + timedelta(days=1),
            "iat": datetime.now(),
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
        return token, payload["exp"]

    @classmethod
    def verify_jwt_token(cls, token: str) -> int:
        try:
            encoded_jwt = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            return encoded_jwt["user_id"]
        except jwt.ExpiredSignatureError as e:
            raise exceptions.TokenExpired() from e
        except jwt.InvalidTokenError as e:
            raise exceptions.InvalidToken() from e
        except Exception as e:
            logging.error("Error verifying JWT token: %s", e)
            raise exceptions.InvalidToken() from e
