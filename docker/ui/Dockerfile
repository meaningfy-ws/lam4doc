FROM python:3.8.5-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /usr/src/app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD gunicorn --timeout ${LAM_GUNICORN_TIMEOUT} -w ${LAM_GUNICORN_UI_WORKERS} --bind 0.0.0.0:${LAM_UI_PORT} --reload --log-level=debug lam4doc.entrypoints.ui.run:app