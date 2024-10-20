from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPAuthorizationCredentials
from schemas.schemas import ScrapeRequestSchema, ScrapeResponseSchema
from utils.auth import authenticate_request
from utils.user import User
from queue_manager import QueueManager


router = APIRouter(
    tags=['scrapers'],
    prefix='/scraper'
)


@router.post('/dental_stall', status_code=status.HTTP_202_ACCEPTED,  response_model=ScrapeResponseSchema)
def scrap(request: ScrapeRequestSchema, credentials: HTTPAuthorizationCredentials = Depends(authenticate_request)):
    # when getting any request add it to the queue
    try:
        event_payload = {
            'request': request.dict(),
            'retry_count': 0,
            'user': User.get_user()
        }
        queue_manager = QueueManager()
        queue_manager.add_to_queue(scrap_req=event_payload)

        return ScrapeResponseSchema(message="Request received and added to the queue, we will process and notify you soon.", status=status.HTTP_202_ACCEPTED)

    # TODO: @Madhav to handle error in more detailed way
    except Exception as ex:
        raise ex

    """
        TODO: @Madhav to re-visit this in future
        if data in cache:
            return data from cache
        else:
            add the item in the queue
    """
