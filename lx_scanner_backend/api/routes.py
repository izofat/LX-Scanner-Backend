from flask import Blueprint

from lx_scanner_backend.api.controllers.scanner import ScannerController
from lx_scanner_backend.api.controllers.user import UserController

bp = Blueprint("api", __name__)

bp.route("/user/register", methods=["POST"])(UserController.create_user)
bp.route("/user/login", methods=["POST"])(UserController.login_user)

bp.route("/scanner/input", methods=["POST"])(ScannerController.scan)
bp.route("/scanner/input", methods=["GET"])(ScannerController.get_all_images)
bp.route("/scanner/input/id/<image_id>", methods=["GET"])(
    ScannerController.get_image_by_id
)
bp.route("/scanner/input/name/<image_name>", methods=["GET"])(
    ScannerController.get_image_by_name
)
