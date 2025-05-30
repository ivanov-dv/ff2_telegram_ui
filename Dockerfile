FROM python:3.12

ARG TYPE_ENV=production

ENV TYPE_ENV=${TYPE_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  POETRY_VERSION=1.8.4

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    poetry self update $POETRY_VERSION

WORKDIR /app
COPY poetry.lock pyproject.toml ./
RUN poetry install $( [ "$TYPE_ENV" = "production" ] && echo "--only=main" ) --no-interaction --no-ansi

COPY src /app/src

CMD poetry run python3 src/main.py
