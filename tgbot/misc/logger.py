"""Enables logging"""

import logging
import sys

from tgbot.config import LOG_FILE


sys.tracebacklimit = 0


logger: logging.Logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.WARNING,
    format="%(levelname)-8s %(filename)s:%(lineno)d [%(asctime)s] - %(name)s - %(message)s",
)

# Removes the pytube module warning:
# Unexpected renderer encountered. Renderer name: dict_keys(['reelShelfRenderer'])
# appearing when pytube search results include videos from YouTube Shorts
pytube_logger = logging.getLogger("pytube")
pytube_logger.setLevel(logging.ERROR)
