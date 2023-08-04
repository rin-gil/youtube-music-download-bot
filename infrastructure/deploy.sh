#!/bin/bash

mkdir youtube-music-download-bot
cd youtube-music-download-bot
git init
git config core.sparseCheckout true
git remote add origin https://github.com/rin-gil/youtube-music-download-bot
echo "src" > .git/info/sparse-checkout
git fetch --depth 1 origin master
git checkout master
rm -r -f .git
mv src/* .
mv src/.env.example .env
rm src -r -f
rm requirements-dev.txt -r -f
cd ..
rm deploy.sh -f
