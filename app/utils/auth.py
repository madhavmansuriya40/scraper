import os
from fastapi import Depends, HTTPException, status
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


# static token, can be dynamic in future
STATIC_TOKEN = os.getenv('STATIC_TOKEN')

# HTTPBearer for static token authentication
token_auth_scheme = HTTPBearer()


def authenticate_request(credentials: HTTPAuthorizationCredentials = Depends(token_auth_scheme)) -> None:
    if credentials.credentials != STATIC_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")
