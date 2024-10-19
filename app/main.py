from fastapi import FastAPI
from routers import scraper

app = FastAPI()

# Scraping function


@app.get("/ready")
def ready():
    return 'Service Up and Running! 😈'


# adding routes
app.include_router(scraper.router)
