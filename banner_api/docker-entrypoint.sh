#!/bin/sh

alembic upgrade head

if [ "$APP_DEBUG" = "True" ]; then
    echo "DEBUG MODE"
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
else
    echo "RELEASE MODE"
    gunicorn main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --proxy-allow-from nginx
fi