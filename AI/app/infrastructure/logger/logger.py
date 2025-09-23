import logging
import os
import sys
from logging.handlers import RotatingFileHandler


class Logger:
    """
    Logger class for logging messages to the console and file.
    """

    def __init__(self, name: str):
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.INFO)

        # Prevent adding handlers multiple times
        if self._logger.handlers:
            return

        # Prevent propagation to root logger to avoid duplicates
        self._logger.propagate = False

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(console_format)

        # File handler - only add if logs directory exists or can be created
        try:
            # Ensure logs directory exists
            os.makedirs("logs", exist_ok=True)

            file_handler = RotatingFileHandler(
                "logs/app.log",
                maxBytes=10485760,
                backupCount=5,  # 10MB
            )
            file_handler.setLevel(logging.INFO)
            file_format = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            file_handler.setFormatter(file_format)
            self._logger.addHandler(file_handler)
        except (OSError, PermissionError):
            # If we can't create the logs directory or file, just use console logging
            # This is common in CI environments or read-only filesystems
            pass

        self._logger.addHandler(console_handler)

    def info(self, message: str) -> None:
        self._logger.info(message)

    def error(self, message: str) -> None:
        self._logger.error(message)

    def warning(self, message: str) -> None:
        self._logger.warning(message)

    def debug(self, message: str) -> None:
        self._logger.debug(message)

    def critical(self, message: str) -> None:
        self._logger.critical(message)


def setup_logger(name: str) -> Logger:
    return Logger(name)
