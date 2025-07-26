FROM python:3.13-slim

WORKDIR /app/

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=2.0.0
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY . .


CMD ["python", "video_api/manage.py", "runserver", "0.0.0.0:8000"]
