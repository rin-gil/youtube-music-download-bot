"""Configuration settings for the bot"""

from dataclasses import dataclass
from os.path import join
from pathlib import Path

from environs import Env


_BASE_DIR: Path = Path(__file__).resolve().parent
LOCALES_DIR: str = join(_BASE_DIR, "locales")
TEMP_DIR: str = join(_BASE_DIR, "temp")
LOG_FILE: str = join(_BASE_DIR, "YoutubeMusicDownloadBot.log")
BOT_LOGO: str = join(_BASE_DIR, "assets/img/bot_logo.png")

MAX_VIDEO_DURATION: int = 1200  # in seconds


@dataclass
class TgBot:
    """Bot token"""

    token: str


@dataclass
class Config:
    """Bot config"""

    tg_bot: TgBot


def load_config() -> Config:
    """Loads tokens from environment variables"""
    env = Env()
    env.read_env()
    return Config(tg_bot=TgBot(token=env.str("BOT_TOKEN")))
