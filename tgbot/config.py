"""Configuration settings for the bot"""

from os.path import join, normpath
from pathlib import Path
from typing import NamedTuple

from environs import Env


_BASE_DIR: Path = Path(__file__).resolve().parent.parent
LOCALES_DIR: str = normpath(join(_BASE_DIR, "tgbot/locales"))
TEMP_DIR: str = normpath(join(_BASE_DIR, "tgbot/temp"))
LOG_FILE: str = join(_BASE_DIR, "log.log")
BOT_LOGO: str = normpath(join(_BASE_DIR, "tgbot/assets/img/bot_logo.png"))

MAX_VIDEO_DURATION: int = 1200  # in seconds


class TgBot(NamedTuple):
    """Bot token"""

    token: str


class Config(NamedTuple):
    """Bot config"""

    tg_bot: TgBot


def load_config() -> Config:
    """Loads tokens from environment variables"""
    env = Env()
    env.read_env()
    return Config(tg_bot=TgBot(token=env.str("BOT_TOKEN")))
