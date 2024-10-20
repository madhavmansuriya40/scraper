import pika


class RabbitMQConnection:
    def __init__(self) -> None:
        self.connection = None

    def connect(self) -> 'RabbitMQConnection':

        parameters = pika.ConnectionParameters(
            host='rabbitmq',  # Use the service name defined in docker-compose
            port=5672,
            credentials=pika.PlainCredentials('guest', 'guest')
        )

        self.connection = pika.BlockingConnection(parameters)
