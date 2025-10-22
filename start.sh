#!/bin/bash
exec gunicorn --bind 0.0.0.0:${PORT:-8080} --workers 4 --threads 2 --worker-class gevent --timeout 120 --access-logfile - --error-logfile - app:app
