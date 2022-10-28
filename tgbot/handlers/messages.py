from os import remove

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InputFile

from tgbot import MAX_VIDEO_DURATION, BANNED_CONTENT
from tgbot.keyboards import print_search_results
from tgbot.misc import Actions
from tgbot.services import youtube_link, download, search_result


async def unknown_message(message: Message, state: FSMContext) -> None:
    """
    Handles messages containing BANNED_CONTENT.

    :param state: State from FSM
    :param message: Message from the user
    :return: None
    """
    async with state.proxy() as data:
        if data.state == 'Actions:Lock':
            await message.delete()
        else:
            await message.reply(text='🤷 Я не знаю, что с этим делать.\n\n'
                                     'Напиши мне <b>название песни</b> или сбрось ссылку на видеоролик с '
                                     '<a href="https://www.youtube.com">YouTube</a>')


async def messages(message: Message, state: FSMContext) -> None:
    """
    Handles messages from the user that do not contain BANNED_CONTENT.

    :param state: State from FSM
    :param message: Message from the user
    :return: None
    """
    if youtube_link(text=message.text):
        await message.answer(text='⏬ Качаю..')
        await Actions.Lock.set()  # Block user actions while the download is in progress.
        audio_file: str = download(url=message.text)
        if audio_file[-3:] == 'mp3':
            await message.answer_audio(InputFile(path_or_bytesio=audio_file))
            remove(audio_file)
        elif audio_file[15:21] == 'stream':
            await message.answer(text='❌ Я не могу скачивать живые трансляции!\n\n'
                                      'Попробуй скачать что-то другое. 🙁')
        elif audio_file == 'Video is too long':
            await message.answer(text=f'❌ Упс..\n\n'
                                      f'Это видео длится больше {round(MAX_VIDEO_DURATION / 60)} минут!\n'
                                      f'Найди что-нибудь покороче. 😒')
        else:
            await message.answer(text='❌ Ошибка при отправке файла!\n\n'
                                      'Попробуй скачать что-то другое. 🙁')
        await state.reset_state()  # Download completed, unblock user actions.
    else:
        msg = await message.reply(text='🔍 Ищу..')
        await Actions.Lock.set()  # Block user actions while the search is in progress.
        search = search_result(search_query=message.text)
        if not search:
            await message.bot.edit_message_text(text='❌ Упс..\n\n'
                                                     'Я не могу это найти.\n'
                                                     'Попробуй поискать что-то другое. 😒',
                                                chat_id=msg.chat.id, message_id=msg.message_id)
        else:
            await message.bot.edit_message_text(text='👇 Смотри, что я нашел:',
                                                chat_id=msg.chat.id, message_id=msg.message_id)
            await print_search_results(search, message)
        await state.reset_state()  # Search completed, unblock user actions.


async def lock_messages(message: Message) -> None:
    """
    The stub function, deletes messages from the user while the user's actions are blocked.

    :param message: Message from the user
    :return: None
    """
    await message.delete()


def register_messages(dp: Dispatcher) -> None:
    """
    Registers the handling of messages from the user in the Dispatcher.

    :param dp: Dispatcher
    :return: None
    """
    dp.register_message_handler(unknown_message, content_types=BANNED_CONTENT, state='*')
    dp.register_message_handler(messages, content_types='text', state=None)
    dp.register_message_handler(lock_messages, content_types='text', state=Actions.Lock)
