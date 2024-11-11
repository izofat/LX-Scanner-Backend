import pydash
from flask import jsonify, make_response, request

from lx_scanner_backend import exceptions
from lx_scanner_backend.api.middleware.validation import auth_request
from lx_scanner_backend.api.services.user import UserService
from lx_scanner_backend.logger import Logger


class UserController:
    @staticmethod
    @auth_request
    def create_user():
        try:
            data = request.json
            username = pydash.get(data, "username")
            password = pydash.get(data, "password")

            UserService.create_user(username, password)

            return make_response(jsonify({"message": "User created"}), 200)

        except (
            exceptions.UserAlreadyExists,
            exceptions.UsernameTooLong,
            exceptions.UsernameTooShort,
            exceptions.PasswordTooLong,
            exceptions.PasswordTooShort,
        ) as e:
            return make_response(e.message, e.status_code)
        except Exception as e:
            Logger.error(e)
            return make_response(jsonify({"message": "Internal server error"}), 500)

    @staticmethod
    @auth_request
    def login_user():
        try:
            data = request.json
            username = pydash.get(data, "username")
            password = pydash.get(data, "password")

            token, exp = UserService.login_user(username, password)

            return make_response(
                jsonify(
                    {
                        "message": "Login successfully",
                        "token": token,
                        "exp": exp.isoformat(),
                    }
                ),
                200,
            )

        except exceptions.InvalidCredentials as e:
            return make_response(e.message, e.status_code)
        except Exception as e:
            Logger.error(e)
            return make_response(jsonify({"message": "Internal server error"}), 500)
