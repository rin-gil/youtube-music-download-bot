<p align="center">
    <img src="https://repository-images.githubusercontent.com/558609537/280063f1-bec4-49aa-bf56-054cdb00f8d3" alt="YouTube Music Download Bot" width="640">
</p>

<p align="center">
    <a href="https://www.python.org/downloads/release/python-3110/">
        <img src="https://img.shields.io/badge/python-v3.11-informational" alt="python version">
    </a>
    <a href="https://pypi.org/project/aiogram/2.23.1/">
        <img src="https://img.shields.io/badge/aiogram-v2.23.1-informational" alt="aiogram version">
    </a>
    <a href="https://pypi.org/project/environs/9.5.0/">
        <img src="https://img.shields.io/badge/environs-v9.5.0-informational" alt="environs version">
    </a>
    <a href="https://pypi.org/project/moviepy/1.0.3/">
        <img src="https://img.shields.io/badge/moviepy-v1.0.3-informational" alt="moviepy version">
    </a>
    <a href="https://pypi.org/project/pytube/12.1.0/">
        <img src="https://img.shields.io/badge/pytube-v12.1.0-informational" alt="pytube version">
    </a>
    <a href="https://github.com/psf/black">
        <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-black.svg">
    </a>
    <a href="https://github.com/rin-gil/YoutubeMusicDownloadBot/actions/workflows/tests.yml">
        <img src="https://github.com/rin-gil/YoutubeMusicDownloadBot/actions/workflows/tests.yml/badge.svg" alt="Code tests">
    </a>
    <a href="https://github.com/rin-gil/YoutubeMusicDownloadBot/actions/workflows/codeql.yml">
        <img src="https://github.com/rin-gil/YoutubeMusicDownloadBot/actions/workflows/codeql.yml/badge.svg" alt="Code tests">
    </a>
    <a href="https://github.com/rin-gil/YoutubeMusicDownloadBot/blob/master/LICENCE">
        <img src="https://img.shields.io/badge/licence-MIT-success" alt="MIT licence">
    </a>
</p>

<p align="right">
    <a href="https://github.com/rin-gil/YoutubeMusicDownloadBot/blob/master/README.ru.md">
        <img src="https://raw.githubusercontent.com/rin-gil/rin-gil/main/assets/img/icons/flags/russia_24x24.png" alt="Ru">
    </a>
    <a href="https://github.com/rin-gil/YoutubeMusicDownloadBot/blob/master/README.ua.md">
        <img src="https://raw.githubusercontent.com/rin-gil/rin-gil/main/assets/img/icons/flags/ukraine_24x24.png" alt="Ua">
    </a>
</p>

## YouTube Music Download Bot

Bot to download music from YouTube. Working version is available here [@YT_upl_Bot](https://t.me/YT_upl_Bot)

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

* Register a new bot with [@BotFather](https://t.me/BotFather) and copy the obtained token
* Insert the bot token into the .env file
* Running the bot through the bot.py file `python bot.py`

### Restrictions

* Bot only downloads music (audio file .mp3)
* Bot does not download live broadcasts
* The entire playlist is not downloaded, only one item is downloaded
* Bot does not download clips longer than 20 minutes
* The title for the audio file is generated from the YouTube video title. Since the title may contain undesirable characters not supported by the file system, all characters except letters, numbers, spaces, '_' and '-' characters are removed from the title, the title length is truncated to 100 characters

### Localization

* Since version 1.1.0 the bot added localization for English, Ukrainian and Russian
* To add a translation in your language, do the following:
  1. go to the folder with the bot
  2. activate the virtual environment:

     `source venv/bin/activate`
  3. create a translation file for your language, where **{language}** is the [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) language code

     `pybabel init --input-file=tgbot/locales/tgbot.pot --output-dir=tgbot/locales --domain=tgbot --locale={language}`
  4. translate the lines in the file **locales/{language}/LC_MESSAGES/tgbot.po**
  5. compile the translation with the command:

     `pybabel compile --directory=tgbot/locales --domain=tgbot`
  6. restart the bot
* If you change the lines to be translated in the code, you will need to completely recreate and compile the 
  translation files for all localizations:
  1. extract strings to be translated from the code:

     `pybabel extract --input-dirs=./tgbot --output-file=tgbot/locales/tgbot.pot --sort-by-file --project=YoutubeMusicDownloadBot`
  2. create translation files for all localizations:

     `pybabel init --input-file=tgbot/locales/tgbot.pot --output-dir=tgbot/locales --domain=tgbot --locale={language}`
  3. compile translations:

     `pybabel compile --directory=tgbot/locales --domain=tgbot`
* You can read more about this in the example from the documentation of [aiogram](https://docs.aiogram.dev/en/latest/examples/i18n_example.html)

### Developers

* [Ringil](https://github.com/rin-gil)

### License

YouTubeMusicDownloadBot is licensed under [MIT](https://github.com/rin-gil/YoutubeMusicDownloadBot/blob/master/LICENCE)