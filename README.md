<p align="center">
    <img src="https://repository-images.githubusercontent.com/558609537/96515af2-a015-4470-a760-448352f38a98" alt="YouTube Music Download Bot" width="640">
</p>

<p align="center">
    <a href="https://www.python.org/downloads/release/python-3110/">
        <img src="https://img.shields.io/badge/python-v3.11-informational" alt="python version">
    </a>
    <a href="https://pypi.org/project/aiogram/2.25.1/">
        <img src="https://img.shields.io/badge/aiogram-v2.25.1-informational" alt="aiogram version">
    </a>
    <a href="https://pypi.org/project/asyncpg/0.28.0/">
        <img src="https://img.shields.io/badge/asyncpg-v0.28.0-informational" alt="asyncpg version">
    </a>
    <a href="https://pypi.org/project/environs/9.5.0/">
        <img src="https://img.shields.io/badge/environs-v9.5.0-informational" alt="environs version">
    <a href="https://pypi.org/project/imageio-ffmpeg/0.4.8/">
        <img src="https://img.shields.io/badge/imageio_ffmpeg-v0.4.8-informational" alt="static-ffmpeg version">
    </a>
    </a>
    <a href="https://pypi.org/project/matplotlib/3.7.2/">
        <img src="https://img.shields.io/badge/matplotlib-v3.7.2-informational" alt="matplotlib version">
    </a>
    <a href="https://pypi.org/project/numpy/1.25.2/">
        <img src="https://img.shields.io/badge/numpy-v1.25.2-informational" alt="numpy version">
    </a>
    <a href="https://pypi.org/project/redis/4.6.0/">
        <img src="https://img.shields.io/badge/redis-v4.6.0-informational" alt="redis version">
    </a>
    <a href="https://pypi.org/project/yt-dlp/22023.7.6/">
        <img src="https://img.shields.io/badge/yt_dlp-v2023.7.6-informational" alt="yt-dlp version">
    </a>
</p>

<p align="center">
    <a href="https://github.com/psf/black">
        <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-black.svg">
    </a>
    <a href="https://github.com/rin-gil/youtube-music-download-bot/actions/workflows/tests.yml">
        <img src="https://github.com/rin-gil/youtube-music-download-bot/actions/workflows/tests.yml/badge.svg" alt="Code tests">
    </a>
    <a href="https://github.com/rin-gil/youtube-music-download-bot/actions/workflows/codeql.yml">
        <img src="https://github.com/rin-gil/youtube-music-download-bot/actions/workflows/codeql.yml/badge.svg" alt="Code tests">
    </a>
    <a href="https://github.com/rin-gil/youtube-music-download-bot/blob/master/LICENCE">
        <img src="https://img.shields.io/badge/licence-MIT-success" alt="MIT licence">
    </a>
</p>

<p align="right">
    <a href="https://github.com/rin-gil/youtube-music-download-bot/blob/master/README.ru.md">
        <img src="https://raw.githubusercontent.com/rin-gil/rin-gil/main/assets/img/icons/flags/russia_24x24.png" alt="Ru">
    </a>
    <a href="https://github.com/rin-gil/youtube-music-download-bot/blob/master/README.ua.md">
        <img src="https://raw.githubusercontent.com/rin-gil/rin-gil/main/assets/img/icons/flags/ukraine_24x24.png" alt="Ua">
    </a>
</p>

## YouTube Music Download Bot

Bot to download music from YouTube. Working version is available here [@YT_upl_Bot](https://t.me/YT_upl_Bot)

### Features

* Search for music on YouTube
* Downloading found videos in .mp3 format

### Installing Bot

If you want a simple version of the bot, without using Postgres database and without working in webhook mode, go to [this branch](https://github.com/rin-gil/youtube-music-download-bot/tree/simple-with-sqlite-no-webhook).

Install the bot with the command in the terminal:

```
wget https://raw.githubusercontent.com/rin-gil/youtube-music-download-bot/master/infrastructure/deploy.sh && chmod +x deploy.sh && ./deploy.sh
```

### Installing and setup Postgres

Install the Postgres database according to the instructions from the official website: https://www.postgresql.org/download/

The work of the bot is tested on Postgres version 15

Create the database, user, and settings by running the commands in the terminal:

```
sudo -u postgres psql
CREATE DATABASE db_name;
CREATE USER db_user WITH PASSWORD 'db_password';
\connect db_name;
CREATE SCHEMA db_name AUTHORIZATION db_user;
ALTER ROLE db_user SET client_encoding TO 'utf8';
ALTER ROLE db_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE db_user SET timezone TO 'UTC';
\q
```

Replace _db_name_, _db_user_ and _db_password_ in these commands with your data.

### Setup and launch

* Register a new bot with [@BotFather](https://t.me/BotFather) and copy the obtained token
* Insert the bot token and database credentials into the .env file
* Running the bot through the bot.py file `python bot.py`

### Additional configuration

Example configurations for running the bot in webhook mode or as a systemd service can be found in the [infrastructure](https://github.com/rin-gil/youtube-music-download-bot/tree/master/infrastructure) folder

### Restrictions

* Bot only downloads music (audio file .mp3)
* Bot does not download live broadcasts
* The entire playlist is not downloaded, only one item is downloaded
* Bot does not download clips longer than 15 minutes
* The title for the audio file is generated from the YouTube video title. Since the title may contain undesirable characters not supported by the file system, all characters except letters, numbers, spaces, '_' and '-' characters are removed from the title, the title length is truncated to 100 characters

### Developers

* [Ringil](https://github.com/rin-gil)

### License

YouTubeMusicDownloadBot is licensed under [MIT](https://github.com/rin-gil/youtube-music-download-bot/blob/master/LICENCE.md)
