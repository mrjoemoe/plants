#!/bin/bash
. venv/bin/activate
source .config
mkdir -p $HOME/plant_log_history
cp bot.log "$HOME/plant_log_history/$(date +'%Y-%m-%d-%H-%M').log"
rm -f bot.log
nohup python3 bot.py >> bot.log &
