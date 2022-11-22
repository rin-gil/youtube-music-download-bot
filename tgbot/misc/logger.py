"""Enables logging"""

from logging import basicConfig, getLogger, INFO, Logger

from tgbot.config import LOG_FILE


log: Logger = getLogger(__name__)
basicConfig(
    filename=LOG_FILE,
    level=INFO,
    format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
)
