import json
from schemas.schemas import ScrapeRequestSchema
from utils.queue import RabbitMQConnection


class QueueManager:

    def __init__(self) -> None:
        self.rabbitmq_connection = RabbitMQConnection()
        self.rabbitmq_connection.connect()

    def add_to_queue(self, scrap_req: ScrapeRequestSchema) -> None:

        if not self.rabbitmq_connection.connection or self.rabbitmq_connection.connection.is_closed:
            self.rabbitmq_connection.connect()

        channel = self.rabbitmq_connection.connection.channel()

        # Declare the queue
        channel.queue_declare(queue='scraping_queue')

        # Add the request to the queue
        message = json.dumps(scrap_req)
        channel.basic_publish(
            exchange='', routing_key='scraping_queue', body=message)

        # Do NOT close the connection here
