#!/bin/sh
set -e

uv run python manage.py migrate --noinput --settings=config.settings.prod

uv run python -m gunicorn config.asgi:application \
  --bind 0.0.0.0:8000 \
  --workers 2 \
  --worker-class uvicorn.workers.UvicornWorker