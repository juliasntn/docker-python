FROM python:3.9-slim

WORKDIR /app

RUN pip install --upgrade pip

RUN pip install influxdb_client schedule

COPY script.py .

CMD ["python", "script.py"]