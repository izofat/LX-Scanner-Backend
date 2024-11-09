from functools import wraps

from flask import jsonify, make_response, request


def auth_request(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data = request.json
        if not data or not data.get("username") or not data.get("password"):
            return make_response(
                jsonify({"message": "Missing username or password"}), 400
            )
        return f(*args, **kwargs)

    return decorated
