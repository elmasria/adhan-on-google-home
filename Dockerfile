FROM python:3.9

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY . .

CMD ["gunicorn", "-w", "1", "--capture-output", "-b", "0.0.0.0:5000", "--log-level", "debug", "app.main:app"]
