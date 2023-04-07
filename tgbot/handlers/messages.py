"""Handlers of messages from user"""

from asyncio import get_running_loop
from os import remove as os_remove

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InputFile, Message

from tgbot.keyboards.inline import create_download_kb
from tgbot.middlewares.localization import i18n
from tgbot.misc.states import UserInput
from tgbot.services.youtube import (
    check_video_availability,
    get_path_to_audio_file,
    VideoAvailability,
    search_videos,
    VideoCard,
)

_ = i18n.gettext  # Alias for gettext method


async def if_user_sent_youtube_link(message: Message, state: FSMContext) -> None:
    """Handles the message if a user sent YouTube link"""
    user_lang_code: str = message.from_user.language_code
    await UserInput.Block.set()  # Block user input while the download is in progress
    bot_reply: Message = await message.reply(text="⏬ " + _("Downloading, wait a bit...", locale=user_lang_code))
    chat_id: int = message.from_user.id
    bot_reply_id: int = bot_reply.message_id
    video: VideoAvailability = await check_video_availability(url=message.text, lang_code=user_lang_code)
    if video.available:
        path_to_audio_file: str = await get_path_to_audio_file(url=message.text)
        await message.reply_audio(audio=InputFile(path_to_audio_file))
        await message.bot.delete_message(chat_id=chat_id, message_id=bot_reply_id)
        os_remove(path_to_audio_file)
    else:
        await message.bot.edit_message_text(text=f"❌ {video.description}", chat_id=chat_id, message_id=bot_reply_id)
    await state.reset_state()  # Unblock user input, when download completed


async def if_user_sent_link_not_to_youtube(message: Message) -> None:
    """Handles the message if the user sent a link other than YouTube"""
    user_lang_code: str = message.from_user.language_code
    await message.reply(text="❌ " + _("It doesn't look like a YouTube link", locale=user_lang_code))


async def if_user_sent_text(message: Message, state: FSMContext) -> None:
    """Handles the message if a user sent text"""
    await UserInput.Block.set()  # Block user actions while the search is in progress.

    user_lang_code: str = message.from_user.language_code
    chat_id: int = message.from_user.id

    # If there are previous search results in the chat, delete them
    async with state.proxy() as data:
        if data.get("bot_answers_ids"):
            await message.bot.delete_message(chat_id=chat_id, message_id=data["user_message_id"])
            await message.bot.delete_message(chat_id=chat_id, message_id=data["bot_reply_id"])
            for bot_answer_id in data["bot_answers_ids"]:
                await message.bot.delete_message(chat_id=chat_id, message_id=bot_answer_id)
    await state.reset_data()

    # Starting a new search
    bot_reply: Message = await message.reply(text="🔍 " + _("Looking, wait a bit...", locale=user_lang_code))
    bot_reply_id: int = bot_reply.message_id
    search_results: list[VideoCard] = await get_running_loop().run_in_executor(
        None, search_videos, *(message.text, user_lang_code)
    )

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
        if_user_sent_youtube_link, Text(startswith="https://"), regexp=r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", state=None
    )
    dp.register_message_handler(if_user_sent_link_not_to_youtube, Text(startswith="https://"), state=None)
    dp.register_message_handler(if_user_sent_text, content_types="text", state=None)
    dp.register_message_handler(if_user_input_block, content_types="text", state=UserInput.Block)
    dp.register_message_handler(if_user_sent_anything_but_text, content_types=types.ContentTypes.ANY, state="*")
