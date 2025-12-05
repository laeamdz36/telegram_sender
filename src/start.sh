#!/bin/bash
if [ -z "$WEB_CONCURRENCY" ]; then
  WEB_CONCURRENCY=4
fi

# El comando clave: Gunicorn llama a Uvicorn
exec gunicorn app.main:app \
  --workers $WEB_CONCURRENCY \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8036 \
  --log-level info