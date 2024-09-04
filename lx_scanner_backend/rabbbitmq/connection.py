import pika

from settings import RabbitMQConfig


class RabbitMQConnection:
    def __init__(self):
        self._connection = None
        self._channel = None
        self.connect()

    def connect(self):
        credentials = pika.PlainCredentials(
            RabbitMQConfig.USER, RabbitMQConfig.PASSWORD
        )
        parameters = pika.ConnectionParameters(
            RabbitMQConfig.HOST, RabbitMQConfig.PORT, "/", credentials
        )
        self._connection = pika.BlockingConnection(parameters)
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=RabbitMQConfig.QUEUE_NAME, durable=True)

    def close(self):
        self._connection.close()

    def publish(self, message):
        self._channel.basic_publish(
            exchange="",
            routing_key=RabbitMQConfig.QUEUE_NAME,
            body=message,
            properties=pika.BasicProperties(delivery_mode=2),
        )
