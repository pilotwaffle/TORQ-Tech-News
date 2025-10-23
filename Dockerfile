FROM python:3.11-slim

# Cache buster - updated timestamp
ENV REBUILD_TIMESTAMP=2025-10-23-fix-port-and-slugs

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Set environment variables
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Run Gunicorn directly with dynamic PORT from Railway
CMD gunicorn --bind 0.0.0.0:${PORT:-8080} --workers 4 --threads 2 --worker-class gevent --timeout 120 --access-logfile - --error-logfile - app:app
