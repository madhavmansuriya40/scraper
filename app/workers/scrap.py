import json
from scrapers.dental_stall_scraper import DentalStallScraper
from schemas.schemas import ScrapeRequestSchema
from database.json_database import JSONDatabase
from cache.mem_cache import MemcachedCache
from utils.queue import RabbitMQConnection
from notifications.scrap_notifications import ScrapNotifications, ScrapNotificationsStatusEnum


class ScrapingWorker:

    def __init__(self) -> None:
        self.db_manager = JSONDatabase()
        self.cache_manager = MemcachedCache()
        self.scraper = DentalStallScraper()
        self.rabbitmq_connection = RabbitMQConnection()
        self.connection = self.rabbitmq_connection.connect()

    def process_queue(self) -> None:
        channel = self.rabbitmq_connection.connection.channel()

        channel.queue_declare(queue='scraping_queue')

        def callback(ch, method, properties, body) -> None:
            # Simulate sending notification [logging messages]
            ScrapNotifications.send(
                type=ScrapNotificationsStatusEnum.PROCESSING)

            decoded_string = body.decode('utf-8')
            scrape_request_data = json.loads(decoded_string)

            # re-try mechanism, which will re-try failed items for 2 time
            while scrape_request_data['retry_count'] < 2:
                try:
                    scrape_request = ScrapeRequestSchema(
                        **scrape_request_data['request'])
                    data = self.scraper.scrape_catalogue(
                        scrap_req=scrape_request)

                    # Save to DB and cache
                    self.db_manager.save_data(data=data)

                    # updating cache with the latest cache
                    self.cache_manager.set(key=scrape_request.url, value=data)

                    # Simulate sending notification [logging messages]
                    ScrapNotifications.send(
                        type=ScrapNotificationsStatusEnum.PROCESSED)

                # TODO: @madhav to revisit and handle the exception properly
                except Exception as ex:
                    scrape_request_data['retry_count'] += 1
                    # Simulate sending notification [logging messages]
                    ScrapNotifications.send(
                        type=ScrapNotificationsStatusEnum.FAILED)
                    print(ex)

                break

        channel.basic_consume(
            queue='scraping_queue',
            on_message_callback=callback,
            auto_ack=True
        )
        print("Waiting for scraping tasks...")
        channel.start_consuming()


# To run the worker
if __name__ == "__main__":
    # I want to keep my working running, so running it explicitly
    worker = ScrapingWorker()
    worker.process_queue()
