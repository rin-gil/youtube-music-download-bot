from os import remove
from time import strftime, gmtime

from moviepy.audio.io.AudioFileClip import AudioFileClip
from pytube import Search, YouTube

from tgbot import MAX_VIDEO_DURATION, DOWNLOAD_FOLDER


def youtube_link(text: str) -> bool:
    """
    Checks if the user's message is a link to YouTube

    :param text: Message from user
    :return: True or False
    """
    if text.startswith('https://www.youtube.com/watch?v=') \
            or text.startswith('https://youtube.com/watch?v=') \
            or text.startswith('https://youtu.be/') \
            or text.startswith('https://www.youtube.com/shorts/'):
        return True
    else:
        return False


def correct_input(name: str) -> str:
    """
    Removes everything from the string except letters, numbers, spaces, hyphens, and underscores.

    :param name: Source string
    :return: Processed string
    """
    source_string: str = name[:100]
    processed_string: str = ''
    for char in source_string:
        if char.isalnum() or char == '-' or char == '_':
            processed_string += char
        elif char.isspace() and (not processed_string or not processed_string[-1].isspace()):
            processed_string += char
    return processed_string


def search_result(search_query: str):
    """
    Search YouTube for videos requested by the user.

    :param search_query: Message from user
    :return: Nested list of the form [text to reply to user, link to video] or False
    """
    try:
        search = Search(correct_input(name=search_query))
        result: list = []
        count: int = 0
        while True:
            length: int = search.results[count].length
            # Remove live streams (0 seconds long) and videos longer than MAX_VIDEO_DURATION from search results
            if 0 < length <= MAX_VIDEO_DURATION:
                link: str = search.results[count].watch_url
                title: str = search.results[count].title
                duration: str = strftime('%M:%S', gmtime(length))
                card: str = f'<a href="{link}"><b>{title}</b></a>\n<b>Время: {duration}</b>'
                result.append([card, link])
            if len(result) == 3:
                break
            count += 1
        return result
    except Exception as ex:
        print(ex)
        return False


def convert_mp4_to_mp3(mp4file: str, mp3file: str) -> None:
    """
    Converts mp4 files to mp3 files. The mp4 file is deleted after conversion.

    :param mp4file: Path to mp4 file
    :param mp3file: Path to mp3 file
    :return: None
    """
    clip = AudioFileClip(filename=mp4file)
    clip.write_audiofile(filename=mp3file, codec="mp3", bitrate="192k", logger=None)
    clip.close()
    remove(mp4file)


def download(url: str) -> str:
    """
    Uploads an audio stream from YouTube in mp4 format and converts it to mp3 format.

    :param url: Link to YouTube video
    :return: The path to the downloaded file or a description of the error.
    """
    try:
        yt = YouTube(url=url)
        if yt.length <= MAX_VIDEO_DURATION:
            audio = yt.streams.get_audio_only()
            mp4_file: str = audio.download(DOWNLOAD_FOLDER, filename=f'{correct_input(yt.title)}.mp4')
            mp3_file: str = f'{mp4_file[:-1]}3'
            convert_mp4_to_mp3(mp4file=mp4_file, mp3file=mp3_file)
            return mp3_file
        else:
            raise ValueError('Video is too long')
    except Exception as ex:
        return str(ex)
