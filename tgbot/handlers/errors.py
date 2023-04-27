"""Handles errors"""

from aiogram import Dispatcher
from aiogram.types import Update
from aiogram.utils.exceptions import TelegramAPIError

from tgbot.middlewares.localization import i18n
from tgbot.misc.logger import logger

_ = i18n.gettext  # Alias for gettext method


async def errors_handler(update: Update, exception: TelegramAPIError) -> bool:
    """Logs exceptions that have occurred and are not handled by other functions"""
    message_from_user: str | None = None
    chat_id: int | None = None
    user_lang_code: str | None = None

    if update.message:
        chat_id = update.message.chat.id
        user_lang_code = update.message.from_user.language_code
        message_from_user = update.message.text

    if update.callback_query:
        chat_id = update.callback_query.message.chat.id
        user_lang_code = update.callback_query.from_user.language_code

    if update.message or update.callback_query:
        await update.bot.send_message(
            chat_id=chat_id,
            text="❌ " + _("Unexpected error. We will fix it in the near future.", locale=user_lang_code),
        )

    logger.error(
        "When processing the update with id=%s there was a unhandled error: %s. Message text: %s.",
        update.update_id,
        repr(exception),
        message_from_user,
    )

    # Reset FSM state, if necessary
    dp: Dispatcher = Dispatcher.get_current()
    if await dp.storage.get_state(chat=chat_id) == "UserInput:Block":
        await dp.storage.reset_state(chat=chat_id, with_data=True)

    return True


def register_errors(dp: Dispatcher) -> None:
    """Registers errors handlers"""
    dp.register_errors_handler(errors_handler)
