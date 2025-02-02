#!/usr/bin/env bash
# exit on error
set -o errexit

# Delete the database (if using SQLite)
rm db.sqlite3

# Delete migrations (except __init__.py)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete



pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata data_converted.json
