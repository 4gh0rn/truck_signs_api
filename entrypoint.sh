#!/usr/bin/env bash
set -e

echo "Waiting for postgres to connect ..."

while ! nc -z db 5432; do
  sleep 0.1
done

echo "PostgreSQL is active"

python manage.py collectstatic --noinput --clear
# Do NOT generate migrations in production/runtime
# Apply existing migrations non-interactively
python manage.py migrate --noinput

# Create superuser if it doesn't exist
python manage.py shell -c "
from django.contrib.auth.models import User
import os
username = os.environ.get('SUPERUSER_USERNAME')
email = os.environ.get('SUPERUSER_EMAIL')
password = os.environ.get('SUPERUSER_PASSWORD')
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'Superuser {username} created with password {password}')
else:
    print(f'Superuser {username} already exists')
"

gunicorn truck_signs_designs.wsgi:application --bind 0.0.0.0:8000