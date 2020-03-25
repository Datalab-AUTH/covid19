#!/bin/bash

DEFAULT_SITE_URL="http://covid19.vlahavas.com"

if [[ -z $SITE_URL ]]; then
	echo "Using default SITE_URL: $DEFAULT_SITE_URL"
	SITE_URL=$DEFAULT_SITE_URL
else
	echo "SITE_URL has been set to: $SITE_URL"
fi
sed -i \
	"s|const host = .*|const host = '$SITE_URL'|" \
	/static/js/bind-variables.js \
	/static/js/morris/morris-plain.js
python get_data.py
(
while true; do
	sleep 7200 # 2 hours
	python get_data.py
done
) &
service nginx start
uwsgi --ini uwsgi.ini

