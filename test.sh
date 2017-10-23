#!/bin/bash
export rmq_user=guest
export rmq_pass=guest
export rmq_host=localhost
#Run Django unittests
python manage.py test
