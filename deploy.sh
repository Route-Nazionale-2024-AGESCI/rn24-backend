#!/bin/bash
cd /opt/rn24-backend
echo $CR_PAT | docker login ghcr.io -u USERNAME --password-stdin
git pull origin master
docker compose pull
docker compose exec backend python manage.py migrate --noinput
docker compose exec backend python manage.py collectstatic --noinput
docker compose up -d
