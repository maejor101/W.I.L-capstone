# Dockerfile for notice-service

FROM python:3.9-slim

WORKDIR /app

COPY notice-service/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY notice-service/ ./

CMD ["python", "app.py"]
