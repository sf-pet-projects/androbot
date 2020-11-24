FROM python:3.8-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV POETRY_VIRTUALENVS_CREATE=false

RUN apt-get update -qy && \
    apt-get install -y libpq-dev gcc

RUN pip install poetry==1.*

WORKDIR /code

COPY pyproject.toml poetry.lock /code/

COPY ./androbot  /code/androbot/
COPY ./templates  /code/templates/

RUN poetry install --no-dev --no-interaction --no-ansi

ENTRYPOINT ["python3", "/code/androbot/__init__.py"]
