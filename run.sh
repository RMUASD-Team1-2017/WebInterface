#!/bin/bash
export rmq_user=drone
export rmq_pass=drone
export rmq_host=drone.stefanrvo.dk
python manage.py migrate
python manage.py runserver 0.0.0.0:8000 &
while true
do
  sleep 1000
done
