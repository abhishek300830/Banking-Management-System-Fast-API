import os
from dotenv import load_dotenv

from fastapi import HTTPException, Request
from jose import JWTError, jwt

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def extract_jwt_token(request: Request):
    """Extract JWT token from request

    Args:
        request (Request): request from which JWT token is extracted

    Returns:
        dict: details of JWT token extracted from request
    """
    try:
        tokenAuth = request.headers.get("Authorization")

        if tokenAuth is None:
            return None

        token = tokenAuth.split(" ")[1]

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_name: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        role: int = payload.get("role")

        return {
            "username": user_name,
            "user_id": user_id,
            "role": role,
        }

    except JWTError as error:
        raise HTTPException(status_code=404, detail=str(error))
