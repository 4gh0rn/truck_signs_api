FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    libffi-dev \
    gcc \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY entrypoint.sh .

RUN pip install -r requirements.txt

COPY . .

RUN mkdir -p /app/media /app/static

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]