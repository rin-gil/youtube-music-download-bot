from os import remove

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InputFile

from tgbot.misc import Actions
from tgbot.services import download


async def callbacks(call: CallbackQuery, state: FSMContext) -> None:
    """
    Handles keystrokes in inline keyboards.

    :param state: State from FSM
    :param call: CallbackQuery
    :return: None
    """
    await call.answer(cache_time=1)
    await Actions.Lock.set()  # Block user actions while the download is in progress.
    chat_id: int = call.message.chat.id
    await call.bot.send_message(chat_id=chat_id, text='⏬ Качаю..')
    audio_file: str = download(url=call.data)
    if audio_file[-3:] == 'mp3':
        await call.bot.send_audio(chat_id=chat_id, audio=InputFile(path_or_bytesio=audio_file))
        remove(audio_file)
    else:
        await call.bot.send_message(chat_id=call.message.chat.id,
                                    text='❌ Ошибка при отправке файла!\n\n'
                                         'Попробуй скачать что-то другое. 🙁')
    await state.reset_state()  # Download completed, unblock user actions.


async def lock_callbacks(call: CallbackQuery) -> None:
    """
    The stub function, does not perform any action while the user's actions are blocked.

    :param call: CallbackQuery
    :return: None
    """
    await call.answer(cache_time=1)


def register_callbacks(dp: Dispatcher) -> None:
    """
    Registers the processing of inline keyboard key presses in the dispatcher

    :param dp: Dispatcher
    :return: None
    """
    dp.register_callback_query_handler(callbacks, state=None)
    dp.register_callback_query_handler(lock_callbacks, state=Actions.Lock)
