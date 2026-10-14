import logging.config
from logging_reference import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)

logger.error("Log with info-level severity")