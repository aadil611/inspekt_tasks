import logging
from logging.handlers import RotatingFileHandler
import os


LOG_DIR = "logs"
LOG_FILE = "app.log"

os.makedirs(LOG_DIR, exist_ok=True)

LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"


def get_logger(module_name: str) -> logging.Logger:
    """return a Logger object for specific module"""
    logger = logging.getLogger(module_name)
    formatter = logging.Formatter(LOG_FORMAT, datefmt="%Y-%m-%d %H:%M:%S")
    logger.setLevel(logging.DEBUG)

    # file handler
    file_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, LOG_FILE), maxBytes=1024 * 1024 * 5, backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
