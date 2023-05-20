FROM python:3.11-slim-buster AS base

ARG BUILD_TYPE=dev

ENV BUILD_TYPE=${BUILD_TYPE} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.13


RUN groupadd -r app \
    && useradd --no-log-init -M -r -g app app
RUN mkdir -p /app/server
RUN chown -R app:app /app

WORKDIR /app

FROM base AS build

# For build stage
ADD --chown=app:app poetry.lock pyproject.toml /app/

RUN python -m venv /venv

RUN . /venv/bin/activate && \
    chown -R app:app /venv && \
    python -m pip install "poetry==$POETRY_VERSION" && \
    poetry config virtualenvs.create false &&  \
    poetry install --no-interaction --no-ansi \
    $(test "$BUILD_TYPE" = production && echo "--no-dev")


FROM base AS main

USER app:app

COPY --from=build /venv /venv
COPY --from=build /app /app

WORKDIR /app

# Python code
COPY --chown=app:app main.py /app/
RUN mkdir -p /app/server
COPY --chown=app:app server /app/server/

# Docker entrypoint
COPY --chown=app:app docker/docker-entrypoint.sh /app/
RUN chmod u+x docker-entrypoint.sh

# Just env file
ADD --chown=app:app .env /app

EXPOSE 8888

ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["gunicorn", "main:app", "--workers", "4", "--bind", "0.0.0.0:8888", "--forwarded-allow-ips='*'", "--worker-class", "uvicorn.workers.UvicornWorker"]

FROM main AS migrations

COPY --from=main /venv /venv
COPY --from=main /app /app

COPY --chown=app:app alembic.ini /app/
COPY --chown=app:app migrations /app/migrations/

CMD ["alembic", "upgrade", "head"]