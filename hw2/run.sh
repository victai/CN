#!/bin/bash
python3 agent.py > agent.log &
python3 receiver.py $2 > receiver.log &
python3 sender.py $1 > sender.log &

