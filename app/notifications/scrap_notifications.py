from enum import Enum


class ScrapNotificationsStatusEnum(Enum):
    PROCESSING = 'PROCESSING'
    PROCESSED = 'PROCESSED'
    FAILED = 'FAILED'


class ScrapNotifications():

    @staticmethod
    def __get_message(type: ScrapNotificationsStatusEnum) -> str:
        message = 'Hi there! '
        if type == ScrapNotificationsStatusEnum.PROCESSING:
            message += 'your scraped data is under process'
        if type == ScrapNotificationsStatusEnum.PROCESSED:
            message += 'your scraped data is ready'
        if type == ScrapNotificationsStatusEnum.FAILED:
            message += 'your scrap request failed due to some reason, please try again later'

        return message

    @staticmethod
    def send(type: ScrapNotificationsStatusEnum) -> None:
        message = ScrapNotifications.__get_message(type=type)
        # printing message for now, we can change this logic with any other notification system integration
        print(message)
