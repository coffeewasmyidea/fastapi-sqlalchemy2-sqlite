FROM python:3.11-buster

ARG CURRENT_ENV

ENV CURRENT_ENV=${CURRENT_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.4.2

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY . .

RUN poetry config virtualenvs.create false \
  && poetry install $(test "$CURRENT_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

CMD [ "scripts/start" ]
