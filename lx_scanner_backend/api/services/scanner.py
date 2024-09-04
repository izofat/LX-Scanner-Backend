import uuid

from lx_scanner_backend.api.services.user import UserService
from lx_scanner_backend.db.query import Query
from lx_scanner_backend.rabbbitmq.connection import RabbitMQConnection
from settings import input_file_path


class ScannerService:
    query = Query()
    rabbit_mq = RabbitMQConnection()
    user_service = UserService()

    @classmethod
    def scan(
        cls, username, password, image, language, expected_output
    ):  # pylint: disable=too-many-arguments
        user_id = cls.user_service.login_user(username, password)

        image_path = f"{input_file_path}/{uuid.uuid4()}.jpg"

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
