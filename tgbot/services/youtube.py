"""Set of functions for working with YouTube"""

from asyncio import get_running_loop

from pytube import YouTube

from tgbot.config import MAX_VIDEO_DURATION
from tgbot.middlewares.localization import i18n
from tgbot.services.formatter import format_search_data, VideoCard
from tgbot.services.misc import convert_mp4_to_mp3, download_audio_stream, get_raw_search_results

_ = i18n.gettext  # Alias for gettext method


def search_videos(query: str, lang_code: str) -> list[VideoCard]:
    """Search YouTube for videos requested by the user"""
    search_results: list[VideoCard] = []
    raw_results: list[YouTube] = get_raw_search_results(query=query)
    for raw_result_item in raw_results:
        if 0 < raw_result_item.length <= MAX_VIDEO_DURATION:  # Remove streams and long videos from search results
            result_item: VideoCard = format_search_data(raw_result_item=raw_result_item, lang_code=lang_code)
            search_results.append(result_item)
        if len(search_results) == 3:
            break
    return search_results


async def get_path_to_audio_file(url: str) -> str:
    """Returns the path to the downloaded audio file"""
    path_to_mp4_file: str = await get_running_loop().run_in_executor(None, download_audio_stream, url)
    path_to_mp3_file: str = await get_running_loop().run_in_executor(None, convert_mp4_to_mp3, path_to_mp4_file)
    return path_to_mp3_file
