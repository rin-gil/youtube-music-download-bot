from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message


async def commands(message: Message) -> None:
    """
    Handles commands from the user /start and /help.

    :param message: Message from the user
    :return: None
    """
    await message.delete()
    if message.text == '/start':
        await message.answer(text='Напиши мне <b>название песни</b> или сбрось ссылку на видеоролик с '
                                  '<a href="https://www.youtube.com">YouTube</a>. 😉')
    elif message.text == '/help':
        await message.answer(text='Я умею скачивать песни с <a href="https://www.youtube.com">YouTube</a>!\n\n'
                                  'Напиши мне <b>название песни</b>, или сбрось <b>ссылку</b> на видеоролик.')


async def unknown_commands(message: Message) -> None:
    """
    Handles unknown commands.

    :param message: Message from the user
    :return: None
    """
    await message.answer(text='❌ Неизвестная команда!\n\n'
                              'Напиши мне <b>название песни</b> или сбрось ссылку на видеоролик с '
                              '<a href="https://www.youtube.com">YouTube</a>. 😉')


def register_commands(dp: Dispatcher) -> None:
    """
    Registers the handling of commands from the user in the Dispatcher.

    :param dp: Dispatcher
    :return: None
    """
    dp.register_message_handler(commands, commands=['start', 'help'])
    dp.register_message_handler(unknown_commands, Text(startswith='/'))
