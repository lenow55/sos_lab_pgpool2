import logging
from logging.handlers import RotatingFileHandler
import os
from src.core.settings import EnvironmentOption, serverSettings
#from tortoise.log import logger as tortoise_logger, db_client_logger
import sys

LOG_DIR = os.path.join(os.path.dirname(
    os.path.dirname(__file__)), 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE_PATH = os.path.join(LOG_DIR, 'app.log')

if serverSettings.environment == EnvironmentOption.DEBUG:
    LOGGING_LEVEL = logging.DEBUG
else:
    LOGGING_LEVEL = logging.INFO

#tortoise_logger.setLevel(LOGGING_LEVEL)
#db_client_logger.setLevel(LOGGING_LEVEL)


def configureLogger(logger: logging.Logger):
    level = LOGGING_LEVEL
    fmt = logging.Formatter(
        fmt="%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",)

    shell_handler = logging.StreamHandler(
        sys.stdout)
    shell_handler.setLevel(level)
    shell_handler.setFormatter(fmt)

    file_handler = RotatingFileHandler(
        LOG_FILE_PATH, maxBytes=10485760, backupCount=5)
    file_handler.setLevel(level)
    file_handler.setFormatter(fmt)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(shell_handler)
    return logger

