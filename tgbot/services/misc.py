"""Miscellaneous auxiliary functions"""

from json import JSONDecodeError
from os import remove as os_remove
from time import gmtime, strftime
from typing import NamedTuple

from moviepy.audio.io.AudioFileClip import AudioFileClip

from pytube import Search, Stream, YouTube
from pytube.exceptions import LiveStreamError, PytubeError, VideoUnavailable

from tgbot.config import MAX_VIDEO_DURATION, TEMP_DIR
from tgbot.middlewares.localization import i18n
from tgbot.services.formatter import remove_unwanted_chars


_ = i18n.gettext  # Alias for gettext method


class VideoAvailability(NamedTuple):
    """Storing information about the availability of videos on YouTube"""

    available: bool
    description: str


def check_video_available(url: str, lang_code: str) -> VideoAvailability:
    """Checks video available on YouTube"""
    try:
        youtube_video: YouTube = YouTube(url=url)
        youtube_video.check_availability()
        if youtube_video.length > MAX_VIDEO_DURATION:
            return VideoAvailability(
                available=False,
                description=_("Can't download songs longer than", locale=lang_code)
                + f" <b>{strftime('%M:%S', gmtime(MAX_VIDEO_DURATION))}</b> "
                + _("minutes", locale=lang_code),
            )
        if youtube_video.streams.get_audio_only() is None:
            return VideoAvailability(
                available=False, description=_("There is no audio track in the video", locale=lang_code)
            )
        return VideoAvailability(available=True, description="")
    except LiveStreamError:
        return VideoAvailability(
            available=False, description=_("Video is streaming live and cannot be loaded", locale=lang_code)
        )
    except VideoUnavailable:
        return VideoAvailability(
            available=False, description=_("Video is private, restricted access, or unavailable", locale=lang_code)
        )
    except PytubeError:
        return VideoAvailability(available=False, description=_("Can't download this video", locale=lang_code))


def get_raw_search_results(query: str) -> list[YouTube]:
    """Returns raw search results for a user's query"""
    try:
        search: Search = Search(query=remove_unwanted_chars(string=query))
        results: list[YouTube] = search.results
        return results
    except (JSONDecodeError, IndexError):
        return []


def download_audio_stream(url: str) -> str:
    """
    Downloads audio stream from YouTube video

    :param url: link to YouTube video
    :return: path to downloaded mp4 file
    """
    youtube_video: YouTube = YouTube(url=url)
    audio_stream: Stream = youtube_video.streams.get_audio_only()
    path_to_mp4_file: str = audio_stream.download(
        output_path=TEMP_DIR, filename=f"{remove_unwanted_chars(string=youtube_video.title)}.mp4"
    )
    return path_to_mp4_file


def convert_mp4_to_mp3(path_to_mp4_file: str) -> str:
    """
    Converts mp4 files to mp3 files, mp4 file is deleted after conversion

    :param path_to_mp4_file: path to mp4 file
    :return: path to the converted mp3 file
    """
    path_to_mp3_file: str = f"{path_to_mp4_file[:-1]}3"
    clip: AudioFileClip = AudioFileClip(filename=path_to_mp4_file)
    clip.write_audiofile(filename=path_to_mp3_file, codec="mp3", bitrate="128k", logger=None)
    clip.close()
    os_remove(path_to_mp4_file)
    return path_to_mp3_file
