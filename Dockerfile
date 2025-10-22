FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Railway automatically sets PORT environment variable
# Gunicorn will read it at runtime: ${PORT}
CMD gunicorn --bind 0.0.0.0:${PORT:-8080} --workers 4 --threads 2 --worker-class gevent --timeout 120 --access-logfile - --error-logfile - app:app
