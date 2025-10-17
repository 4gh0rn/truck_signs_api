FROM python:3.9-slim

WORKDIR /app

# Install system dependencies for psycopg2, cffi, and nc (netcat)
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

# Copy .env file to the location Django expects
RUN mkdir -p truck_signs_designs/settings && cp .env truck_signs_designs/settings/.env

# Create media and static directories
RUN mkdir -p /app/media /app/static

# Make entrypoint executable
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]