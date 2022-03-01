#!/bin/bash

#CREATE VIRTUAL FRAME BUFFER (XSERVER ON DISPLAY 99)
nohup /usr/bin/Xvfb :99 -ac -screen 0 1024x768x8 > /tmp/nohup.out 2>&1 &

#SET DEFAULT DISPLAY (REQUIRED IF RUN FROM CRONTAB)
export DISPLAY=:99

cd /data/selenium/ 
/data/selenium/venv3.10/bin/python3 /data/selenium/main.py

echo 'SCRIPT COMPLETE'

chmod a+r /mnt/webdev/*.log


