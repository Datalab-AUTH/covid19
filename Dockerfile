FROM python:3
COPY --chown=www-data:www-data . /app/
WORKDIR /app
RUN pip install -r requirements.txt && \
		pip install -r production-requirements.txt && \
		rm -rf /root/.cache && \
		apt-get update && \
		apt-get install -y nginx && \
		apt-get clean && \
		mv nginx.conf /etc/nginx/nginx.conf
USER www-data:www-data
CMD [ "./run.sh" ]

