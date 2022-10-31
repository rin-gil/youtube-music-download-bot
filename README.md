<p align="center">
    <img src="https://repository-images.githubusercontent.com/558609537/280063f1-bec4-49aa-bf56-054cdb00f8d3" alt="YouTube Music Download Bot" width="640">
</p>

<p align="center">
    <a href="https://www.python.org/downloads/release/python-3110/"><img src="https://img.shields.io/badge/python-v3.11-informational" alt="python version"></a>
    <a href="https://pypi.org/project/aiogram/2.22.2/"><img src="https://img.shields.io/badge/aiogram-v2.22.2-informational" alt="aiogram version"></a>
    <a href="https://pypi.org/project/environs/9.5.0/"><img src="https://img.shields.io/badge/environs-v9.5.0-informational" alt="environs version"></a>
    <a href="https://pypi.org/project/moviepy/1.0.3/"><img src="https://img.shields.io/badge/moviepy-v1.0.3-informational" alt="moviepy version"></a>
    <a href="https://pypi.org/project/pytube/12.1.0/"><img src="https://img.shields.io/badge/pytube-v12.1.0-informational" alt="pytube version"></a>
    <a href="https://github.com/rin-gil/YoutubeMusicDownloadBot/blob/master/LICENCE"><img src="https://img.shields.io/badge/licence-MIT-success" alt="MIT licence"></a>
</p>

<p align="right">
    <a href="https://github.com/rin-gil/YoutubeMusicDownloadBot/blob/master/README.ru.md">Читать на русском</a>
</p>

## YouTube Music Download Bot

Bot to download music from YouTube. Working version is available here [https://t.me/YT_upl_Bot](https://t.me/YT_upl_Bot)

### Features

* Search for music on YouTube
* Downloading found videos in .mp3 format

### Installing

```
git clone https://github.com/rin-gil/YoutubeMusicDownloadBot.git
cd YoutubeMusicDownloadBot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
mv .env.dist .env
```

### Setup and launch

* Register a new bot with [BotFather](https://t.me/BotFather) and copy the obtained token
* Insert the bot token into the .env file
* If you want to download videos longer than 15 minutes, change the **MAX_VIDEO_DURATION** constant in [tgbot/config.py](https://github.com/rin-gil/YoutubeMusicDownloadBot/blob/master/tgbot/config.py), the default is 900 seconds (15 minutes)
* Due to limitations of the Telegram API **MAX_VIDEO_DURATION** should not be set higher than 1800 sec. - bot will not be able to send files to the user
* Running the bot through the bot.py file `python bot.py`

### Restrictions
* Bot only downloads music (audio file .mp3)
* Bot does not download live broadcasts
* The entire playlist is not downloaded, only one item is downloaded
* Bot does not download clips longer than 15 minutes
* The title for the audio file is generated from the YouTube video title. Since the title may contain undesirable characters not supported by the file system, all characters except letters, numbers, spaces, '_' and '-' characters are removed from the title, the title length is truncated to 100 characters

### Developers

* [Ringil](https://github.com/rin-gil)

### License

YouTubeMusicDownloadBot is licensed under [MIT](https://github.com/rin-gil/YoutubeMusicDownloadBot/blob/master/LICENCE)