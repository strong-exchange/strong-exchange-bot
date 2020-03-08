FROM ubuntu:19.10
ENV PYTHONBUFFERED=1

# Heroku set the PORT dynamically at runtime
EXPOSE 8000
ENV PORT=8000 \
    DJANGO_SETTINGS_MODULE=currency_bot.settings.container

RUN apt-get update && apt-get install -y nginx build-essential python3-dev python3-pip python3-setuptools python3-wheel
WORKDIR /app

# forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY containers/nginx_server.conf /etc/nginx/sites-enabled/default
COPY currency_bot ./currency_bot/

RUN python3 ./currency_bot/manage.py collectstatic

# change the $PORT placeholder to the port from the environment(8000 is default) in Nginx settings and run the server
CMD sed -i -e 's/$PORT/'"$PORT"'/g' /etc/nginx/sites-enabled/default && nginx \
    && gunicorn --bind unix:/tmp/gunicorn.sock --timeout 1800 --workers 5 --chdir currency_bot currency_bot.wsgi:application
