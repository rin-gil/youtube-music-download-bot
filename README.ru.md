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
    <a href="https://github.com/rin-gil/youtube-music-download-bot/blob/master/README.md">
        <img src="https://raw.githubusercontent.com/rin-gil/rin-gil/main/assets/img/icons/flags/united-kingdom_24x24.png" alt="En">
    </a>
    <a href="https://github.com/rin-gil/youtube-music-download-bot/blob/master/README.ua.md">
        <img src="https://raw.githubusercontent.com/rin-gil/rin-gil/main/assets/img/icons/flags/ukraine_24x24.png" alt="Ua">
    </a>
</p>

## YouTube Music Download Bot

Бот для загрузки музыки с YouTube. Рабочая версия доступна по ссылке [@YT_upl_Bot](https://t.me/YT_upl_Bot)

### Возможности

* Поиск музыки на YouTube
* Скачивание найденных видео в формате .mp3

### Установка бота

Если вам нужна простая версия бота, без использования базы данных Postgres и без работы в режиме webhook, то перейдите в [эту ветку](https://github.com/rin-gil/youtube-music-download-bot/tree/simple-with-sqlite-no-webhook).

Установите бота с помощью команды в терминале:

```
wget https://raw.githubusercontent.com/rin-gil/youtube-music-download-bot/master/infrastructure/deploy.sh && chmod +x deploy.sh && ./deploy.sh
```

### Установка и настройка Postgres

Установите базу данных Postgres в соответствии с инструкциями с официального сайта: https://www.postgresql.org/download/

Работа бота проверена на Postgres версии 15

Создайте базу данных, пользователя и настройки, выполнив команды в терминале:

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

Замените _db_name_, _db_user_ и _db_password_ в этих командах на свои данные.

### Настройка и запуск

* Зарегистрируйте нового бота у [@BotFather](https://t.me/BotFather) и скопируйте полученный токен
* Вставьте токен бота и учетные данные базы данных в файл .env
* Запуск бота через файл bot.py `python bot.py`

### Дополнительная конфигурация

Примеры конфигураций для запуска бота в режиме webhook или в качестве systemd сервиса можно найти в папке [infrastructure](https://github.com/rin-gil/youtube-music-download-bot/tree/master/infrastructure)

### Ограничения

* Бот скачивает только музыку (аудиофайл .mp3)
* Бот не скачивает живые трансляции
* Плейлист не скачивается полностью, скачивается только один элемент
* Бот не скачивает клипы продолжительностью больше 15 минут
* Название для аудиофайла формируется из названия видео на YouTube. Поскольку в названии могут содержаться нежелательные символы, не поддерживаемые файловой системой, из названия убираются все символы, кроме букв, цифр, пробелов, знаков '_' и '-', длина названия обрезается до 100 символов

### Разработчики

* [Ringil](https://github.com/rin-gil)

### Лицензия

Проект YouTubeMusicDownloadBot распространяется по лицензии [MIT](https://github.com/rin-gil/youtube-music-download-bot/blob/master/LICENCE.md)
