#!/bin/bash

cd ../..

source venv/bin/activate

pybabel update \
--input-file=./src/tgbot/locales/messages.pot \
--output-dir=./src/tgbot/locales \
--width=120 \
--init-missing \
--update-header-comment \
--locale=en

pybabel update \
--input-file=./src/tgbot/locales/messages.pot \
--output-dir=./src/tgbot/locales \
--width=120 \
--init-missing \
--update-header-comment \
--locale=ru

pybabel update \
--input-file=./src/tgbot/locales/messages.pot \
--output-dir=./src/tgbot/locales \
--width=120 \
--init-missing \
--update-header-comment \
--locale=uk

deactivate
