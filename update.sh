#!/bin/bash
echo 'START UPDATE.........................'


echo 'PULL CODE.........................'
pwd
sudo git pull

echo 'RELOAD UWSGI.........................'
docker exec -td backend_service uwsgi --reload /data/code/run/uwsgi.pid
echo 'END UPDATE.........................'

echo 'RESTART DJANGO.........................'
# docker-compose restart
