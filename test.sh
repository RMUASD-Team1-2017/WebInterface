#!/bin/bash

#Run Django unittests
cd "${0%/*}"
python manage.py test
