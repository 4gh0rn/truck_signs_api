# Truck Signs API

A Django REST API for managing truck signs and designs with PostgreSQL database and Docker deployment.

## Table of Contents

- [Repository Description](#repository-description)
- [Features](#features)
- [Quickstart](#quickstart)
  - [Prerequisites](#prerequisites)
  - [How to Build the Image](#how-to-build-the-image)
  - [Quick Setup](#quick-setup)
- [Usage](#usage)
  - [Environment Variables](#environment-variables)
  - [Building the Container Image](#building-the-container-image)
  - [Running with Docker](#running-with-docker)
  - [Database Setup](#database-setup)
  - [Network Configuration](#network-configuration)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Testing](#testing)

## Repository Description

This repository contains a Django REST API application for managing truck signs and designs. The main purpose is to provide a containerized backend service that can handle truck sign orders, designs, and related business logic.

**Essential contents:**
- Django REST API application (`truck_signs_designs/`)
- Docker configuration files (Dockerfile, compose.yml)
- Environment configuration files
- Build and deployment scripts
- GitHub Actions CI/CD pipeline

**Purpose:** Production-ready containerized API service for truck sign management system.

## Features

- RESTful API built with Django and Django REST Framework
- PostgreSQL database integration
- Stripe payment processing
- Email functionality
- Docker containerization
- Automated testing and deployment
- Admin interface for content management

## Quickstart

### Prerequisites

- Docker (version 20.0 or higher)
- Docker Compose (version 2.0 or higher)
- Git

### How to Build the Image

Build the Docker image using the provided build script:

```bash
chmod +x build.sh
./build.sh
```

Or manually with Docker:

```bash
docker build -t truck-signs-api .
```

### Quick Setup

1. Clone the repository:
```bash
git clone https://github.com/4gh0rn/truck_signs_api.git
cd truck_signs_api
```

2. Create environment file:
```bash
cp .env.example .env
```
Edit the .env file with your configuration.

3. Build and start the application:
```bash
./build.sh
```

The API will be available at `http://localhost:8020`

## Usage

### Environment Variables

Configure the application using these environment variables:

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DOCKER_SECRET_KEY` | Django secret key | - | Yes |
| `DOCKER_DB_NAME` | Database name | `truck_signs_db` | Yes |
| `DOCKER_DB_USER` | Database username | `postgres` | Yes |
| `DOCKER_DB_PASSWORD` | Database password | - | Yes |
| `DOCKER_DB_HOST` | Database host | `db` | Yes |
| `DOCKER_DB_PORT` | Database port | `5432` | No |
| `SUPERUSER_USERNAME` | Admin username | `admin` | No |
| `SUPERUSER_EMAIL` | Admin email | `admin@example.com` | No |
| `SUPERUSER_PASSWORD` | Admin password | - | Yes |
| `DOCKER_STRIPE_PUBLISHABLE_KEY` | Stripe public key | - | No |
| `DOCKER_STRIPE_SECRET_KEY` | Stripe secret key | - | No |
| `DOCKER_EMAIL_HOST_USER` | SMTP username | - | No |
| `DOCKER_EMAIL_HOST_PASSWORD` | SMTP password | - | No |
| `PRODUCTION_HOST` | Production domain | `localhost` | No |
| `FRONTEND_URL` | Frontend URL | `http://localhost:3000` | No |

### Building the Container Image

The Dockerfile creates a production-ready image based on Python 3.11.

Build the image:
```bash
docker build -t truck-signs-api .
```

Build with build args:
```bash
docker build \
  --build-arg SECRET_KEY=${SECRET_KEY} \
  --build-arg DB_NAME=${DB_NAME} \
  -t truck-signs-api .
```

### Running with Docker

#### Single Container (for testing)

```bash
docker run -d \
  --name truck-signs-api \
  -p 8020:8020 \
  -e DOCKER_SECRET_KEY="your-secret-key-here" \
  -e DOCKER_DB_HOST="your-db-host" \
  -e DOCKER_DB_PASSWORD="your-db-password" \
  -e SUPERUSER_PASSWORD="your-admin-password" \
  truck-signs-api
```

#### With Docker Compose (recommended)

Start all services:
```bash
docker-compose up -d
```

View logs:
```bash
docker-compose logs -f
```

Stop services:
```bash
docker-compose down
```

### Database Setup

The application uses PostgreSQL. When using Docker Compose, the database is automatically configured:

```yaml
# Database service in compose.yml
db:
  image: postgres:15
  environment:
    POSTGRES_DB: ${DOCKER_DB_NAME}
    POSTGRES_USER: ${DOCKER_DB_USER}
    POSTGRES_PASSWORD: ${DOCKER_DB_PASSWORD}
  volumes:
    - postgres_data:/var/lib/postgresql/data
```

### Network Configuration

Containers communicate through a Docker network. The database is accessible to the API container using the hostname `db`.

Create custom network:
```bash
docker network create truck-signs-network
```

Run database:
```bash
docker run -d \
  --name truck-signs-db \
  --network truck-signs-network \
  -e POSTGRES_DB=truck_signs_db \
  postgres:15
```

Run API (connects to db via hostname 'truck-signs-db'):
```bash
docker run -d \
  --name truck-signs-api \
  --network truck-signs-network \
  -p 8020:8020 \
  -e DOCKER_DB_HOST=truck-signs-db \
  truck-signs-api
```

## API Documentation

The API provides the following endpoints:

- `GET /admin/` - Django admin interface
- `GET /api/` - API root (browsable API)
- `GET /health/` - Health check endpoint

Access the browsable API at `http://localhost:8020/api/` when the server is running.

## Development

For local development without Docker:

Create virtual environment:
```bash
python -m venv venv
```

Activate virtual environment (Linux/Mac):
```bash
source venv/bin/activate
```

Activate virtual environment (Windows):
```bash
venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run migrations:
```bash
python manage.py migrate
```

Create superuser:
```bash
python manage.py createsuperuser
```

Run development server:
```bash
python manage.py runserver
```

## Testing

The application includes automated testing.

Run tests in container:
```bash
docker-compose exec web python manage.py test
```

Run with coverage:
```bash
docker-compose exec web coverage run --source='.' manage.py test
docker-compose exec web coverage report
```
