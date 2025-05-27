# syntax=docker/dockerfile:1

FROM python:3.13-slim

# install poetry
ENV POETRY_HOME=/opt/poetry \
    PATH="/opt/poetry/bin:${PATH}"

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && curl -sSL https://install.python-poetry.org | python - --version 2.1.1 \
    && apt-get purge -y curl && rm -rf /var/lib/apt/lists/*

# sign app
WORKDIR /app
# copy dependences
COPY pyproject.toml poetry.lock ./

# disable venv creation, install deps into container Python
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-root --no-ansi --no-interaction

# copy project
COPY . .
EXPOSE 5050
ENV PORT=5050
# run
ENTRYPOINT ["poetry", "run", "python", "src/ai_phone_assistant/main.py"]
