from flask import Blueprint

from .controllers.user import UserController

bp = Blueprint("api", __name__)

bp.route("/users", methods=["POST"])(UserController.create_user)
