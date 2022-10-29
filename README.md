<p style="text-align:center">
    <img src="https://repository-images.githubusercontent.com/558609537/280063f1-bec4-49aa-bf56-054cdb00f8d3" alt="YouTube Music Download Bot" width="640">
</p>

<p style="text-align:center">
    <a href="https://pypi.org/project/aiogram/2.22.2/"><img src="https://img.shields.io/badge/python-v3.7-blue" alt="python version"></a>
    <a href="https://pypi.org/project/aiogram/2.22.2/"><img src="https://img.shields.io/badge/aiogram-v2.22.2-informational" alt="aiogram version"></a>
    <a href="https://pypi.org/project/environs/9.5.0/"><img src="https://img.shields.io/badge/environs-v9.5.0-informational" alt="environs version"></a>
    <a href="https://pypi.org/project/moviepy/1.0.3/"><img src="https://img.shields.io/badge/moviepy-v1.0.3-informational" alt="moviepy version"></a>
    <a href="https://pypi.org/project/pytube/12.1.0/"><img src="https://img.shields.io/badge/pytube-v12.1.0-informational" alt="pytube version"></a>
    <a href="https://github.com/rin-gil/YoutubeMusicDownloadBot/blob/master/LICENCE"><img src="https://img.shields.io/badge/licence-MIT-success" alt="MIT licence"></a>
</p>

## YouTube Music Download Bot

Бот для загрузки музыки с YouTube. Рабочая версия доступна по ссылке [https://t.me/YT_upl_Bot](https://t.me/YT_upl_Bot)

### Возможности

* Поиск музыки на YouTube
* Скачивание найденных видео в формате .mp3

### Установка

```
git clone https://github.com/rin-gil/YoutubeMusicDownloadBot.git
cd YoutubeMusicDownloadBot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
mv .env.dist .env
```

### Настройка и запуск

* Зарегистрируйте нового бота у [BotFather](https://t.me/BotFather) и скопируйте полученный токен
* Вставьте токен бота в файл .env
* Если хотите скачивать видео длиной более 15 минут, измените константу **MAX_VIDEO_DURATION** в файле [tgbot/config.py](https://github.com/rin-gil/YoutubeMusicDownloadBot/blob/master/tgbot/config.py), по умолчанию 900 сек. (15 минут)
* Из-за ограничений API Telegram **MAX_VIDEO_DURATION** не нужно устанавливать более 1800 сек. - бот не сможет отправлять файлы пользователю

### Ограничения
* Бот скачивает только музыку (аудиофайл .mp3)
* Бот не скачивает живые трансляции
* Плейлист не скачивается полностью, скачивается только один элемент
* Бот не скачивает клипы продолжительностью больше 15 минут
* Название для аудиофайла формируется из названия видео на YouTube. Поскольку в названии могут содержаться нежелательные символы, не поддерживаемые файловой системой, из названия убираются все символы, кроме букв, цифр, пробелов, знаков '_' и '-', длина названия обрезается до 100 символов
