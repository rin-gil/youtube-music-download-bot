@echo off

cd ../..

call venv\Scripts\activate

pybabel init ^
--input-file=./src/tgbot/locales/messages.pot ^
--output-dir=./src/tgbot/locales ^
--width=120 ^
--locale=en

pybabel init ^
--input-file=./src/tgbot/locales/messages.pot ^
--output-dir=./src/tgbot/locales ^
--width=120 ^
--locale=ru

pybabel init ^
--input-file=./src/tgbot/locales/messages.pot ^
--output-dir=./src/tgbot/locales ^
--width=120 ^
--locale=uk

venv\Scripts\deactivate
