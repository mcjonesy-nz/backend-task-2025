import logging
import os
import json

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger  # Prevent duplicate handlers in Lambda

    logger.setLevel(LOG_LEVEL)

    handler = logging.StreamHandler()

    formatter = logging.Formatter(
        json.dumps({
            "level": "%(levelname)s",
            "logger": "%(name)s",
            "message": "%(message)s",
            "timestamp": "%(asctime)s"
        })
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
