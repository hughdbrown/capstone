#!/bin/sh

# Run this on laptop to copy code and configuration to AWS

cd ~/workspace/hughdbrown/capstone
scp requirements.txt capstone:
scp .tmux.conf capstone:

cd script
scp -r . capstone:script/
