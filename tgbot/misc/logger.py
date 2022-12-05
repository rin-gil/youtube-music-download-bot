"""Enables logging"""

from logging import basicConfig, getLogger, INFO, Logger

from tgbot.config import LOG_FILE


logger: Logger = getLogger(__name__)
basicConfig(
    filename=LOG_FILE,
    level=INFO,
    format="%(levelname)-8s %(filename)s:%(lineno)d [%(asctime)s] - %(name)s - %(message)s",
)
