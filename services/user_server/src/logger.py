import logging
from logging.handlers import RotatingFileHandler
import os
from src.settings import EnvironmentOption, serverSettings
from tortoise.log import logger as tortoise_logger, db_client_logger
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

fmt = logging.Formatter(
        fmt="%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

logger = logging.getLogger('')
shell_handler = logging.StreamHandler(sys.stdout)
shell_handler.setLevel(LOGGING_LEVEL)
shell_handler.setFormatter(fmt)

file_handler = RotatingFileHandler(
    LOG_FILE_PATH, maxBytes=10485760, backupCount=5)
file_handler.setLevel(LOGGING_LEVEL)
file_handler.setFormatter(fmt)

logger.addHandler(file_handler)
logger.addHandler(shell_handler)

tortoise_logger.setLevel(LOGGING_LEVEL)
tortoise_logger.addHandler(shell_handler)
db_client_logger.setLevel(LOGGING_LEVEL)
db_client_logger.addHandler(shell_handler)
