FROM ubuntu:20.04
ENV PYTHONBUFFERED=1

# Heroku set the PORT dynamically at runtime
EXPOSE 8000
ENV PORT=8000 \
    DJANGO_SETTINGS_MODULE=currency_bot.settings.container

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends --no-install-suggests -y \
    nginx python3-pip
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
