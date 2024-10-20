from enum import Enum


class ScrapNotificationsStatusEnum(Enum):
    PROCESSING = 'PROCESSING'
    PROCESSED = 'PROCESSED'
    FAILED = 'FAILED'


class ScrapNotifications():

    @staticmethod
    def __get_message(to: str, type: ScrapNotificationsStatusEnum, total_updated: int = None) -> str:
        message = f'🔔 Hi {to}! '
        if type == ScrapNotificationsStatusEnum.PROCESSING:
            message += 'your scraped data is under process'
        if type == ScrapNotificationsStatusEnum.PROCESSED:
            message += 'your scraped data is ready. ' + \
                str(total_updated) + ' records scrapped'
        if type == ScrapNotificationsStatusEnum.FAILED:
            message += 'your scrap request failed due to some reason, please try again later'

        return message

    @staticmethod
    def send(to: str, type: ScrapNotificationsStatusEnum, total_updated: int = None) -> None:
        message = ScrapNotifications.__get_message(
            to=to, type=type, total_updated=total_updated)
        # printing message for now, we can change this logic with any other notification system integration
        print(message)
