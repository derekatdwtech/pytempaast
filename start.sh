#!/bin/sh
sudo pip install -r /opt/meatmonitor/requirements.txt
if [ ! -d /var/log/meatmonitor ]; then
	sudo mkdir -p /var/log/meatmonitor
	if [ ! -f /var/log/meatmonitor/out.log ]; then
		sudo touch /var/log/meatmonitor/out.log
	fi
fi
sudo python /opt/meatmonitor/main.py 
