FROM python:3.12.8

RUN pip install poetry
RUN poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml ./
RUN poetry install

COPY . /app
WORKDIR /app/src

CMD gunicorn --bind :8000 --timeout 120 --workers 10 --threads=3 --worker-connections=1000 wsgi
