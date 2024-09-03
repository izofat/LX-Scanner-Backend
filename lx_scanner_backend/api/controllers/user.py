import pydash
from flask import request

from lx_scanner_backend.api.services.user import UserService


class UserController:
    @staticmethod
    def create_user():
        data = request.json
        username = pydash.get(data, "username")
        password = pydash.get(data, "password")

        result = UserService.create_user(username, password)

        if result == 1:
            return "User created", 200

        return "User already exists", 400
