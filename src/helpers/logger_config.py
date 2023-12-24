import logging


def initialize_main_logger(logger_name):
    logger = logging.getLogger(logger_name)

    logging.basicConfig(
        filename="main.log",
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    return logger


class CustomLogger:
    """This class implements logging methods for logging"""

    def __init__(self, logger_name):
        self.logger = logging.getLogger(logger_name)

    def debug(self, message):
        """Log a debug message

        Args:
            message (String):  The error message
        """
        self.logger.debug(message)

    def info(self, message):
        """Log a info message

        Args:
            message (String):  The error message
        """
        self.logger.info(message)

    def warning(self, message):
        """Log a warning message

        Args:
            message (String):  The error message
        """
        self.logger.warning(message)

    def error(self, message):
        """Log a critical message

        Args:
            message (String):  The error message
        """
        self.logger.error(message)

    def critical(self, message):
        """Log a critical message

        Args:
            message (String):  The error message
        """
        self.logger.critical(message)
