# Dockerfile for auth-service

FROM python:3.9-slim

WORKDIR /app

COPY auth-service/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY auth-service/ ./

CMD ["python", "app.py"]
