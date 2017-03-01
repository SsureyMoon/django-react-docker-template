#!/bin/sh
if [ $WORKER_SETTING = "SERVER" ]
then
  cd /tmp && npm install --no-optional
  cp -a /tmp/node_modules /var/www/appserver/
  cd /var/www/appserver && npm run cloud-build
  python3.4 manage.py migrate --noinput
  python3.4 manage.py collectstatic --noinput
fi
