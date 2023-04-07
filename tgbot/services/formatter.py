"""Functions for data formatting"""

from time import gmtime, strftime
from typing import NamedTuple

from pytube import YouTube

from tgbot.middlewares.localization import i18n


_ = i18n.gettext  # Alias for gettext method


class VideoCard(NamedTuple):
    """Storing information about videos"""

    description: str
    url: str


def remove_unwanted_chars(string: str) -> str:
    """Removes everything from the string except letters, numbers, spaces, hyphens, and underscores"""
    processed_string: str = ""
    for char in string[:100]:
        if char.isalnum() or char == "-" or char == "_":
            processed_string += char
        elif char.isspace() and (not processed_string or not processed_string[-1].isspace()):
            processed_string += char
    return processed_string


def format_search_data(raw_result_item: YouTube, lang_code: str) -> VideoCard:
    """Formats the raw search data into the desired representation"""
    url: str = raw_result_item.watch_url
    title: str = raw_result_item.title
    duration: str = strftime("%M:%S", gmtime(raw_result_item.length))
    description: str = f'<b><a href="{url}">{title}</a>\n' + _("Duration", locale=lang_code) + f": {duration}</b>"
    return VideoCard(description=description, url=url)


def format_date(date: str, locale: str) -> str:
    """Returns the formatted date value in the user's local language"""
    month_in_user_local_language: dict[str, str] = {
        "01": _("Jan", locale=locale),
        "02": _("Feb", locale=locale),
        "03": _("Mar", locale=locale),
        "04": _("Apr", locale=locale),
        "05": _("May", locale=locale),
        "06": _("Jun", locale=locale),
        "07": _("Jul", locale=locale),
        "08": _("Aug", locale=locale),
        "09": _("Sep", locale=locale),
        "10": _("Oct", locale=locale),
        "11": _("Nov", locale=locale),
        "12": _("Dec", locale=locale),
    }
    return f"{month_in_user_local_language.get(date[5:])}\n{date[:4]}"
