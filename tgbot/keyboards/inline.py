from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def print_search_results(search: list, message) -> None:
    """
    Sends a queue of messages from the search results and a “Download” button under each message.

    :param search: Search results
    :param message: Message from the user
    :return: None
    """
    for item in search:
        kb_download = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='⏬ Скачать',
                                                                                  callback_data=item[1])]])
        await message.answer(item[0], disable_web_page_preview=False, reply_markup=kb_download)
