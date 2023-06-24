FROM python:3.9

WORKDIR /app

COPY pyproject.toml ./

RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH=/root/.local/bin:$PATH
ENV PATH=$HOME/.poetry/bin:$PATH
RUN cd ~ && pwd && echo "${PATH}" && ls -lai /root/.local/bin
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY . .

# CMD ["gunicorn", "-w", "1", "--capture-output", "-b", "0.0.0.0:5000", "--log-level", "debug", "app.main:app"]
CMD ["python", "-m", "app.main"]
