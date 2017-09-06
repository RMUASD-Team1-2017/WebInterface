#!/bin/bash
python manage.py migrate
python manage.py runserver 0.0.0.0:8000 &
while true
do
  sleep 1000
done
