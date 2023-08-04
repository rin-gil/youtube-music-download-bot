#!/bin/bash

cd ../..

source venv/bin/activate

pybabel compile \
--directory=./src/tgbot/locales \
--statistics

deactivate
