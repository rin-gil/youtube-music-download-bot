@echo off

cd ../..

call venv\Scripts\activate

pybabel compile ^
--directory=./src/tgbot/locales ^
--statistics

venv\Scripts\deactivate
