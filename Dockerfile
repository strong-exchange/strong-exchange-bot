FROM python as poetry-requirements-export
WORKDIR /app
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --output requirements.txt


FROM ubuntu:24.04
ENV PYTHONBUFFERED=1 VIRTUAL_ENV=/venv PATH=/venv/bin:$PATH

# Heroku set the PORT dynamically at runtime
EXPOSE 8000
ENV PORT=8000 \
    DJANGO_SETTINGS_MODULE=strong_exchange_bot.settings

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends --no-install-suggests -y \
    nginx python3-venv python3-pip \
    && python3 -m venv ${VIRTUAL_ENV} \
    && rm -rf /var/lib/apt/lists/*

# forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

WORKDIR /app/
COPY --from=poetry-requirements-export /app/requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY containers/nginx_server.conf /etc/nginx/sites-enabled/default
COPY strong_exchange_bot ./

RUN python3 ./manage.py collectstatic

# change the $PORT placeholder to the port from the environment(8000 is default) in Nginx settings and run the server
CMD sed -i -e 's/$PORT/'"$PORT"'/g' /etc/nginx/sites-enabled/default && nginx \
    && gunicorn --bind unix:/tmp/gunicorn.sock --timeout 1800 --workers 5 strong_exchange_bot.wsgi:application
