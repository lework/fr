# build stage
FROM node:lts-alpine as frontend_builder

COPY fr_frontend/  /app/

WORKDIR /app

RUN npm install --registry=https://registry.npm.taobao.org \
    && npm run build-prod


FROM python:3.8-buster as backend_builder

WORKDIR /code

COPY fr_backend/requirements.txt /code/

RUN pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple


# production stage
FROM python:3.8-slim-buster as runner

ENV APP_ENV=production

WORKDIR /code

COPY fr_backend/ /code/
COPY entrypoint.sh /entrypoint.sh
COPY --from=frontend_builder /app/dist/ /code/apps/ui/templates/ui/
COPY --from=backend_builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY --from=backend_builder /usr/local/bin/uwsgi /usr/local/bin/uwsgi

RUN apt update \
    && apt install -y libpq5 libxml2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -r -s /bin/false uwsgi \
    && chown -R uwsgi /code \
    && chmod +x /entrypoint.sh

USER uwsgi

EXPOSE 8000


ENTRYPOINT ["/entrypoint.sh"]
