import functools


def basic_logger(logger):
    """THis is a logging decorator

    Args:
        logger : logger to log messages
    """

    def decorator(fun):
        @functools.wraps(fun)
        def wrapper(*args, **kwargs):
            operation = fun.__name__
            logger.debug(f"{operation} called with {(args, kwargs)}.")
            response = fun(*args, **kwargs)
            logger.debug(f"{operation} returned {response}.")

            return response

        return wrapper

    return decorator
