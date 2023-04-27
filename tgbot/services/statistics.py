"""Functions for graphing downloads in the bot and saving the graph image"""

from os import makedirs
from os.path import exists, join
from typing import Any, NamedTuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.container import BarContainer
from matplotlib.figure import Figure
from numpy import ndarray

from tgbot.config import STATS_BG_IMAGE, TEMP_DIR
from tgbot.middlewares.localization import i18n
from tgbot.services.decorators import run_in_asyncio_thread

_ = i18n.gettext  # Alias for gettext method


class BotStatisticsData(NamedTuple):
    """Presents a counter of downloads and searches by months"""

    date: list[str]
    downloads_counter: list[int]
    searches_counter: list[int]


class PlottingBotStatistics:
    """Plots searches and downloads made by the bot on YouTube"""

    def __init__(self) -> None:
        """Creates a folder in which the image of the constructed graph will be saved"""
        if not exists(TEMP_DIR):
            makedirs(TEMP_DIR)

    @staticmethod
    def _format_date(date: str, locale: str) -> str:
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

    @run_in_asyncio_thread
    def get_path_to_statistics_graph(self, bot_statistics_data: BotStatisticsData, locale: str) -> Any:
        """
        Plots an image of the bot's statistics graph and saves it to a file

        Note: Do not use named arguments when calling this method

        Args:
            bot_statistics_data (): Data on bot usage statistics
            locale (): Telegram user language

        Returns:
            Path to the saved image file with the graph or None
        """

        figure: Figure = plt.figure(figsize=(12, 8))
        axes: Axes = figure.add_subplot()

        # Let's get the data for the graph
        dates: list[str] = [self._format_date(date=date, locale=locale) for date in bot_statistics_data.date]
        counters: dict[str, list[int]] = {
            _("Downloads", locale=locale): bot_statistics_data.downloads_counter,
            _("Searches", locale=locale): bot_statistics_data.searches_counter,
        }

        # Making a chart
        range_of_dates: ndarray = np.arange(len(dates))  # Number of values on the abscissa axis
        width: float = 0.4  # The width of the bars
        multiplier: float = 0.5  # Offset of bars relative to the center of the container

        for key, value in counters.items():
            offset: float = width * multiplier
            rects: BarContainer = axes.bar(x=range_of_dates + offset, height=value, width=width, label=key)
            axes.bar_label(container=rects, padding=3)
            multiplier += 1

        axes.invert_xaxis()

        # Add explanatory labels
        axes.set_title(label=_("Chart of bot usage by date", locale=locale))
        axes.set_yticks([])  # Remove labels on the ordinate axis
        axes.set_xticks(range_of_dates + width, dates)  # Add the labels on the abscissa axis
        axes.legend(loc="upper left", ncols=2)  # Legend for charts

        # Add background image on chart
        bg_image: ndarray = plt.imread(fname=STATS_BG_IMAGE, format="png")
        x_min, x_max = axes.get_xlim()
        y_min, y_max = axes.get_ylim()
        axes.imshow(bg_image, extent=(x_min, x_max, y_min, y_max), aspect="auto", alpha=0.9)

        # Save the chart to a file
        path_to_statistics_graph: str = join(TEMP_DIR, "stats.png")
        figure.savefig(fname=path_to_statistics_graph)

        return path_to_statistics_graph


bot_statistics: PlottingBotStatistics = PlottingBotStatistics()
