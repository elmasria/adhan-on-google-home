FROM python:3.9

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY . .

CMD ["python", "app/main.py"]
