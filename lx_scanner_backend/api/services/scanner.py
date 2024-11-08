import uuid

from lx_scanner_backend.db.query import Query
from lx_scanner_backend.rabbbitmq.connection import RabbitMQConnection
from settings import INPUT_FILE_PATH


class ScannerService:
    query = Query()
    rabbit_mq = RabbitMQConnection()

    @classmethod
    def scan(
        cls, user_id, image, language, expected_output
    ):  # pylint: disable=too-many-arguments
        image_path = f"{INPUT_FILE_PATH}/{uuid.uuid4()}.jpg"

        with open(image_path, "wb") as f:
            f.write(image)

        cls.query.insert_scanner_input(user_id, image_path, language, expected_output)

        # TODO send image to rabbitmq

    def send_image_to_rabbitmq(
        self,
        user_id,
        image_path,
        language,
    ):
        pass
