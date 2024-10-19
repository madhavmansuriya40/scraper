from fastapi import APIRouter, Depends
from schemas.schemas import ScrapeRequestSchema, UserSchema
from utils.auth import authenticate_token
from scrapers.dental_stall_scraper import DentalStallScraper
from json_database import JSONDatabase


router = APIRouter(
    tags=['scrapers'],
    prefix='/scraper'
)


@router.post('/dental_stall')
def create_blog(request: ScrapeRequestSchema, token: UserSchema = Depends(authenticate_token)):
    try:
        scrapped_data = DentalStallScraper.scrape_catalogue(request)
        JSONDatabase.save_data(data=scrapped_data)
    # TODO @madhav to re-visit and add septate exceptions
    except Exception as ex:  # the exception can be streamlined to a specific exception
        raise ex
