from dataclasses import dataclass
from os import path
from pathlib import Path

from environs import Env

BANNED_CONTENT: tuple = ('animation', 'audio', 'contact', 'document', 'game', 'location', 'photo',
                         'pinned_message', 'poll', 'sticker', 'video', 'video_note', 'voice')

DOWNLOAD_FOLDER: str = path.join(Path(__file__).resolve().parent, 'downloads')
MAX_VIDEO_DURATION: int = 900


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot


def load_config():
    env = Env()
    env.read_env()
    return Config(tg_bot=TgBot(token=env.str('BOT_TOKEN')))
