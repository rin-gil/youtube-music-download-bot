"""Handlers of commands from user"""

from aiogram import Dispatcher
from aiogram.types import InputFile, Message

from tgbot.config import BOT_LOGO
from tgbot.middlewares.localization import i18n

_ = i18n.gettext  # Alias for gettext method


async def if_user_sent_command_start(message: Message) -> None:
    """Handles command /start from the user"""
    lang_code: str = message.from_user.language_code
    answer_text: str = (
        _("Write me the name of the song or drop me a link to video from", locale=lang_code)
        + ' <a href="https://www.youtube.com">YouTube</a>. 😉'
    )
    await message.answer_photo(photo=InputFile(BOT_LOGO), caption=answer_text)


async def if_user_sent_command_about(message: Message) -> None:
    """Handles command /about from the user"""
    lang_code: str = message.from_user.language_code
    answer_text: str = (
        _("I can download songs from", locale=lang_code)
        + ' <a href="https://www.youtube.com">YouTube</a>!\n\n'
        + _("Write me the name of the song or drop me a link to the video", locale=lang_code)
    )
    await message.answer_photo(photo=InputFile(BOT_LOGO), caption=answer_text)


def register_commands(dp: Dispatcher) -> None:
    """Registers command handlers"""
    dp.register_message_handler(if_user_sent_command_start, commands="start", state=None)
    dp.register_message_handler(if_user_sent_command_about, commands="about", state=None)
