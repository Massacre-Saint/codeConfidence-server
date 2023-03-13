#!/bin/bash
rm -rf ccapi/migrations
rm db.sqlite3
python manage.py migrate
python manage.py makemigrations ccapi
python manage.py migrate ccapi
python manage.py loaddata messages
python manage.py loaddata tech
