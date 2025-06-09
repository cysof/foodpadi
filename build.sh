#!/usr/bin/env bash
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser only if it doesn't exist
if [[ $CREATE_SUPERUSER == "True" ]]; then
  python <<EOF
import os
from django.contrib.auth import get_user_model
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "foodpadi.settings")

import django
django.setup()

User = get_user_model()
phone = os.environ["DJANGO_SUPERUSER_PHONE"]
username = os.environ["DJANGO_SUPERUSER_USERNAME"]
email = os.environ["DJANGO_SUPERUSER_EMAIL"]
password = os.environ["DJANGO_SUPERUSER_PASSWORD"]

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(phone=phone, username=username, email=email, password=password)
    print("✅ Superuser created with phone:", phone)
else:
    print("ℹ️ Superuser with phone", phone, "already exists.")
EOF
fi
