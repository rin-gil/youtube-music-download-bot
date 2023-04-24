"""Handlers of callbacks from user"""

from os import remove as os_remove

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InputFile

from tgbot.misc.states import UserInput
from tgbot.middlewares.localization import i18n
from tgbot.services.database import database
from tgbot.services.youtube import get_path_to_audio_file


_ = i18n.gettext  # Alias for gettext method


async def if_user_clicks_download(call: CallbackQuery, state: FSMContext) -> None:
    """Handles clicks on the Download button in search results"""
    await UserInput.Block.set()  # Block user actions while the download is in progress.

    user_lang_code: str = call.from_user.language_code
    chat_id: int = call.from_user.id

    # If there is data in RAM in state.proxy()
    try:
        async with state.proxy() as data:
            await call.bot.edit_message_text(
                text="⏬ " + _("Downloading, wait a bit...", locale=user_lang_code),
                chat_id=chat_id,
                message_id=data["bot_reply_id"],
            )
            await call.answer(cache_time=1)
            for bot_answer_id in data["bot_answers_ids"]:  # Deleting search results from chat
                await call.bot.delete_message(chat_id=chat_id, message_id=bot_answer_id)

        audio_file: str = await get_path_to_audio_file(url=call.data)
        await call.bot.send_audio(
            chat_id=chat_id, audio=InputFile(audio_file), reply_to_message_id=data["user_message_id"]
        )
        await call.bot.delete_message(chat_id=chat_id, message_id=data["bot_reply_id"])
        os_remove(audio_file)
        await database.increase_downloads_counter()

    # If the bot was restarted and now there is no data in RAM in state.proxy()
    except KeyError:
        await call.answer(text="❌ " + _("This link is out of date", locale=user_lang_code), cache_time=1)
        await call.bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)

    await state.reset_state(with_data=True)  # Download completed, unblock user actions.


def register_callbacks(dp: Dispatcher) -> None:
    """Registers callback handlers"""
    dp.register_callback_query_handler(if_user_clicks_download, state=None)
