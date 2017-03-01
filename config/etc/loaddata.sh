#!/bin/sh
echo "pass loading initial data"
python3.4 manage.py loaddata /var/www/appserver/appserver/fixtures/*
