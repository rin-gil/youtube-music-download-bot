"""Configuration settings for the bot"""

from os.path import join, normpath
from pathlib import Path
from typing import NamedTuple

from environs import Env


class DbConfig(NamedTuple):
    """Database configuration"""

    host: str
    port: str
    password: str
    user: str
    database: str


class RedisConfig(NamedTuple):
    """Redis database configuration"""

    host: str
    port: int
    database_index: int
    password: str


class WebhookCredentials(NamedTuple):
    """Represents credentials to use webhook"""

    wh_host: str
    wh_path: str
    wh_token: str
    app_host: str
    app_port: int


class TgBot(NamedTuple):
    """Bot token"""

    token: str
    admin_ids: tuple[int, ...]


class Config(NamedTuple):
    """Bot config"""

    tg_bot: TgBot
    db: DbConfig
    redis: RedisConfig | None
    webhook: WebhookCredentials | None


# Change USE_WEBHOOK to True to use a webhook instead of long polling
USE_WEBHOOK: bool = False

# Change USE_REDIS to True to use redis storage for FSM instead of memory
USE_REDIS: bool = False

_BASE_DIR: Path = Path(__file__).resolve().parent.parent
LOCALES_DIR: str = normpath(join(_BASE_DIR, "tgbot/locales"))
TEMP_DIR: str = normpath(join(_BASE_DIR, "tgbot/temp"))
LOG_FILE: str = join(_BASE_DIR, "youtube-music-download-bot.log")
BOT_LOGO: str = normpath(join(_BASE_DIR, "tgbot/assets/img/bot_logo.jpg"))
STATS_BG_IMAGE: str = normpath(join(_BASE_DIR, "tgbot/assets/img/stats_bg.png"))

MAX_DURATION: int = 900  # in seconds


def load_config() -> Config:
    """Loads tokens from environment variables"""
    env: Env = Env()
    env.read_env()
    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=tuple(map(int, env.list("ADMINS"))),
        ),
        db=DbConfig(
            host=env.str("POSTGRES_DB_HOST"),
            port=env.str("POSTGRES_DB_PORT"),
            password=env.str("POSTGRES_DB_PASSWORD"),
            user=env.str("POSTGRES_DB_USER"),
            database=env.str("POSTGRES_DB_NAME"),
        ),
        redis=(
            RedisConfig(
                host=env.str("REDIS_HOST"),
                port=env.int("REDIS_PORT"),
                database_index=env.int("REDIS_DB_INDEX"),
                password=env.str("REDIS_DB_PASS"),
            )
            if USE_REDIS
            else None
        ),
        webhook=(
            WebhookCredentials(
                wh_host=env.str("WEBHOOK_HOST"),
                wh_path=env.str("WEBHOOK_PATH"),
                wh_token=env.str("WEBHOOK_TOKEN"),
                app_host=env.str("APP_HOST"),
                app_port=env.int("APP_PORT"),
            )
            if USE_WEBHOOK
            else None
        ),
    )
