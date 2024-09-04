import base64

import pydash
from flask import request

from lx_scanner_backend.api.services.scanner import ScannerService


class ScannerController:  # pylint: disable=too-few-public-methods
    @staticmethod
    def recognize_image():
        try:
            data = request.json

            username = pydash.get(data, "username")
            password = pydash.get(data, "password")
            image = pydash.get(data, "image")
            language = pydash.get(data, "language")
            expected_output = pydash.get(data, "expected_output")

            image = base64.b64decode(image)

            ScannerService.scan(username, password, image, language, expected_output)

            return "Processing image", 200

        except Exception:
            return "Internal server error", 400
