#!/bin/bash
if [ -z "$WEB_CONCURRENCY" ]; then
# modified to only 1 worker, TODO: Create a independent service
# for async scheduler
  WEB_CONCURRENCY=1
fi

exec gunicorn app.main:app \
  --workers $WEB_CONCURRENCY \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8036 \
  --log-level info \
  --access-logfile - \
  --error-logfile -