"""Enables logging"""

import logging

from tgbot.config import LOG_FILE


logger: logging.Logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(levelname)-8s %(filename)s:%(lineno)d [%(asctime)s] - %(name)s - %(message)s",
)
