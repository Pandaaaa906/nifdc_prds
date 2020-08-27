#!/bin/bash
chmod 0644 /etc/cron.d/cronpy
chmod -R 744 /app/run.py


crontab /etc/cron.d/cronpy
printenv | grep -v "no_proxy" >> /etc/environment
touch /var/log/cron.log
cron -f