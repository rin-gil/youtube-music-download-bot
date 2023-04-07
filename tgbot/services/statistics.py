"""Functions for graphing downloads in the bot and saving the graph image"""

from asyncio import get_running_loop
from os import makedirs, path
from typing import NamedTuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.container import BarContainer
from matplotlib.figure import Figure
from numpy import ndarray

from tgbot.config import TEMP_DIR
from tgbot.middlewares.localization import i18n
from tgbot.misc.logger import logger
from tgbot.services.formatter import format_date

_ = i18n.gettext  # Alias for gettext method


class BotStatisticsData(NamedTuple):
    """Represents a counter of downloads by months"""

    date: list[str]
    downloads_counter: list[int]
    searches_counter: list[int]


def plot_download_graph(downloads_data: BotStatisticsData, locale: str) -> str | None:
    """Builds an image of the download graph and saves it to a file"""
    try:
        figure: Figure = plt.figure(figsize=(12, 9))
        axes: Axes = figure.add_subplot()

        # Let's get the data for the graph
        dates: list[str] = [format_date(date=date, locale=locale) for date in downloads_data.date]
        counters: dict[str, list[int]] = {
            _("Downloads", locale=locale): downloads_data.downloads_counter,
            _("Searches", locale=locale): downloads_data.searches_counter,
        }

        # Making a chart
        range_of_dates: ndarray = np.arange(len(dates))  # Number of values on the abscissa axis
        width: float = 0.4  # The width of the bars
        multiplier: float = 0.5  # Offset of bars relative to the center of the container

        for key, value in counters.items():
            offset: float = width * multiplier
            rects: BarContainer = axes.bar(x=range_of_dates + offset, height=value, width=width, label=key)
            axes.bar_label(rects, padding=3)
            multiplier += 1

        axes.invert_xaxis()

        # Add explanatory labels
        axes.set_title(label=_("Chart of bot usage by date", locale=locale))
        axes.set_yticks([])  # Remove labels on the ordinate axis
        axes.set_xticks(range_of_dates + width, dates)  # Add the labels on the abscissa axis
        axes.legend(loc="upper left", ncols=2)  # Legend for charts

        # Save the chart to a file
        path_to_statistics_graph: str = path.join(TEMP_DIR, "stats.png")
        figure.savefig(path.join(TEMP_DIR, "stats.png"))

        return path_to_statistics_graph

    except Exception as ex:
        logger.info("Error in plotting the graph: %s", ex)

    return None


async def get_path_to_statistics_graph(downloads_data: BotStatisticsData, locale: str) -> str | None:
    """Returns the path to the graph image"""
    if not path.exists(TEMP_DIR):
        makedirs(TEMP_DIR)
    path_to_graph_image: str | None = await get_running_loop().run_in_executor(
        None, plot_download_graph, downloads_data, locale
    )
    return path_to_graph_image
