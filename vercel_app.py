#!/usr/bin/env python3
"""
Vercel-compatible static file server for TORQ Tech News
This is a simplified version that works with Vercel's serverless environment
"""

from flask import Flask, send_from_directory, jsonify
import os
import json

app = Flask(__name__, static_folder='.')

# Serve static files
@app.route('/')
def home():
    """Serve homepage"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    try:
        return send_from_directory('.', filename)
    except:
        return send_from_directory('.', 'index.html')

@app.route('/topics/<topic>')
def topic_page(topic):
    """Serve topic pages"""
    return send_from_directory('.', 'topic.html')

@app.route('/article/<slug>')
def article_page(slug):
    """Serve article pages"""
    return send_from_directory('.', 'article.html')

@app.route('/api/health')
@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'TORQ Tech News',
        'version': '1.0.0'
    })

# This is required for Vercel
if __name__ == '__main__':
    app.run()
