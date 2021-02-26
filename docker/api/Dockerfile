FROM python:3.8.5-buster

RUN apt-get update \
    && apt-get install -y texlive texlive-bibtex-extra texlive-latex-extra texlive-xetex texlive-lang-european lmodern --no-install-recommends \
    && apt --purge remove tex.\*-doc$

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /usr/src/app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD gunicorn --timeout ${LAM_GUNICORN_TIMEOUT} -w ${LAM_GUNICORN_API_WORKERS} --bind 0.0.0.0:${LAM_API_PORT} --reload --log-level=debug lam4doc.entrypoints.api.run:app