import uuid
from typing import Optional

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
    ):  # pylint: disable=too-many-arguments
        image_path = f"{INPUT_FILE_PATH}/{uuid.uuid4()}.jpg"

        image.save(image_path)

        cls.query.insert_scanner_input(
            user_id, name, expected_output, image_path, input_language
        )

        # TODO send image to rabbitmq

    def send_image_to_rabbitmq(
        self,
        user_id,
        image_path,
        language,
    ):
        pass
