"""Handlers of messages from user"""

from os import remove as os_remove

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InputFile, Message
from aiogram.utils.exceptions import MessageToDeleteNotFound

from tgbot.config import MAX_DURATION
from tgbot.keyboards.inline import create_download_kb
from tgbot.middlewares.localization import i18n
from tgbot.misc.states import UserInput
from tgbot.services.database import database
from tgbot.services.youtube import youtube, VideoInfo

_ = i18n.gettext  # Alias for gettext method


async def if_user_sent_youtube_link(message: Message, state: FSMContext) -> None:
    """Handles the message if a user sent YouTube link"""
    await database.increase_downloads_counter()
    user_lang_code: str = message.from_user.language_code
    await UserInput.Block.set()  # Block user input while the download is in progress
    bot_reply: Message = await message.reply(text="⏬ " + _("Downloading, wait a bit...", locale=user_lang_code))
    chat_id: int = message.from_user.id
    bot_reply_id: int = bot_reply.message_id
    path_to_audio_file: str | None = await youtube.download_audio(message.text)
    if path_to_audio_file:
        await message.reply_audio(audio=InputFile(path_to_audio_file))
        await message.bot.delete_message(chat_id=chat_id, message_id=bot_reply_id)
        os_remove(path_to_audio_file)
    else:
        await message.bot.edit_message_text(
            text="❌ "
            + _("Failed to download an audio file", locale=user_lang_code)
            + "\n\n"
            + _("Possible reasons:", locale=user_lang_code)
            + "\n"
            + "  - "
            + _("video is unavailable", locale=user_lang_code)
            + "\n"
            + "  - "
            + _("video with limited access", locale=user_lang_code)
            + "\n"
            + "  - "
            + _("this is a live broadcast", locale=user_lang_code)
            + "\n"
            + "  - "
            + _("video is longer than", locale=user_lang_code)
            + f" {MAX_DURATION} "
            + _("seconds", locale=user_lang_code),
            chat_id=chat_id,
            message_id=bot_reply_id,
        )
    await state.reset_state()  # Unblock user input, when download completed


async def if_user_sent_link_not_to_youtube(message: Message) -> None:
    """Handles the message if the user sent a link other than YouTube"""
    user_lang_code: str = message.from_user.language_code
    await message.reply(text="❌ " + _("It doesn't look like a YouTube link", locale=user_lang_code))


async def if_user_sent_text(message: Message, state: FSMContext) -> None:
    """Handles the message if a user sent text"""
    await database.increase_searches_counter()
    await UserInput.Block.set()  # Block user actions while the search is in progress.

    user_lang_code: str = message.from_user.language_code
    chat_id: int = message.from_user.id

    # If there are previous search results in the chat, delete them
    async with state.proxy() as data:
        if data.get("bot_answers_ids"):
            try:
                await message.bot.delete_message(chat_id=chat_id, message_id=data["user_message_id"])
                await message.bot.delete_message(chat_id=chat_id, message_id=data["bot_reply_id"])
                for bot_answer_id in data["bot_answers_ids"]:
                    await message.bot.delete_message(chat_id=chat_id, message_id=bot_answer_id)
            except MessageToDeleteNotFound:
                pass
    await state.reset_data()

    # Starting a new search
    bot_reply: Message = await message.reply(text="🔍 " + _("Looking, wait a bit...", locale=user_lang_code))
    bot_reply_id: int = bot_reply.message_id
    search_results: list[VideoInfo] | None = await youtube.search_videos(message.text, user_lang_code)

    # If the search results are not empty
    if search_results:
        await message.bot.edit_message_text(
            text="👇 " + _("Look what I found", locale=user_lang_code) + ":",
            chat_id=chat_id,
            message_id=bot_reply_id,
        )
        bot_answers: list = []
        for result in search_results:  # Display the search results
            bot_answer: Message = await message.answer(
                text=result.description,
                reply_markup=await create_download_kb(callback_data=result.url, lang_code=user_lang_code),
            )
            bot_answers.append(bot_answer.message_id)
        async with state.proxy() as data:  # Store search results in RAM
            data["user_message_id"] = message.message_id
            data["bot_reply_id"] = bot_reply_id
            data["bot_answers_ids"] = bot_answers

    # If the search results are empty
    else:
        await message.bot.edit_message_text(
            text="❌ "
            + _("I didn't find anything", locale=user_lang_code)
            + "\n"
            + _("Try looking for something else", locale=user_lang_code)
            + " 😒",
            chat_id=chat_id,
            message_id=bot_reply_id,
        )

    await state.reset_state(with_data=False)  # Search completed, unblock user actions.


async def if_user_input_block(message: Message) -> None:
    """Deletes all user messages in the UserInput.Block state"""
    await message.delete()


async def if_user_sent_anything_but_text(message: Message) -> None:
    """Deletes messages with any content from a user that is not text"""
    await message.delete()


def register_messages(dp: Dispatcher) -> None:
    """Registers message handlers, the sequence of registering handlers is important!"""
    dp.register_message_handler(
        if_user_sent_youtube_link,
        Text(startswith="https://"),
        regexp=(
            r"(?:https?://)?(?:www\.)?"
            r"(?:youtube\.com/(?:watch\?v=|embed/)|youtu\.be/|youtube.com/shorts/)"
            r"([a-zA-Z0-9_-]{11})"
        ),
        state=None,
    )
    dp.register_message_handler(if_user_sent_link_not_to_youtube, Text(startswith="https://"), state=None)
    dp.register_message_handler(if_user_sent_text, content_types=types.ContentTypes.TEXT, state=None)
    dp.register_message_handler(if_user_input_block, content_types=types.ContentTypes.TEXT, state=UserInput.Block)
    dp.register_message_handler(if_user_sent_anything_but_text, content_types=types.ContentTypes.ANY)
