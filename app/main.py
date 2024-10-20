import asyncio
from fastapi import FastAPI, Depends
from routers import scraper
from fastapi.security import HTTPAuthorizationCredentials
from utils.auth import authenticate_request
from utils.queue import RabbitMQConnection

app = FastAPI()
rabbitmq_conn = RabbitMQConnection()


@app.on_event("startup")
async def startup_event():
    await asyncio.sleep(5)
    rabbitmq_conn.connect()


@app.get("/ready")
def ready(credentials: HTTPAuthorizationCredentials = Depends(authenticate_request)):
    return 'Service Up and Running! 😈'


# adding routes
app.include_router(scraper.router)
