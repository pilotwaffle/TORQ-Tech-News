#!/usr/bin/env python3
"""
Railway production startup script.
Forces Gunicorn to run instead of Flask dev server.
"""
import os
import sys

if __name__ == '__main__':
    # Get port from environment
    port = os.environ.get('PORT', '8080')
    
    # Force Gunicorn startup
    os.execvp('gunicorn', [
        'gunicorn',
        '--bind', f'0.0.0.0:{port}',
        '--workers', '4',
        '--threads', '2',
        '--worker-class', 'gevent',
        '--timeout', '120',
        '--access-logfile', '-',
        '--error-logfile', '-',
        'app:app'
    ])
