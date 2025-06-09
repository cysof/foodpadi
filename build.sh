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

phone_number = os.environ["DJANGO_SUPERUSER_PHONE"]
email = os.environ["DJANGO_SUPERUSER_EMAIL"]
username = os.environ["DJANGO_SUPERUSER_USERNAME"]
password = os.environ["DJANGO_SUPERUSER_PASSWORD"]
first_name = os.environ.get("DJANGO_SUPERUSER_FIRSTNAME", "Admin")
last_name = os.environ.get("DJANGO_SUPERUSER_LASTNAME", "User")
account_type = os.environ.get("DJANGO_SUPERUSER_ACCOUNT_TYPE", "FARMER")

if not User.objects.filter(phone_number=phone_number).exists():
    User.objects.create_superuser(
        phone_number=phone_number,
        email=email,
        username=username,
        
        password=password,
        first_name=first_name,
        last_name=last_name,
        account_type=account_type,
        is_staff=True,
        is_superuser=True
    )
    print("✅ Superuser created with phone:", phone_number)
else:
    print("ℹ️ Superuser with phone", phone_number, "already exists.")
EOF
fi
