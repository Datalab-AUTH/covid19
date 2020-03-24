FROM python:3
COPY . /
RUN pip install -r requirements.txt && \
		rm -rf /root/.cache && \
		apt-get update && \
		apt-get install -y nginx && \
		apt-get clean && \
		chown -R www-data:www-data static && \
		mv /nginx.conf /etc/nginx/nginx.conf && \
		sed -i "s|const host = .*|const host = 'http://covid19.vlahavas.com'|" /static/js/bind-variables.js && \
		sed -i "s|const host = .*|const host = 'http://covid19.vlahavas.com'|" /static/js/morris/morris-plain.js
CMD [ "./run.sh" ]

