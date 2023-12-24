import os
from typing import Optional
from datetime import timedelta, datetime

from dotenv import load_dotenv

from jose import jwt

from fastapi import APIRouter, Body, HTTPException, Request, Response, status

from src.helpers.custom_response import error_response, valid_response
from src.helpers.rbac_decorator import role_based_access
from src.helpers.extract_jwt import extract_jwt_token
from src.helpers.validation_decorator import validate

from src.controllers.authentication_operations import AuthenticationOperations

from src.schemas.login_schema import login_schema
from src.schemas.change_password_schema import change_password_schema

from src.helpers.logger_config import CustomLogger


logger = CustomLogger(__name__)
router = APIRouter(prefix="", tags=["auth_operations"])

load_dotenv()


@router.post("/login")
@validate(login_schema)
def login(response: Response, body_data=Body()):
    """login using username and password

    Args:
        response (Response): setting cookies
        body_data : data containing username and password


    Returns:
        dict: login successfully response
    """
    logger.debug("Entering login function")

    auth = AuthenticationOperations(body_data["username"], body_data["password"])
    userAuth, user_details = auth.login()
    logger.debug("User details retrieved")

    if userAuth is not None:
        user_id = userAuth[0]
        username = userAuth[1]
        role = userAuth[3]
        name = user_details[1]

        access_token = __create_access_token(user_id, username, role, name)
        logger.debug("Access token created successfully")

        logger.info("Login successful")
        json_valid_response = {
            "jwt_token": access_token,
            "code": 200,
            "details": "Login Successfully",
            "status": "success",
        }
        return json_valid_response

    logger.error("Invalid Credentials")
    raise HTTPException(
        status.HTTP_401_UNAUTHORIZED, error_response(401, "Invalid Credentials")
    )


def __create_access_token(
    user_id,
    username,
    role,
    name,
    expires_delta: Optional[timedelta] = timedelta(minutes=120),
):
    """create a new access token

    Args:
        user_id (int):  ID of the user
        username (string):  username of the user
        role (string):  role of the user
        expires_delta (Optional[timedelta], optional): expire time of token in minutes. Defaults to 20 Min.

    Returns:
        string: jwt access token
    """
    logger.debug("Creating access token")

    encode = {
        "sub": username,
        "user_id": user_id,
        "role": role,
        "name": name,
    }
    expire = datetime.utcnow() + expires_delta

    encode.update({"exp": expire})
    return jwt.encode(encode, os.getenv("SECRET_KEY"), os.getenv("ALGORITHM"))


@router.put("/changepassword")
@validate(change_password_schema)
@role_based_access(["Customer", "Cashier", "Manager"])
def change_password(request: Request, body_data=Body()):
    """change_password

    Args:
        request (Request): Fast API request object
        body_data (dict): username and password

    Returns:
        dict: Json Response object
    """
    logger.debug("Entering change_password function")

    user_details = extract_jwt_token(request)
    logger.debug("User details extracted successfully")

    user_id = user_details["user_id"]
    old_password = body_data["old_password"]
    new_password = body_data["new_password"]

    if old_password == new_password:
        logger.error("Make sure old and new password are different.")
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            error_response(400, "Make Sure old and new password are different."),
        )

    instance = AuthenticationOperations()
    response = instance.change_password(user_id, old_password, new_password)

    if response:
        logger.info("Password changed successfully")
        return valid_response(200, "Password Updated Successfully.")
    else:
        logger.debug(f"Password not changed details: {response}")
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            error_response(401, "Invalid old password."),
        )
