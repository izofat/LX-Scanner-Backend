import typing
from datetime import UTC, datetime, timedelta

import jwt

from lx_scanner_backend import exceptions
from lx_scanner_backend.db.query import Query
from lx_scanner_backend.logger import Logger
from lx_scanner_backend.models import JwtTokenDecoded, JwtTokenEncoded, User
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
            Logger.info("User ID is missing check the data: %s", user.model_dump())
            raise exceptions.InvalidCredentials("User ID is missing")

        return cls.generate_jwt_token(user.id)

    @classmethod
    def generate_jwt_token(cls, user_id: int) -> typing.Tuple[str, datetime]:
        token_record = cls.query.get_token(user_id)

        if (
            token_record
            and (token_record := token_record[0])
            and token_record["jwtExpireDate"].replace(tzinfo=UTC) - datetime.now(UTC)
            > timedelta(hours=1)
        ):
            return token_record["jwtToken"], token_record["jwtExpireDate"]

        now = datetime.now(UTC)
        exp = now + timedelta(days=1)

        payload = JwtTokenDecoded(userId=user_id, exp=exp, iat=now)

        token = jwt.encode(payload.model_dump(), JWT_SECRET, algorithm="HS256")

        cls.query.insert_token(user_id, token, exp)

        return token, exp

    @classmethod
    def verify_jwt_token(cls, token: str) -> int:
        try:
            decoded_jwt = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            decoded_jwt = JwtTokenDecoded(**decoded_jwt)

            token_data = cls.query.get_token(decoded_jwt.userId)
            if not token_data:
                raise exceptions.FirstLoginRequired()

            token_data = token_data[0]
            encoded_jwt = JwtTokenEncoded(**token_data)

            if token != encoded_jwt.jwtToken:
                raise exceptions.TokenNotMatch()

            return encoded_jwt.userId

        except jwt.ExpiredSignatureError as e:
            raise exceptions.TokenExpired() from e
        except jwt.InvalidTokenError as e:
            raise exceptions.InvalidToken() from e
        except Exception as e:
            Logger.error(e)
            raise exceptions.InvalidToken() from e
