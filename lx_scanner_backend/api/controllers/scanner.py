import base64
import logging

import pydash
from flask import jsonify, make_response, request

from lx_scanner_backend.api.middleware.auth import require_auth
from lx_scanner_backend.api.services.scanner import ScannerService


class ScannerController:  # pylint: disable=too-few-public-methods
    @staticmethod
    @require_auth
    def scan():
        try:
            data = request.json

            image = pydash.get(data, "image")
            language = pydash.get(data, "language")
            expected_output = pydash.get(data, "expected_output")

            image = base64.b64decode(image)

            user_id = request.user_id
            ScannerService.scan(user_id, image, language, expected_output)

            return make_response(jsonify({"message": "Processing image"}), 200)

        except Exception as e:
            logging.error(e)
            return make_response(jsonify({"message": "Internal server error"}), 500)
