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
    <a href="https://pypi.org/project/aiosqlite/0.18.0/">
        <img src="https://img.shields.io/badge/aiosqlite-v0.18.0-informational" alt="aiosqlite version">
    </a>
    <a href="https://pypi.org/project/environs/9.5.0/">
        <img src="https://img.shields.io/badge/environs-v9.5.0-informational" alt="environs version">
    <a href="https://pypi.org/project/imageio-ffmpeg/0.4.8/">
        <img src="https://img.shields.io/badge/imageio_ffmpeg-v0.4.8-informational" alt="static-ffmpeg version">
    </a>
    </a>
    <a href="https://pypi.org/project/matplotlib/3.7.1/">
        <img src="https://img.shields.io/badge/matplotlib-v3.7.1-informational" alt="matplotlib version">
    </a>
    <a href="https://pypi.org/project/numpy/1.24.2/">
        <img src="https://img.shields.io/badge/numpy-v1.24.2-informational" alt="numpy version">
    </a>
    <a href="https://pypi.org/project/yt-dlp/2023.3.4/">
        <img src="https://img.shields.io/badge/yt_dlp-v2023.3.4-informational" alt="yt-dlp version">
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
    <a href="https://github.com/rin-gil/YoutubeMusicDownloadBot/blob/master/README.md">
        <img src="https://raw.githubusercontent.com/rin-gil/rin-gil/main/assets/img/icons/flags/united-kingdom_24x24.png" alt="En">
    </a>
    <a href="https://github.com/rin-gil/YoutubeMusicDownloadBot/blob/master/README.ru.md">
        <img src="https://raw.githubusercontent.com/rin-gil/rin-gil/main/assets/img/icons/flags/russia_24x24.png" alt="Ru">
    </a>
</p>

## YouTube Music Download Bot

Бот для завантаження музики з YouTube. Робоча версія доступна за посиланням [@YT_upl_Bot](https://t.me/YT_upl_Bot)

### Можливості

* Пошук музики на YouTube
* Скачування знайдених відео у форматі .mp3

### Встановлення

```
git clone https://github.com/rin-gil/YoutubeMusicDownloadBot.git
cd YoutubeMusicDownloadBot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
mv .env.dist .env
```

### Налаштування та запуск

* Зареєструйте нового бота у [@BotFather](https://t.me/BotFather) і скопіюйте отриманий токен
* Вставте токен бота у файл .env
* Запуск бота через файл bot.py `python bot.py`

### Обмеження

* Бот завантажує тільки музику (аудіофайл .mp3)
* Бот не завантажує живі трансляції
* Плейлист не завантажується повністю, завантажується тільки один елемент
* Бот не скачує кліпи тривалістю понад 15 хвилин
* Назва для аудіофайлу формується з назви відео на YouTube. Оскільки в назві можуть міститися небажані символи, що не підтримуються файловою системою, з назви прибираються всі символи, крім букв, цифр, пробілів, знаків '_' і '-', довжина назви обрізається до 100 символів.

### Локалізація

* З версії 1.1.0 у бот додано локалізацію для англійської, української та російської мови
* Для додавання перекладу на свою мову, зробіть наступне:
  1. перейдіть у папку з ботом
  2. активуйте віртуальне оточення:

     `source venv/bin/activate`
  3. створіть файл перекладу на вашу мову, де **{language}** - код мови за стандартом [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)

     `pybabel init --input-file=tgbot/locales/tgbot.pot --output-dir=tgbot/locales --domain=tgbot --locale={language}`
  4. перекладіть рядки у файлі **locales/{language}/LC_MESSAGES/tgbot.po**
  5. скомпілюйте переклад командою:

     `pybabel compile --directory=tgbot/locales --domain=tgbot`
  6. перезапустіть бота
* При змінах рядків для перекладу в коді, вам потрібно буде повністю перестворити і скомпілювати файли 
  перекладу для всіх локалізацій:
  1. витягти рядки для перекладу з коду:

     `pybabel extract --input-dirs=./tgbot --output-file=tgbot/locales/tgbot.pot --sort-by-file --project=YoutubeMusicDownloadBot`
  2. створити файли перекладу для всіх локалізацій:

     `pybabel init --input-file=tgbot/locales/tgbot.pot --output-dir=tgbot/locales --domain=tgbot --locale={language}`
  3. скомпілювати переклади:

     `pybabel compile --directory=tgbot/locales --domain=tgbot`
* Детальніше про це можна прочитати в прикладі з документації [aiogram](https://docs.aiogram.dev/en/latest/examples/i18n_example.html)
  
### Розробники

* [Ringil](https://github.com/rin-gil)

### Ліцензія

Проект YouTubeMusicDownloadBot поширюється за ліцензією [MIT](https://github.com/rin-gil/YoutubeMusicDownloadBot/blob/master/LICENCE)