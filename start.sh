#!/bin/bash
. venv/bin/activate
source .config
nohup ./bot.py >> bot.log &
