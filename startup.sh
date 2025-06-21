#!/bin/bash

# Exit on any failure
set -e

echo "Starting icat-api deployment on Azure Web App..."

# Ensure we're in the correct directory
cd /home/site/wwwroot

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install Gunicorn if not in requirements.txt
pip install gunicorn

# Set environment variables for production
export DJANGO_SETTINGS_MODULE=icat.settings

# Wait for database to be available (optional, useful for MySQL/PostgreSQL)
echo "Waiting for database to be available..."
python -c "
import os
import time
import dj_database_url
import sys

# Parse database URL
db_config = dj_database_url.parse(os.environ.get('DATABASE_URL', ''))
if db_config:
    print('Database configuration found. Proceeding...')
else:
    print('Warning: No DATABASE_URL found')
    sys.exit(0)
"

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create superuser if it doesn't exist (optional)
# echo "Creating superuser if needed..."
# python manage.py shell -c "
# from django.contrib.auth import get_user_model
# User = get_user_model()
# if not User.objects.filter(is_superuser=True).exists():
#     User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
#     print('Superuser created')
# else:
#     print('Superuser already exists')
# "

# Start the application with Gunicorn
echo "Starting Django application with Gunicorn..."

# Determine the port (Azure Web Apps typically use port 80 or the PORT environment variable)
PORT=${PORT:-8000}

# Start Gunicorn with appropriate settings for Azure Web Apps
exec gunicorn \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --worker-class sync \
    --worker-connections 1000 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --timeout 30 \
    --keep-alive 2 \
    --log-level info \
    --access-logfile - \
    --error-logfile - \
    --capture-output \
    icat.wsgi:application
