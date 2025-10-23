#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MIT Sloan Review - Full Web Application
Complete website with visitor tracking, dynamic content, automation, and advanced analytics
"""

import sys
import os

# Force UTF-8 encoding for Windows compatibility
if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'

from flask import Flask, render_template, jsonify, request, send_from_directory
from datetime import datetime, timedelta
import json
import random
import threading
import time
import sqlite3
from pathlib import Path
import hashlib
import html
import unicodedata
import re
from user_agents import parse

app = Flask(__name__,
           static_folder='.',
           template_folder='.')

# Database setup
# Use relative path for cross-platform compatibility
import os
DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "analytics.db")
DATA_CACHE_PATH = os.path.join(DB_DIR, "data_cache.json")

def init_db():
    """Initialize database for analytics and content with advanced tracking"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Visitors table (existing)
    c.execute('''CREATE TABLE IF NOT EXISTS visitors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip_hash TEXT,
        user_agent TEXT,
        page_url TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        session_id TEXT
    )''')

    # Page views table (existing)
    c.execute('''CREATE TABLE IF NOT EXISTS page_views (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        article_id TEXT,
        article_title TEXT,
        view_count INTEGER DEFAULT 1,
        last_viewed DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    # Articles table with full content (existing)
    c.execute('''CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        slug TEXT UNIQUE,
        title TEXT,
        excerpt TEXT,
        content TEXT,
        category TEXT,
        author TEXT,
        author_title TEXT,
        published_date TEXT,
        reading_time INTEGER,
        image_url TEXT,
        views INTEGER DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    # ===== ADVANCED ANALYTICS TABLES =====

    # User sessions table - Track complete user sessions
    c.execute('''CREATE TABLE IF NOT EXISTS user_sessions (
        session_id TEXT PRIMARY KEY,
        visitor_id TEXT,
        start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
        end_time DATETIME,
        total_pages INTEGER DEFAULT 0,
        duration_seconds INTEGER DEFAULT 0,
        bounce_rate REAL DEFAULT 0,
        device_type TEXT,
        browser TEXT,
        os TEXT,
        screen_resolution TEXT,
        referrer_url TEXT,
        landing_page TEXT,
        is_active INTEGER DEFAULT 1
    )''')

    # User events table - Track granular user interactions
    c.execute('''CREATE TABLE IF NOT EXISTS user_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        event_type TEXT,
        element_id TEXT,
        value TEXT,
        page_url TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (session_id) REFERENCES user_sessions(session_id)
    )''')

    # Referrers table - Track traffic sources
    c.execute('''CREATE TABLE IF NOT EXISTS referrers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        referrer_url TEXT,
        landing_page TEXT,
        count INTEGER DEFAULT 1,
        first_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
        last_seen DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    # Devices table - Track device information
    c.execute('''CREATE TABLE IF NOT EXISTS devices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_type TEXT,
        browser TEXT,
        os TEXT,
        screen_resolution TEXT,
        session_id TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (session_id) REFERENCES user_sessions(session_id)
    )''')

    # Conversion funnels table - Track user journey steps
    c.execute('''CREATE TABLE IF NOT EXISTS conversion_funnels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        funnel_step TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        metadata TEXT,
        FOREIGN KEY (session_id) REFERENCES user_sessions(session_id)
    )''')

    # Create indexes for performance
    c.execute('CREATE INDEX IF NOT EXISTS idx_visitors_session ON visitors(session_id)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_visitors_timestamp ON visitors(timestamp)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_sessions_start_time ON user_sessions(start_time)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_events_session ON user_events(session_id)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_events_type ON user_events(event_type)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_events_timestamp ON user_events(timestamp)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_funnels_session ON conversion_funnels(session_id)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_funnels_step ON conversion_funnels(funnel_step)')

    conn.commit()
    conn.close()
    print("[DB] Database initialized successfully with advanced analytics")

def migrate_db():
    """Migrate existing database to include advanced analytics tables"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    try:
        # Check if advanced tables exist
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_sessions'")
        if not c.fetchone():
            print("[DB MIGRATION] Adding advanced analytics tables...")
            init_db()
            print("[DB MIGRATION] Migration completed successfully")
        else:
            print("[DB MIGRATION] Advanced analytics tables already exist")
    except Exception as e:
        print(f"[DB MIGRATION ERROR] {e}")
    finally:
        conn.close()

def init_data_cache():
    """Initialize data cache file if it doesn't exist"""
    if not os.path.exists(DATA_CACHE_PATH):
        print("[CACHE] data_cache.json not found, creating default cache...")
        default_data = {
            "featured": {
                "title": "The Future of Digital Transformation in Enterprise",
                "excerpt": "How leading organizations are leveraging AI and automation to stay competitive",
                "category": "Digital Transformation",
                "author": "Dr. Sarah Chen",
                "author_title": "Professor of Digital Strategy",
                "date": "December 15, 2024",
                "reading_time": 8,
                "image": ""
            },
            "articles": [
                {
                    "title": "AI Strategy: Building Competitive Advantage",
                    "excerpt": "Strategic frameworks for AI implementation",
                    "category": "AI Strategy",
                    "author": "Robert C. Pozen",
                    "date": "December 10, 2024",
                    "reading_time": 6
                },
                {
                    "title": "Leadership in the Age of Automation",
                    "excerpt": "How leaders can navigate technological disruption",
                    "category": "Leadership",
                    "author": "Renee Fry",
                    "date": "December 8, 2024",
                    "reading_time": 7
                },
                {
                    "title": "Sustainability Meets Innovation",
                    "excerpt": "Creating sustainable business models",
                    "category": "Sustainability",
                    "author": "Sam Ransbotham",
                    "date": "December 5, 2024",
                    "reading_time": 5
                }
            ]
        }
        with open(DATA_CACHE_PATH, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, indent=2, ensure_ascii=False)
        print("[CACHE] Default data cache created successfully")
    else:
        print("[CACHE] data_cache.json found")

# Initialize database and data cache on startup
init_db()
migrate_db()
init_data_cache()

# Content generator for full articles
class ContentGenerator:
    """Generates full article content"""

    ARTICLE_TEMPLATES = [
        {
            "intro": "In today's rapidly evolving business landscape, {topic} has emerged as a critical factor for organizational success. Recent research from MIT Sloan Management Review reveals surprising insights into how leading companies are approaching this challenge.",
            "body": [
                "Our comprehensive study of over 500 organizations across various industries has uncovered several key patterns. First, companies that prioritize {focus_area} consistently outperform their competitors by an average of 23% in terms of revenue growth.",
                "The research methodology involved extensive interviews with C-suite executives, detailed analysis of financial performance data, and surveys of over 10,000 employees. What emerged was a clear framework for success.",
                "Three critical success factors stood out: strategic alignment, operational excellence, and cultural transformation. Organizations that excelled in all three areas demonstrated remarkable resilience during market disruptions.",
                "However, implementation is where many companies struggle. Our findings suggest that 68% of initiatives fail not due to poor strategy, but because of inadequate execution and change management.",
                "The most successful organizations follow a systematic approach: they start with pilot programs, measure results rigorously, and scale gradually. This reduces risk while building organizational capability."
            ],
            "conclusion": "As we look to the future, the organizations that will thrive are those that embrace {topic} not as a one-time initiative, but as an ongoing journey of continuous improvement and adaptation."
        },
        {
            "intro": "The question facing business leaders today is not whether to embrace {topic}, but how to do so effectively. Drawing on extensive research and real-world case studies, we explore what separates successful implementations from failures.",
            "body": [
                "The landscape of {topic} has changed dramatically over the past decade. What was once considered cutting-edge is now table stakes for competitive survival.",
                "Our analysis of industry leaders reveals a common pattern: they invest heavily in {focus_area} while maintaining flexibility to adapt as circumstances change.",
                "Consider the case of a Fortune 500 company we'll call GlobalTech. By implementing a comprehensive {topic} strategy, they increased productivity by 34% while reducing costs by 18%.",
                "The key to their success was a holistic approach that addressed technology, processes, and people simultaneously. Too often, organizations focus on just one dimension and wonder why results fall short.",
                "Data from our longitudinal study spanning five years shows that sustainable results require sustained commitment from senior leadership, adequate resources, and a willingness to learn from failures."
            ],
            "conclusion": "The path forward is clear: organizations must develop deep expertise in {topic}, foster a culture of innovation, and remain committed to long-term value creation over short-term gains."
        }
    ]

    TOPICS = {
        "AI Strategy": {
            "focus": "artificial intelligence integration",
            "keywords": ["machine learning", "automation", "data analytics", "predictive models"]
        },
        "Leadership": {
            "focus": "leadership development and team empowerment",
            "keywords": ["emotional intelligence", "team dynamics", "decision-making", "communication"]
        },
        "Sustainability": {
            "focus": "environmental sustainability and ESG practices",
            "keywords": ["circular economy", "carbon reduction", "social impact", "governance"]
        },
        "Innovation": {
            "focus": "organizational innovation capabilities",
            "keywords": ["design thinking", "agile methodologies", "experimentation", "R&D"]
        },
        "Strategy": {
            "focus": "strategic planning and execution",
            "keywords": ["competitive advantage", "market positioning", "business models", "growth"]
        },
        "Digital Transformation": {
            "focus": "digital technology adoption",
            "keywords": ["cloud computing", "digital platforms", "customer experience", "automation"]
        }
    }

    @classmethod
    def generate_full_article(cls, title, category):
        """Generate complete article with multiple paragraphs"""
        template = random.choice(cls.ARTICLE_TEMPLATES)

        # Determine topic and focus area
        topic = title.split(':')[0] if ':' in title else title
        topic_data = cls.TOPICS.get(category, cls.TOPICS["Strategy"])
        focus_area = topic_data["focus"]

        # Generate content
        intro = template["intro"].format(topic=topic, focus_area=focus_area)
        body_paragraphs = [p.format(topic=topic, focus_area=focus_area) for p in template["body"]]
        conclusion = template["conclusion"].format(topic=topic, focus_area=focus_area)

        # Combine into HTML
        html_content = f"""
        <div class="article-full-content">
            <p class="lead-paragraph">{intro}</p>

            <h3>Key Findings</h3>
            {"".join(f'<p>{p}</p>' for p in body_paragraphs[:3])}

            <h3>Practical Implications</h3>
            {"".join(f'<p>{p}</p>' for p in body_paragraphs[3:])}

            <h3>Conclusion</h3>
            <p>{conclusion}</p>

            <div class="key-takeaways">
                <h4>Key Takeaways</h4>
                <ul>
                    <li>Organizations must develop systematic approaches to {category.lower()}</li>
                    <li>Success requires alignment across technology, processes, and people</li>
                    <li>Long-term commitment and adaptability are essential</li>
                    <li>Measuring results and learning from failures drives improvement</li>
                </ul>
            </div>
        </div>
        """

        return html_content

def normalize_slug(title):
    """Normalize title to slug format (same as JavaScript)"""
    import re
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)  # Remove non-alphanumeric except spaces and dashes
    slug = re.sub(r'\s+', '-', slug)  # Replace spaces with dashes
    slug = re.sub(r'^-+|-+$', '', slug)  # Remove leading/trailing dashes
    return slug[:50]  # Limit to 50 characters

def parse_user_agent(ua_string):
    """Parse user agent string to extract device info"""
    try:
        user_agent = parse(ua_string)
        return {
            'device_type': 'mobile' if user_agent.is_mobile else ('tablet' if user_agent.is_tablet else 'desktop'),
            'browser': f"{user_agent.browser.family} {user_agent.browser.version_string}",
            'os': f"{user_agent.os.family} {user_agent.os.version_string}"
        }
    except:
        return {
            'device_type': 'unknown',
            'browser': 'unknown',
            'os': 'unknown'
        }

# Visitor tracking with enhanced device detection
def track_visitor(page_url):
    """Track visitor analytics with device detection"""
    try:
        ip = request.remote_addr
        user_agent = request.headers.get('User-Agent', '')
        referrer = request.headers.get('Referer', 'direct')

        # Hash IP for privacy
        ip_hash = hashlib.sha256(ip.encode()).hexdigest()[:16]

        # Generate session ID
        session_id = request.cookies.get('session_id', hashlib.sha256(
            f"{ip}{user_agent}{datetime.now().hour}".encode()
        ).hexdigest()[:16])

        # Parse device info
        device_info = parse_user_agent(user_agent)

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Insert visitor record
        c.execute('''INSERT INTO visitors (ip_hash, user_agent, page_url, session_id)
                    VALUES (?, ?, ?, ?)''', (ip_hash, user_agent, page_url, session_id))

        # Update or create session
        c.execute('SELECT session_id FROM user_sessions WHERE session_id = ?', (session_id,))
        session_exists = c.fetchone()

        if not session_exists:
            # Create new session
            c.execute('''INSERT INTO user_sessions
                        (session_id, visitor_id, landing_page, referrer_url, device_type, browser, os)
                        VALUES (?, ?, ?, ?, ?, ?, ?)''',
                     (session_id, ip_hash, page_url, referrer,
                      device_info['device_type'], device_info['browser'], device_info['os']))

            # Track funnel: homepage visit
            if page_url == '/':
                c.execute('''INSERT INTO conversion_funnels (session_id, funnel_step, metadata)
                            VALUES (?, ?, ?)''', (session_id, 'homepage', json.dumps({'referrer': referrer})))

            # Track referrer
            if referrer != 'direct':
                c.execute('SELECT id, count FROM referrers WHERE referrer_url = ? AND landing_page = ?',
                         (referrer, page_url))
                ref_result = c.fetchone()
                if ref_result:
                    c.execute('UPDATE referrers SET count = ?, last_seen = CURRENT_TIMESTAMP WHERE id = ?',
                             (ref_result[1] + 1, ref_result[0]))
                else:
                    c.execute('''INSERT INTO referrers (referrer_url, landing_page, count)
                                VALUES (?, ?, 1)''', (referrer, page_url))
        else:
            # Update existing session
            c.execute('UPDATE user_sessions SET total_pages = total_pages + 1 WHERE session_id = ?',
                     (session_id,))

        conn.commit()
        conn.close()

        return session_id
    except Exception as e:
        print(f"[ERROR] Tracking error: {e}")
        return None

def track_article_view(article_id, article_title):
    """Track article views"""
    try:
        session_id = request.cookies.get('session_id')

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Check if article exists in page_views
        c.execute('SELECT view_count FROM page_views WHERE article_id = ?', (article_id,))
        result = c.fetchone()

        if result:
            # Update view count
            new_count = result[0] + 1
            c.execute('''UPDATE page_views SET view_count = ?, last_viewed = CURRENT_TIMESTAMP
                        WHERE article_id = ?''', (new_count, article_id))
        else:
            # Insert new record
            c.execute('''INSERT INTO page_views (article_id, article_title, view_count)
                        VALUES (?, ?, 1)''', (article_id, article_title))

        # Track funnel: article view
        if session_id:
            c.execute('''INSERT INTO conversion_funnels (session_id, funnel_step, metadata)
                        VALUES (?, ?, ?)''',
                     (session_id, 'article_view', json.dumps({'article_id': article_id, 'title': article_title})))

        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[ERROR] Article tracking error: {e}")

# ===== ADVANCED ANALYTICS API ENDPOINTS =====

@app.route('/api/track-event', methods=['POST'])
def track_event():
    """Track user events (scroll, click, time-on-page, etc.)"""
    try:
        data = request.get_json()
        session_id = data.get('session_id') or request.cookies.get('session_id')
        event_type = data.get('event_type')
        element_id = data.get('element_id', '')
        value = data.get('value', '')
        page_url = data.get('page_url', '')

        if not session_id or not event_type:
            return jsonify({'error': 'Missing required fields'}), 400

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Insert event
        c.execute('''INSERT INTO user_events (session_id, event_type, element_id, value, page_url)
                    VALUES (?, ?, ?, ?, ?)''',
                 (session_id, event_type, element_id, str(value), page_url))

        # Track specific funnel events
        if event_type == 'scroll_depth' and value == '100':
            c.execute('''INSERT INTO conversion_funnels (session_id, funnel_step, metadata)
                        VALUES (?, ?, ?)''',
                     (session_id, 'scroll_100', json.dumps({'page': page_url})))
        elif event_type == 'outbound_link':
            c.execute('''INSERT INTO conversion_funnels (session_id, funnel_step, metadata)
                        VALUES (?, ?, ?)''',
                     (session_id, 'external_click', json.dumps({'url': value})))

        conn.commit()
        conn.close()

        return jsonify({'status': 'success'}), 200

    except Exception as e:
        print(f"[ERROR] Event tracking error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/track-session', methods=['POST'])
def track_session():
    """Track session lifecycle events"""
    try:
        data = request.get_json()
        session_id = data.get('session_id') or request.cookies.get('session_id')
        action = data.get('action')  # 'start', 'update', 'end'
        duration = data.get('duration', 0)
        screen_resolution = data.get('screen_resolution', '')

        if not session_id:
            return jsonify({'error': 'Missing session_id'}), 400

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        if action == 'end':
            # Calculate bounce rate (1 if only one page viewed, 0 otherwise)
            c.execute('SELECT total_pages FROM user_sessions WHERE session_id = ?', (session_id,))
            result = c.fetchone()
            if result:
                bounce_rate = 1.0 if result[0] <= 1 else 0.0
                c.execute('''UPDATE user_sessions
                            SET end_time = CURRENT_TIMESTAMP, duration_seconds = ?,
                                bounce_rate = ?, is_active = 0
                            WHERE session_id = ?''',
                         (duration, bounce_rate, session_id))
        elif action == 'update':
            c.execute('''UPDATE user_sessions
                        SET duration_seconds = ?, screen_resolution = ?
                        WHERE session_id = ?''',
                     (duration, screen_resolution, session_id))

        conn.commit()
        conn.close()

        return jsonify({'status': 'success'}), 200

    except Exception as e:
        print(f"[ERROR] Session tracking error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/advanced')
def advanced_analytics():
    """Get advanced analytics data"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Average session duration
        c.execute('''SELECT AVG(duration_seconds) FROM user_sessions
                    WHERE duration_seconds > 0 AND start_time > datetime('now', '-7 days')''')
        avg_duration = c.fetchone()[0] or 0

        # Bounce rate
        c.execute('''SELECT AVG(bounce_rate) FROM user_sessions
                    WHERE start_time > datetime('now', '-7 days')''')
        bounce_rate = c.fetchone()[0] or 0

        # Top referrers
        c.execute('''SELECT referrer_url, SUM(count) as total FROM referrers
                    GROUP BY referrer_url ORDER BY total DESC LIMIT 10''')
        top_referrers = [{'url': row[0], 'count': row[1]} for row in c.fetchall()]

        # Device breakdown
        c.execute('''SELECT device_type, COUNT(*) as count FROM user_sessions
                    WHERE start_time > datetime('now', '-7 days')
                    GROUP BY device_type''')
        devices = [{'type': row[0], 'count': row[1]} for row in c.fetchall()]

        # Browser breakdown
        c.execute('''SELECT browser, COUNT(*) as count FROM user_sessions
                    WHERE start_time > datetime('now', '-7 days')
                    GROUP BY browser ORDER BY count DESC LIMIT 10''')
        browsers = [{'browser': row[0], 'count': row[1]} for row in c.fetchall()]

        # Conversion funnel
        c.execute('''SELECT funnel_step, COUNT(*) as count FROM conversion_funnels
                    WHERE timestamp > datetime('now', '-7 days')
                    GROUP BY funnel_step''')
        funnel = [{'step': row[0], 'count': row[1]} for row in c.fetchall()]

        # Popular content by hour
        c.execute('''SELECT strftime('%H', timestamp) as hour, COUNT(*) as count
                    FROM user_events
                    WHERE event_type = 'time_on_page' AND timestamp > datetime('now', '-7 days')
                    GROUP BY hour ORDER BY hour''')
        hourly_activity = [{'hour': int(row[0]), 'count': row[1]} for row in c.fetchall()]

        # User journey paths (top 10 common paths)
        c.execute('''SELECT v1.page_url as page1, v2.page_url as page2, COUNT(*) as count
                    FROM visitors v1
                    JOIN visitors v2 ON v1.session_id = v2.session_id
                        AND v2.timestamp > v1.timestamp
                    WHERE v1.timestamp > datetime('now', '-7 days')
                    GROUP BY page1, page2
                    ORDER BY count DESC LIMIT 10''')
        user_paths = [{'from': row[0], 'to': row[1], 'count': row[2]} for row in c.fetchall()]

        # Scroll depth statistics
        c.execute('''SELECT value, COUNT(*) as count FROM user_events
                    WHERE event_type = 'scroll_depth' AND timestamp > datetime('now', '-7 days')
                    GROUP BY value ORDER BY value''')
        scroll_depths = [{'depth': row[0], 'count': row[1]} for row in c.fetchall()]

        # Active sessions count
        c.execute('SELECT COUNT(*) FROM user_sessions WHERE is_active = 1')
        active_sessions = c.fetchone()[0] or 0

        # Total sessions (7 days)
        c.execute('''SELECT COUNT(*) FROM user_sessions
                    WHERE start_time > datetime('now', '-7 days')''')
        total_sessions = c.fetchone()[0] or 0

        conn.close()

        return jsonify({
            'avg_session_duration': round(avg_duration, 2),
            'bounce_rate': round(bounce_rate * 100, 2),
            'top_referrers': top_referrers,
            'devices': devices,
            'browsers': browsers,
            'conversion_funnel': funnel,
            'hourly_activity': hourly_activity,
            'user_paths': user_paths,
            'scroll_depths': scroll_depths,
            'active_sessions': active_sessions,
            'total_sessions_7d': total_sessions
        })

    except Exception as e:
        print(f"[ERROR] Advanced analytics error: {e}")
        return jsonify({'error': str(e)}), 500

# Routes
@app.route('/')
def home():
    """Home page"""
    session_id = track_visitor('/')

    # Load articles from cache
    try:
        with open(DATA_CACHE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            articles = data.get('articles', [])
    except Exception as e:
        print(f"[ERROR] Failed to load cache in home route: {e}")
        articles = []

    response = send_from_directory('.', 'index.html')
    if session_id:
        response.set_cookie('session_id', session_id, max_age=86400)  # 24 hours
    return response

@app.route('/analytics.js')
def serve_analytics_js():
    """Serve analytics tracking script"""
    return send_from_directory('.', 'analytics.js')

@app.route('/styles.css')
def serve_css():
    """Serve CSS file"""
    return send_from_directory('.', 'styles.css')

@app.route('/script.js')
def serve_js():
    """Serve main JavaScript file"""
    return send_from_directory('.', 'script.js')

@app.route('/make_articles_clickable.js')
def serve_clickable_js():
    """Serve clickable articles JavaScript"""
    return send_from_directory('.', 'make_articles_clickable.js')

@app.route('/populate_ai_section.js')
def serve_ai_js():
    """Serve AI section JavaScript"""
    return send_from_directory('.', 'populate_ai_section.js')

@app.route('/populate_main_articles.js')
def serve_main_articles_js():
    """Serve main articles population JavaScript"""
    return send_from_directory('.', 'populate_main_articles.js')

@app.route('/data_cache.json')
def serve_data_cache():
    """Serve data cache for client-side rendering"""
    return send_from_directory(DB_DIR, 'data_cache.json')

@app.route('/torq-logo.svg')
def serve_logo():
    """Serve TORQ logo"""
    return send_from_directory(DB_DIR, 'torq-logo.svg')


@app.route('/topics/<topic>')
def topic_page(topic):
    """Display articles filtered by topic/category"""
    session_id = track_visitor(f'/topics/{topic}')

    # Load articles from cache
    try:
        with open(DATA_CACHE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            all_articles = data.get('articles', [])
    except Exception as e:
        print(f"[ERROR] Failed to load cache: {e}")
        all_articles = []

    # Topic mapping
    topic_map = {
        'innovation': 'Innovation',
        'leadership': 'Leadership',
        'strategy': 'Strategy',
        'sustainability': 'Sustainability',
        'technology': 'Technology',
        'operations': 'Operations'
    }

    display_topic = topic_map.get(topic.lower(), topic.title())

    # Filter articles by category
    filtered_articles = [
        a for a in all_articles
        if display_topic.lower() in a.get('category', '').lower()
    ]

    # Fallback: if no exact category match, search in title/excerpt
    if not filtered_articles:
        filtered_articles = [
            a for a in all_articles
            if (display_topic.lower() in a.get('title', '').lower() or
                display_topic.lower() in a.get('excerpt', '').lower())
        ]

    return render_template('topic.html',
                         topic=display_topic,
                         articles=filtered_articles,
                         count=len(filtered_articles),
                         session_id=session_id)


@app.route('/article/<slug>')
def article_detail(slug):
    """Full article page - displays extracted content on-site with source attribution"""
    session_id = track_visitor(f'/article/{slug}')

    # Clean up the incoming slug
    slug = slug.strip('-')

    # Load data cache to get article data
    try:
        with open(DATA_CACHE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            articles = data.get('articles', [])
            featured = data.get('featured', {})
    except Exception as e:
        print(f"[ERROR] Failed to load data cache: {e}")
        articles = []
        featured = {}

    # Check featured article first
    if featured and featured.get('slug') == slug:
        cached_article = featured
    else:
        # Find matching article in regular articles using normalized slug
        cached_article = next((a for a in articles if a.get('slug') == slug), None)

    # If still not found, try fuzzy matching
    if not cached_article:
        if featured and featured.get('slug', '').startswith(slug[:20]):
            cached_article = featured
        else:
            cached_article = next((a for a in articles if a.get('slug', '').startswith(slug[:20])), None)

    if not cached_article:
        return "Article not found", 404

    # Track view
    track_article_view(slug, cached_article.get('title', 'Unknown'))

    # Check if we have extracted full_text content
    has_extracted_content = cached_article.get('full_text') and len(cached_article.get('full_text', '')) > 100

    # Prepare article content
    if has_extracted_content:
        # Use extracted content with proper attribution
        article_content = cached_article.get('full_text', '')

        # Normalize Unicode text to ASCII for Windows compatibility
        # First normalize to decomposed form (NFD), then encode as ASCII ignoring errors
        article_content = unicodedata.normalize('NFKD', article_content)
        article_content = article_content.encode('ascii', 'ignore').decode('ascii')

        # Format article text into HTML paragraphs (escape HTML to prevent injection)
        paragraphs = article_content.split('\n\n')
        formatted_content = ''.join(f'<p>{html.escape(p.strip())}</p>' for p in paragraphs if p.strip())

        # Add source attribution banner at the top
        source_name = html.escape(cached_article.get('source', 'Original Source'))
        source_url = html.escape(cached_article.get('link', '#'))

        source_banner = f"""
        <div class="source-attribution">
            <div class="attribution-icon">ℹ️</div>
            <div class="attribution-text">
                <strong>Content from {source_name}</strong>
                <p>This article is aggregated from the original source. We've extracted and displayed it here for your convenience with proper attribution.</p>
            </div>
        </div>
        """

        full_content = f"""
        {source_banner}
        <div class="article-full-content extracted-content">
            {formatted_content}
        </div>
        <div class="original-source-cta">
            <a href="{source_url}" target="_blank" rel="noopener noreferrer" class="read-original-btn">
                📰 Read Original Article at {source_name}
            </a>
        </div>
        """

        # Use summary for excerpt if available
        excerpt = cached_article.get('summary', cached_article.get('excerpt', ''))
        keywords = ', '.join(cached_article.get('keywords', [])[:5]) if cached_article.get('keywords') else ''

    else:
        # Fall back to generated content
        full_content = ContentGenerator.generate_full_article(
            cached_article['title'],
            cached_article.get('category', 'Strategy')
        )
        excerpt = cached_article.get('excerpt', '')
        keywords = cached_article.get('category', 'Technology')

    # Prepare meta information (escape for HTML safety)
    title = html.escape(cached_article.get('title', 'Article'))
    category = html.escape(cached_article.get('category', 'Technology'))
    author = html.escape(cached_article.get('author', 'Unknown'))
    date = html.escape(cached_article.get('date', datetime.now().strftime("%B %d, %Y")))
    reading_time = cached_article.get('reading_time', 10)

    # Prepare excerpt and keywords for meta tags (escape quotes and HTML)
    excerpt_text = excerpt.replace('"', '&quot;').replace("'", '&#39;')[:160]
    keywords_text = keywords.replace('"', '&quot;').replace("'", '&#39;') if keywords else ''

    # Prepare JSON-safe strings for structured data
    title_json = title.replace('"', '\\"')
    author_json = author.replace('"', '\\"')
    excerpt_json = excerpt_text[:200].replace('"', '\\"')
    category_json = category.replace('"', '\\"')

    # Render article template with SEO optimization
    article_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <!-- SEO Meta Tags -->
        <title>{title} - TORQ Tech News</title>
        <meta name="description" content="{excerpt_text}">
        <meta name="keywords" content="{keywords_text}">
        <meta name="author" content="{author}">

        <!-- Open Graph / Facebook -->
        <meta property="og:type" content="article">
        <meta property="og:title" content="{title}">
        <meta property="og:description" content="{excerpt_text[:200]}">
        <meta property="og:site_name" content="TORQ Tech News">

        <!-- Twitter Card -->
        <meta name="twitter:card" content="summary_large_image">
        <meta name="twitter:title" content="{title}">
        <meta name="twitter:description" content="{excerpt_text[:200]}">

        <!-- Structured Data (Schema.org) -->
        <script type="application/ld+json">
        {{
          "@context": "https://schema.org",
          "@type": "NewsArticle",
          "headline": "{title_json}",
          "description": "{excerpt_json}",
          "author": {{
            "@type": "Person",
            "name": "{author_json}"
          }},
          "publisher": {{
            "@type": "Organization",
            "name": "TORQ Tech News",
            "logo": {{
              "@type": "ImageObject",
              "url": "https://torqtechnews.com/torq-logo.svg"
            }}
          }},
          "datePublished": "{date}",
          "articleSection": "{category_json}"
        }}
        </script>

        <link rel="stylesheet" href="/styles.css">
        <script src="/analytics.js" defer></script>
        <style>
            .article-detail {{
                max-width: 800px;
                margin: 0 auto;
                padding: 2rem;
            }}
            .article-header {{
                margin-bottom: 2rem;
                padding-bottom: 2rem;
                border-bottom: 2px solid #e0e0e0;
            }}
            .article-title {{
                font-size: 2.5rem;
                font-weight: 800;
                margin-bottom: 1rem;
                color: #1a1a1a;
                line-height: 1.2;
            }}
            .article-meta {{
                display: flex;
                gap: 1rem;
                color: #666;
                font-size: 0.9rem;
                flex-wrap: wrap;
            }}
            .source-attribution {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 1.5rem;
                border-radius: 12px;
                margin-bottom: 2rem;
                display: flex;
                gap: 1rem;
                align-items: flex-start;
            }}
            .attribution-icon {{
                font-size: 2rem;
                flex-shrink: 0;
            }}
            .attribution-text strong {{
                display: block;
                font-size: 1.1rem;
                margin-bottom: 0.5rem;
            }}
            .attribution-text p {{
                margin: 0;
                opacity: 0.95;
                font-size: 0.95rem;
            }}
            .article-full-content {{
                line-height: 1.8;
                font-size: 1.1rem;
            }}
            .article-full-content p {{
                margin-bottom: 1.5rem;
                color: #2d2d2d;
            }}
            .article-full-content h3 {{
                margin-top: 2rem;
                margin-bottom: 1rem;
                font-size: 1.8rem;
                color: #2d2d2d;
            }}
            .extracted-content p {{
                text-align: justify;
            }}
            .lead-paragraph {{
                font-size: 1.25rem;
                font-weight: 500;
                color: #404040;
            }}
            .key-takeaways {{
                background-color: #f5f5f5;
                padding: 2rem;
                border-left: 4px solid #ef233c;
                margin-top: 2rem;
            }}
            .key-takeaways h4 {{
                margin-top: 0;
                color: #ef233c;
            }}
            .original-source-cta {{
                margin-top: 3rem;
                padding: 2rem;
                background: linear-gradient(135deg, #ef233c 0%, #d32f2f 100%);
                border-radius: 12px;
                text-align: center;
            }}
            .read-original-btn {{
                display: inline-block;
                padding: 1rem 2rem;
                background: white;
                color: #ef233c;
                text-decoration: none;
                font-weight: 700;
                font-size: 1.1rem;
                border-radius: 8px;
                transition: all 0.3s ease;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            }}
            .read-original-btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
            }}
            .back-link {{
                display: inline-block;
                margin: 2rem 0;
                color: #ef233c;
                text-decoration: none;
                font-weight: 600;
                font-size: 1rem;
            }}
            .back-link:hover {{
                text-decoration: underline;
            }}
            @media (max-width: 768px) {{
                .article-title {{
                    font-size: 2rem;
                }}
                .article-detail {{
                    padding: 1rem;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="article-detail">
            <a href="/" class="back-link">← Back to Home</a>

            <div class="article-header">
                <div class="article-category" style="color: #ef233c; font-weight: 600; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 1px;">
                    {category}
                </div>
                <h1 class="article-title">{title}</h1>
                <div class="article-meta">
                    <span>By {author}</span>
                    <span>•</span>
                    <span>{date}</span>
                    <span>•</span>
                    <span>{reading_time} min read</span>
                </div>
            </div>

            {full_content}

            <a href="/" class="back-link">← Back to Home</a>
        </div>

        <script src="/script.js"></script>
    </body>
    </html>
    """

    # Encode HTML response as UTF-8 bytes to handle special characters
    response = app.response_class(
        response=article_html.encode('utf-8'),
        status=200,
        mimetype='text/html; charset=utf-8'
    )

    if session_id:
        response.set_cookie('session_id', session_id, max_age=86400)

    return response

@app.route('/api/analytics')
def analytics():
    """Analytics dashboard data"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Total visitors (last 24 hours)
    c.execute('''SELECT COUNT(DISTINCT session_id) FROM visitors
                WHERE timestamp > datetime('now', '-1 day')''')
    visitors_24h = c.fetchone()[0]

    # Total page views
    c.execute('SELECT COUNT(*) FROM visitors')
    total_views = c.fetchone()[0]

    # Top articles
    c.execute('''SELECT article_title, view_count FROM page_views
                ORDER BY view_count DESC LIMIT 10''')
    top_articles = [{'title': row[0], 'views': row[1]} for row in c.fetchall()]

    # Recent visitors
    c.execute('''SELECT page_url, timestamp FROM visitors
                ORDER BY timestamp DESC LIMIT 20''')
    recent_activity = [{'page': row[0], 'time': row[1]} for row in c.fetchall()]

    conn.close()

    return jsonify({
        'visitors_24h': visitors_24h,
        'total_views': total_views,
        'top_articles': top_articles,
        'recent_activity': recent_activity
    })

@app.route('/admin')
def admin_dashboard():
    """Admin dashboard"""
    return send_from_directory('.', 'admin_dashboard.html')

@app.route('/api/cron/update-content')
def cron_update_content():
    """Vercel Cron Job endpoint for automated content updates"""
    try:
        print("[CRON] Vercel Cron Job triggered")
        import automation_agent
        agent = automation_agent.ContentAgent()
        result = agent.run()

        return jsonify({
            "status": "success",
            "message": "Content updated successfully",
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        print(f"[CRON ERROR] {e}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/api/manual-update')
def manual_update():
    """Manual trigger for content update"""
    try:
        print("[MANUAL] Manual update triggered")
        import multi_source_aggregator
        aggregator = multi_source_aggregator.MultiSourceAggregator()
        result = aggregator.fetch_all_articles()

        return jsonify({
            "status": "success",
            "message": "Content updated successfully from multiple sources",
            "sources": result.get('sources_used', []),
            "article_count": len(result.get('articles', [])),
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        print(f"[MANUAL ERROR] {e}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/health')
@app.route('/api/health')
def health_check():
    """System health check endpoint for monitoring and n8n workflows"""
    try:
        # Check if data_cache.json exists and is valid
        with open(DATA_CACHE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)

        article_count = len(data.get('articles', []))
        last_update = data.get('timestamp', 'Unknown')
        sources_used = data.get('sources_used', [])

        # Check database connectivity
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM visitors')
        total_visitors = c.fetchone()[0]
        conn.close()

        return jsonify({
            'status': 'healthy',
            'version': '1.0.0',
            'service': 'TORQ Tech News',
            'timestamp': datetime.now().isoformat(),
            'data': {
                'article_count': article_count,
                'last_update': last_update,
                'sources': sources_used,
                'total_visitors': total_visitors
            },
            'components': {
                'database': 'operational',
                'cache': 'operational',
                'aggregator': 'operational'
            }
        }), 200
    except FileNotFoundError:
        return jsonify({
            'status': 'degraded',
            'version': '1.0.0',
            'service': 'TORQ Tech News',
            'timestamp': datetime.now().isoformat(),
            'error': 'Data cache not found',
            'components': {
                'database': 'operational',
                'cache': 'missing',
                'aggregator': 'unknown'
            }
        }), 503
    except Exception as e:
        return jsonify({
            'status': 'error',
            'version': '1.0.0',
            'service': 'TORQ Tech News',
            'timestamp': datetime.now().isoformat(),
            'error': str(e),
            'components': {
                'database': 'unknown',
                'cache': 'error',
                'aggregator': 'unknown'
            }
        }), 500

# Automation background task
def auto_update_content():
    """Background task to update content every 5 hours"""
    import schedule

    def run_update():
        """Run the content update"""
        try:
            print("[AUTO] Running scheduled content update...")
            import multi_source_aggregator
            aggregator = multi_source_aggregator.MultiSourceAggregator()
            aggregator.fetch_all_articles()
            print("[AUTO] Content updated successfully from multiple sources")
        except Exception as e:
            print(f"[AUTO] Error in auto-update: {e}")

    # Schedule updates every 5 hours
    schedule.every(5).hours.do(run_update)

    print("[AUTO] Content auto-update service started")
    print("[AUTO] Scheduled updates: Every 5 hours")

    # Run once immediately on startup
    print("[AUTO] Running initial content update...")
    run_update()

    # Keep checking for scheduled tasks
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

# Start background automation
def start_background_automation():
    """Start the automation thread"""
    thread = threading.Thread(target=auto_update_content, daemon=True)
    thread.start()
    print("[INFO] Background automation thread started")

if __name__ == '__main__':
    print("="*60)
    print("MIT Sloan Review - Full Web Application")
    print("="*60)
    print()
    print("[INFO] Initializing application...")
    print("[INFO] Database: E:/sloan-review-landing/analytics.db")
    print("[INFO] Advanced analytics enabled")
    print()

    # Start background automation
    start_background_automation()

    
    port = int(os.environ.get('PORT', 5000))
    
    print()
    print("="*60)
    print(f"[SUCCESS] Server starting on http://localhost:{port}")
    print(f"[INFO] Admin Dashboard: http://localhost:{port}/admin")
    print(f"[INFO] API Analytics: http://localhost:{port}/api/analytics")
    print(f"[INFO] Advanced Analytics: http://localhost:{port}/api/analytics/advanced")
    print("="*60)
    print()
    
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
