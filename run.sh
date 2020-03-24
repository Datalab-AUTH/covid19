#!/bin/sh

(
while true; do
	python get_data.py
	sleep 7200 # 2 hours
done
) &
python flask_app.py

