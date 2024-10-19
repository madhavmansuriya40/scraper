from typing import Optional

from pydantic import BaseModel, AnyHttpUrl, Field, conint
from pydantic import BaseModel


class ScrapeRequestSchema(BaseModel):
    url: str
    page_limit: int
    proxy_url: Optional[str]


class UserSchema(BaseModel):
    name: str
    email: str
    password: str


class TokenData(BaseModel):
    email: str | None = None
