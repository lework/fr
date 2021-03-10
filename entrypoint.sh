#!/bin/sh


trap stop SIGTERM SIGINT SIGQUIT SIGHUP ERR

chdir=/code

start(){
  chown -R uwsgi /code
  cd /code/
  
  python manage.py makemigrations
  python manage.py migrate
  python manage.py collectstatic
  
  [ -f /code/fr_backend/db.sqlite3 ] && { python manage.py create_demo_user; python manage.py create_demo_event; }
  
  uwsgi --ini "$chdir/uwsgi.ini"
}

stop(){
  echo "$(date +'%F %T,%3N') Stopping uwsgi..."
   
  uwsgi --stop "$chdir/uwsgi.pid"
   
  exit
}

start
