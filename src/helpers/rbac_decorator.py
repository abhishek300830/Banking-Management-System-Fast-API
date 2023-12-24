import functools

from fastapi import HTTPException, status
from src.helpers.custom_response import error_response

from src.helpers.extract_jwt import extract_jwt_token


def role_based_access(role_list):
    """this is a decorator which validate the user role and allow or deny according to the access privilges

    Args:
        role_list (list): list of role allowed for that endpoint
    """

    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            request = kwargs.get("request")
            user_details = extract_jwt_token(request)
            if user_details is None:
                raise HTTPException(
                    status.HTTP_403_FORBIDDEN,
                    error_response(403, "Not Authorized to access this resource"),
                )

            role = user_details["role"]
            if role in role_list:
                return function(*args, **kwargs)

            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                error_response(403, "Not Authorized to access this resource"),
            )

        return wrapper

    return decorator
