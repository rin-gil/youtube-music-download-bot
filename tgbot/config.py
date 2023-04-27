"""Configuration settings for the bot"""

from os.path import join, normpath
from pathlib import Path
from typing import NamedTuple

from environs import Env


_BASE_DIR: Path = Path(__file__).resolve().parent.parent
DB_FILE: str = normpath(join(_BASE_DIR, "tgbot/db.sqlite3"))
LOCALES_DIR: str = normpath(join(_BASE_DIR, "tgbot/locales"))
TEMP_DIR: str = normpath(join(_BASE_DIR, "tgbot/temp"))
LOG_FILE: str = join(_BASE_DIR, "log.log")
BOT_LOGO: str = normpath(join(_BASE_DIR, "tgbot/assets/img/bot_logo.jpg"))
STATS_BG_IMAGE: str = normpath(join(_BASE_DIR, "tgbot/assets/img/stats_bg.png"))

MAX_DURATION: int = 900  # in seconds


class TgBot(NamedTuple):
    """Bot token"""

    token: str
    admin_ids: tuple[int, ...]


class Config(NamedTuple):
    """Bot config"""

    tg_bot: TgBot


def load_config() -> Config:
    """Loads tokens from environment variables"""
    env: Env = Env()
    env.read_env()
    return Config(tg_bot=TgBot(token=env.str("BOT_TOKEN"), admin_ids=tuple(map(int, env.list("ADMINS")))))
