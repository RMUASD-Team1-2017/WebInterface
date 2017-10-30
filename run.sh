#!/bin/bash

if [[ -z "$rmq_user" ]]; then
	export rmq_user=drone
fi
if [[ -z "$rmq_pass" ]]; then
	export rmq_pass=drone
fi
if [[ -z "$rmq_host" ]]; then
	export rmq_host=drone.stefanrvo.dk
fi
python manage.py migrate
python manage.py runserver 0.0.0.0:8000 &
while true
do
  sleep 1000
done
