def error_response(status_code: int, message):
    """custom defined error response

    Args:
        status_code (int): status code of response
        error (error): error generated

    Returns:
        dict: return dict with error message
    """

    return {
        "error": {
            "code": status_code,
            "message": message,
        },
        "status": "failure",
    }


def valid_response(status_code: int, message):
    """custom defined valid response

    Args:
        status_code (int): status code of response
        message (string): message for valid response

    Returns:
        dict: dictionary with valid response
    """
    return {
        "code": status_code,
        "details": message,
        "status": "success",
    }


def valid_data_response(status_code: int, data):
    """valid data response for valid response

    Args:
        status_code (int): status code of response
        data : data for valid response

    Returns:
        dict: json with valid responses
    """
    return {
        "code": status_code,
        "data": data,
        "status": "success",
    }
