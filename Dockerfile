# The builder image, used to build the virtual environment
FROM python:3.10-buster as builder

RUN pip install poetry==1.7.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /auth

COPY auth/pyproject.toml auth/poetry.lock ./auth/

RUN touch README.md

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

FROM python:3.10-slim-buster as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/auth/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

WORKDIR /auth

ENTRYPOINT ["pytest"]