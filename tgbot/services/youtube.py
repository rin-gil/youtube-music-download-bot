"""Set of functions for working with YouTube"""

from os import listdir
from os.path import join
from sys import exit as sys_exit
from time import gmtime, strftime
from typing import Any, NamedTuple

from imageio_ffmpeg import get_ffmpeg_exe
from pkg_resources import resource_filename
from yt_dlp import YoutubeDL
from yt_dlp.utils import YoutubeDLError

from tgbot.config import MAX_DURATION, TEMP_DIR
from tgbot.middlewares.localization import i18n
from tgbot.misc.logger import logger
from tgbot.services.decorators import run_in_asyncio_thread

_ = i18n.gettext  # Alias for gettext method


class VideoInfo(NamedTuple):
    """Presents information about the video"""

    description: str
    url: str


class YouTube:
    """Describes methods for working with YouTube videos"""

    def __init__(self) -> None:
        """Loads ffmpeg binaries and adds their parameters"""
        path_to_ffmpeg: str | None = self._get_path_to_ffmpeg()
        if path_to_ffmpeg:
            self._path_to_ffmpeg = path_to_ffmpeg
        else:
            logger.critical("The path to the ffmpeg file was not found, or ffmpeg is not installed")
            sys_exit()

    @staticmethod
    def _get_path_to_ffmpeg() -> str | None:
        """Returns the path to the ffmpeg binary file"""
        try:
            path_to_ffmpeg_exe: str = get_ffmpeg_exe()
            if isinstance(path_to_ffmpeg_exe, str):
                return path_to_ffmpeg_exe
        except RuntimeError:
            ffmpeg_bin_dir: str = resource_filename("imageio_ffmpeg", "binaries")
            ffmpeg_filename: str = [file for file in listdir(ffmpeg_bin_dir) if file.startswith("ffmpeg")][0]
            return join(ffmpeg_bin_dir, ffmpeg_filename)
        return None

    @staticmethod
    def _remove_unwanted_chars(string: str) -> str:
        """Removes everything from the string except letters, numbers, spaces, hyphens, and underscores"""
        processed_string: str = ""
        for char in string[:100]:
            if char.isalnum() or char == "-" or char == "_":
                processed_string += char
            elif char.isspace() and (not processed_string or not processed_string[-1].isspace()):
                processed_string += char
        return processed_string

    @staticmethod
    def _format_search_data(title: str, duration: str, video_url: str, lang_code: str) -> VideoInfo:
        """Formats the raw search data into the desired representation"""
        description: str = (
            f"<b><a href='{video_url}'>{title}</a>\n"
            + _("Duration", locale=lang_code)
            + f": {strftime('%M:%S', gmtime(float(duration)))}</b>"
        )
        return VideoInfo(description=description, url=video_url)

    @run_in_asyncio_thread
    def search_videos(self, query: str, lang_code: str) -> Any:
        """
        Search for videos on YouTube by user request.
        Get the first 10 results, then leave 3 that are no longer than MAX_DURATION.

        Note: Do not use named arguments when calling this method

        Args:
            query (): user search query
            lang_code (): Telegram user language

        Returns:
            A list of three found videos as VideoInfo objects, or None if nothing was found
        """
        options: dict = {
            "format": "m4a/bestaudio/best",
            "geo_bypass": True,
            "noplaylist": True,
            "quiet": True,
        }
        ydl: YoutubeDL = YoutubeDL(params=options)

        try:
            found_videos: list[VideoInfo] = []
            search_results: dict = ydl.extract_info(
                f"ytsearch{10}:{self._remove_unwanted_chars(string=query)}", download=False
            )
            count: int = 0
            for video in search_results["entries"]:
                if count == 3:
                    break
                duration: int | None = video.get("duration")
                if duration and duration <= MAX_DURATION:
                    count += 1
                    found_videos.append(
                        self._format_search_data(
                            title=video["title"],
                            duration=video["duration"],
                            video_url=video["webpage_url"],
                            lang_code=lang_code,
                        )
                    )
            return found_videos if found_videos else None

        except YoutubeDLError as ex:
            logger.error("Error when searching for a video: %s", repr(ex))

        return None

    @run_in_asyncio_thread
    def download_audio(self, youtube_watch_url: str) -> Any:
        """
        Downloads an audio stream from a YouTube link and converts it to mp3 format

        Note: Do not use named arguments when calling this method

        Args:
            youtube_watch_url (): link to YouTube video

        Returns:
            The path to the uploaded audio file,
            or None if the original audio file was longer than MAX_DURATION or is a live broadcast
        """
        options: dict = {
            "format": "m4a/bestaudio/best",
            "ffmpeg_location": self._path_to_ffmpeg,
            "geo_bypass": True,
            "noplaylist": True,
            "noprogress": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "160",
                }
            ],
            "quiet": True,
        }
        ydl: YoutubeDL = YoutubeDL(params=options)

        try:
            # Getting information about the video
            video_info = ydl.extract_info(youtube_watch_url, download=False)
            duration: int | None = video_info.get("duration")

            if duration and duration <= MAX_DURATION:
                # Set save folder and file name
                title: str = video_info.get("title")
                path_to_file: str = join(TEMP_DIR, f"{self._remove_unwanted_chars(string=title)}")
                ydl.params.update({"outtmpl": {"default": path_to_file}})

                # Load an audio stream and convert it to mp3
                ydl.download(youtube_watch_url)

                return f"{path_to_file}.mp3"

        except YoutubeDLError as ex:
            logger.error("Error when loading video: %s", repr(ex))

        return None


youtube = YouTube()
