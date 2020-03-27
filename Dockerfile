FROM python:3
COPY . /
RUN pip install -r requirements.txt && \
		pip install -r production-requirements.txt && \
		rm -rf /root/.cache && \
		apt-get update && \
		apt-get install -y nginx && \
		apt-get clean && \
		chown -R www-data:www-data static && \
		mv /nginx.conf /etc/nginx/nginx.conf
CMD [ "./run.sh" ]

