#!/bin/bash

scriptdir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/"

touch /etc/crontab
/etc/init.d/cron restart

rm /tmp/olaf.pid
python3 ${scriptdir}app.py
