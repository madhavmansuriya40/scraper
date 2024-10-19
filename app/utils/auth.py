# external imports
from fastapi import Depends, HTTPException, status, Header
from fastapi import HTTPException, status


# Define your static token here
STATIC_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1hZEBtYXguY29tIn0.liqUJFFkNq5O_-lwWnF12xMzRhfV-vrxY1dYM0HRd9s"


def authenticate_token(authorization: str = Header(...)):
    # Extract token from the Authorization header
    token_type, token = authorization.split(" ")
    if token_type != "Bearer" or token != STATIC_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
