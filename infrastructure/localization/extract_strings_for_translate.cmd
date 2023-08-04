@echo off

cd ../..

call venv\Scripts\activate

pybabel extract ^
--input-dirs=./src/tgbot ^
--output-file=./src/tgbot/locales/messages.pot ^
--width=120 ^
--sort-by-file ^
--msgid-bugs-address=e.ringil@proton.me ^
--copyright-holder=Ringil ^
--project=YoutubeMusicDownloadBot ^
--version=1.0.0

venv\Scripts\deactivate
