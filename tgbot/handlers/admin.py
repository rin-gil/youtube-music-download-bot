"""Message handlers for administrators"""

from os import remove as os_remove

from aiogram import Dispatcher
from aiogram.types import InputFile, Message

from tgbot.middlewares.localization import i18n
from tgbot.services.database import database
from tgbot.services.statistics import bot_statistics

_ = i18n.gettext  # Alias for gettext method


async def if_admin_sent_command_stats(message: Message) -> None:
    """Shows statistics for administrators"""
    lang_code: str = message.from_user.language_code
    path_to_statistics_graph: str = await bot_statistics.get_path_to_statistics_graph(
        await database.get_statistics_data(), lang_code
    )
    await message.reply_photo(
        photo=InputFile(path_to_statistics_graph),
        caption="📊 " + _("Bot statistics by months", locale=lang_code),
    )
    os_remove(path_to_statistics_graph)


def register_admin(dp: Dispatcher) -> None:
    """Registers admin handlers"""
    dp.register_message_handler(if_admin_sent_command_stats, commands="stats", state=None, is_admin=True)
