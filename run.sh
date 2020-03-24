#!/bin/sh

python get_data.py
(
while true; do
	sleep 7200 # 2 hours
	python get_data.py
done
) &
service nginx start
uwsgi --ini uwsgi.ini

