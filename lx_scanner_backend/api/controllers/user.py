import pydash
from flask import request

from lx_scanner_backend import exceptions
from lx_scanner_backend.api.services.user import UserService


class UserController:
    @staticmethod
    def create_user():
        try:
            data = request.json
            username = pydash.get(data, "username")
            password = pydash.get(data, "password")

            UserService.create_user(username, password)

            return "User created", 200

        except (
            exceptions.UserAlreadyExists,
            exceptions.UsernameTooLong,
            exceptions.UsernameTooShort,
            exceptions.PasswordTooLong,
            exceptions.PasswordTooShort,
        ) as e:
            return e.message, e.status_code
        except Exception:
            return "Internal server error", 400

    @staticmethod
    def login_user():
        try:
            data = request.json
            username = pydash.get(data, "username")
            password = pydash.get(data, "password")

            UserService.login_user(username, password)

            return "Login successfully", 200

        except exceptions.InvalidCredentials as e:
            return e.message, e.status_code
        except Exception:
            return "Internal server error", 400
