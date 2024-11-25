import uuid
from typing import Optional

from flask import json
from werkzeug.datastructures import FileStorage

from lx_scanner_backend.db.query import Query
from lx_scanner_backend.rabbbitmq.connection import RabbitMQConnection
from settings import INPUT_FILE_PATH


class ScannerService:
    query = Query()
    rabbit_mq = RabbitMQConnection()

    @classmethod
    def scan(
        cls,
        user_id,
        name: Optional[str],
        image: FileStorage,
        input_language: str,
        expected_output: Optional[str],
    ):  # pylint: disable=too-many-arguments,too-many-positional-arguments
        image_path = f"{INPUT_FILE_PATH}/{uuid.uuid4()}.jpg"

        image.save(image_path)

        cls.query.insert_scanner_input(
            user_id, name, expected_output, image_path, input_language
        )

        cls.rabbit_mq.publish(
            json.dumps(
                {
                    "user_id": user_id,
                    "image_path": image_path,
                    "language": input_language,
                }
            )
        )

    @classmethod
    def get_all_images(cls, user_id: int):
        return cls.query.get_all_images(user_id)

    @classmethod
    def get_image_by_id(cls, image_id: int):
        return cls.query.get_image_by_id(image_id)

    @classmethod
    def get_image_by_name(cls, image_name: str):
        return cls.query.get_image_by_name(image_name)
