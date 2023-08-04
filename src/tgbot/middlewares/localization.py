"""Enables localization"""

from aiogram.contrib.middlewares.i18n import I18nMiddleware

from tgbot.config import LOCALES_DIR


i18n: I18nMiddleware = I18nMiddleware(domain="tgbot", path=LOCALES_DIR)
