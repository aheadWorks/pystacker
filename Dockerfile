FROM python:3.7-alpine

RUN apk add --update nodejs nodejs-npm docker
RUN docker --version

RUN pip install --upgrade pip click gunicorn
# Workaround, will not build with latest docker-compose (1.24)
RUN pip install --upgrade docker-compose==1.23.2

RUN mkdir -p /app/config

# Copy source & templates
ADD pystacker-backend/pystacker /app/pystacker
ADD pystacker-backend/templates /app/templates
COPY pystacker-backend/setup.py /app

ADD pystacker-backend/config/app.docker.yml /app/config/app.yml

RUN mkdir -p /data/stacks

RUN apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev openssl-dev

# Installing app
RUN pip install -e /app

# Building frontend
ADD pystacker-front /tmp/frontend

RUN cd /tmp/frontend && npm install && npm run build && mv /tmp/frontend/dist /app/frontend  && rm -rf /tmp/frontend
RUN apk del nodejs nodejs-npm build-base python3-dev libffi-dev openssl-dev

VOLUME /data

ENV MIN_ID=10
ENV MAX_ID=99

CMD ["gunicorn", "pystacker:gunicorn_app", "--bind", ":80", "--worker-class", "aiohttp.GunicornWebWorker"]