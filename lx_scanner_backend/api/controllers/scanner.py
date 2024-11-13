from typing import Optional

import pydash
from flask import jsonify, make_response, request
from werkzeug.datastructures import FileStorage

from lx_scanner_backend.api.middleware.auth import require_auth
from lx_scanner_backend.api.services.scanner import ScannerService
from lx_scanner_backend.logger import Logger


class ScannerController:  # pylint: disable=too-few-public-methods
    @staticmethod
    @require_auth
    def scan():
        try:
            data = request.form
            files = request.files

            image: FileStorage = pydash.get(files, "image")
            input_language: str = pydash.get(data, "input_language")
            expected_output: Optional[str] = pydash.get(data, "expected_output", None)

            if not image or not input_language:
                return make_response(
                    jsonify({"message": "Image and language are required"}), 400
                )

            user_id = request.user_id
            ScannerService.scan(user_id, image, input_language, expected_output)

            return make_response(jsonify({"message": "Processing image"}), 200)

        except Exception as e:
            Logger.error(e)
            return make_response(jsonify({"message": "Internal server error"}), 500)
