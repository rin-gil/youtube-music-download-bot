"""Handles errors"""

from aiogram import Dispatcher
from aiogram.types import Update
from aiogram.utils.exceptions import TelegramAPIError

from tgbot.middlewares.localization import i18n
from tgbot.misc.logger import logger
from tgbot.misc.states import UserInput

_ = i18n.gettext  # Alias for gettext method


async def errors_handler(update: Update, exception: TelegramAPIError) -> bool:
    """Logs exceptions that have occurred and are not handled by other functions"""
    if update.message:
        await update.bot.send_message(
            chat_id=update.message.chat.id,
            text="❌ " + _("Error when searching for a video", locale=update.message.from_user.language_code),
            reply_to_message_id=update.message.message_id,
        )
        logger.error(
            "When processing the update with id=%s there was a unhandled error: %s. Message text: %s.",
            update.update_id,
            exception,
            update.message.text,
        )
    elif update.callback_query:
        await update.bot.send_message(
            chat_id=update.callback_query.message.chat.id,
            text="❌ " + _("Error downloading the video", locale=update.callback_query.from_user.language_code),
        )
        logger.error(
            "When processing the update with id=%s there was a unhandled error: %s. Message text: %s.",
            update.update_id,
            exception,
            update.callback_query.message.text,
        )
    else:
        logger.error(
            "When processing the update with id=%s there was a unhandled error: %s",
            update.update_id,
            exception,
        )
    await UserInput.previous()
    return True


def register_errors(dp: Dispatcher) -> None:
    """Registers errors handlers"""
    dp.register_errors_handler(errors_handler)
