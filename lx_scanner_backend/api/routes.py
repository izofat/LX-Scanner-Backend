from flask import Blueprint

from .controllers.scanner import ScannerController
from .controllers.user import UserController

bp = Blueprint("api", __name__)

bp.route("/user/register", methods=["POST"])(UserController.create_user)
bp.route("/user/login", methods=["POST"])(UserController.login_user)

bp.route("/scanner/input", methods=["POST"])(ScannerController.scan)
