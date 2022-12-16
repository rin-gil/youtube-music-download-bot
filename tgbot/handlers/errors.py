"""Handles errors"""

from aiogram import Dispatcher
from aiogram.types import Update
from aiogram.utils.exceptions import TelegramAPIError

from tgbot.misc.logger import logger


async def errors_handler(update: Update, exception: TelegramAPIError) -> bool:
    """Logs exceptions that have occurred and are not handled by other functions"""
    logger.error("When processing the update with id=%s there was a unhandled error: %s", update.update_id, exception)
    return True


def register_errors(dp: Dispatcher) -> None:
    """Registers errors handlers"""
    dp.register_errors_handler(errors_handler)
