from typing import Optional

from pydantic import BaseModel
from pydantic import BaseModel


class ScrapeRequestSchema(BaseModel):
    url: str
    page_limit: int
    proxy_url: Optional[str]


class ScrapeResponseSchema(BaseModel):
    message: str
    status: int

    class Config:
        schema_extra = {
            "example": {
                "message": "Request received and added to the queue.",
                "status": 202
            }
        }


class UserSchema(BaseModel):
    name: str
    email: str
    password: str


class TokenData(BaseModel):
    email: str | None = None
