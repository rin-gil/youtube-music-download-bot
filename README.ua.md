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
    <a href="https://github.com/rin-gil/youtube-music-download-bot/blob/master/README.ru.md">
        <img src="https://raw.githubusercontent.com/rin-gil/rin-gil/main/assets/img/icons/flags/russia_24x24.png" alt="Ru">
    </a>
</p>

## YouTube Music Download Bot

Бот для завантаження музики з YouTube. Робоча версія доступна за посиланням [@YT_upl_Bot](https://t.me/YT_upl_Bot)

### Можливості

* Пошук музики на YouTube
* Скачування знайдених відео у форматі .mp3

### Інсталяція бота

Якщо вам потрібна проста версія бота, без використання бази даних Postgres і без роботи в режимі веб-хука, перейдіть до [цієї гілки](https://github.com/rin-gil/youtube-music-download-bot/tree/simple-with-sqlite-no-webhook).

Встановіть бота за допомогою команди в терміналі:

```
wget https://raw.githubusercontent.com/rin-gil/youtube-music-download-bot/master/infrastructure/deploy.sh && chmod +x deploy.sh && ./deploy.sh
```

### Встановлення та налаштування Postgres

Встановіть базу даних Postgres згідно з інструкцією з офіційного сайту: https://www.postgresql.org/download/

Робота бота протестована на Postgres версії 15

Створіть базу даних, користувача та налаштування, виконавши команди в терміналі:

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

Замініть _db_name_, _db_user_ і _db_password_ у цих командах своїми даними.

### Налаштування та запуск

* Зареєструйте нового бота у [@BotFather](https://t.me/BotFather) і скопіюйте отриманий токен
* Вставте токен бота та облікові дані до бази даних у файл .env
* Запуск бота через файл bot.py `python bot.py`

### Додаткова конфігурація

Приклади конфігурацій для запуску бота в режимі webhook або як systemd-сервіс можна знайти в теці [infrastructure](https://github.com/rin-gil/youtube-music-download-bot/tree/master/infrastructure)

### Обмеження

* Бот завантажує тільки музику (аудіофайл .mp3)
* Бот не завантажує живі трансляції
* Плейлист не завантажується повністю, завантажується тільки один елемент
* Бот не скачує кліпи тривалістю понад 15 хвилин
* Назва для аудіофайлу формується з назви відео на YouTube. Оскільки в назві можуть міститися небажані символи, що не підтримуються файловою системою, з назви прибираються всі символи, крім букв, цифр, пробілів, знаків '_' і '-', довжина назви обрізається до 100 символів.

### Розробники

* [Ringil](https://github.com/rin-gil)

### Ліцензія

Проект YouTubeMusicDownloadBot поширюється за ліцензією [MIT](https://github.com/rin-gil/youtube-music-download-bot/blob/master/LICENCE.md)
