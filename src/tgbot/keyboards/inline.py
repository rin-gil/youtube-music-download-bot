"""Creates inline keyboards for dialogs with the bot"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.middlewares.localization import i18n


_ = i18n.gettext  # Alias for gettext method


async def create_download_kb(callback_data: str, lang_code: str) -> InlineKeyboardMarkup:
    """Creates a keyboard with a download button"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⏬ " + _("Download", locale=lang_code), callback_data=callback_data)]
        ]
    )
