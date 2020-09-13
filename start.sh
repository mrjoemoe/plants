#!/bin/bash
. venv/bin/activate
source .config
mkdir -p $HOME/plant_log_history
cp bot.log "$HOME/plant_log_history/$(date +'%Y-%m-%d-%H-%M').log"
rm -f bot.log

# if any arg passed to start script then run in debug mode
if [ $# -eq 0 ]; then
    nohup python3 bot.py >> bot.log &
else
	python3 bot.py "debug"
fi
