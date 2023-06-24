FROM python:3.9

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r ./requirements.txt

COPY . .

# CMD ["gunicorn", "-w", "1", "--capture-output", "-b", "0.0.0.0:5000", "--log-level", "debug", "app.main:app"]
CMD ["python", "-m", "app.main"]
