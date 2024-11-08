from functools import wraps

from flask import jsonify, make_response, request

from lx_scanner_backend import exceptions
from lx_scanner_backend.api.services.user import UserService


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return make_response(
                jsonify({"message": "Unauthorized - No token provided"}), 401
            )

        token = auth_header.split(" ")[1]
        try:
            user_id = UserService.verify_jwt_token(token)

            request.user_id = user_id
            return f(*args, **kwargs)
        except (
            exceptions.TokenExpired,
            exceptions.InvalidToken,
        ) as e:
            return make_response(jsonify({"message": str(e)}), e.status_code)
        except Exception:
            return make_response(jsonify({"message": "Internal server error"}), 500)

    return decorated
