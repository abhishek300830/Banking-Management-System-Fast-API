import functools
from fastapi import HTTPException, status

import jsonschema

from src.helpers.custom_response import error_response


def validate(schema):
    """validate a JSON schema

    Args:
        schema : a JSON schema to validate with body_data of the request
    """

    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            body_data = kwargs.get("body_data")
            try:
                jsonschema.validate(instance=body_data, schema=schema)
            except jsonschema.ValidationError as error:
                raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    error_response(404, error.message),
                )

            return function(*args, **kwargs)

        return wrapper

    return decorator
