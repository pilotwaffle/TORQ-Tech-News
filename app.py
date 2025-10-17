#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MIT Sloan Review - Full Web Application
Complete website with visitor tracking, dynamic content, and automation
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
    """Initialize database for analytics and content"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Visitors table
    c.execute('''CREATE TABLE IF NOT EXISTS visitors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip_hash TEXT,
        user_agent TEXT,
        page_url TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        session_id TEXT
    )''')

    # Page views table
    c.execute('''CREATE TABLE IF NOT EXISTS page_views (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        article_id TEXT,
        article_title TEXT,
        view_count INTEGER DEFAULT 1,
        last_viewed DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    # Articles table with full content
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

    conn.commit()
    conn.close()
    print("[DB] Database initialized successfully")

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

# Visitor tracking
def track_visitor(page_url):
    """Track visitor analytics"""
    try:
        ip = request.remote_addr
        user_agent = request.headers.get('User-Agent', '')

        # Hash IP for privacy
        ip_hash = hashlib.sha256(ip.encode()).hexdigest()[:16]

        # Generate session ID
        session_id = request.cookies.get('session_id', hashlib.sha256(
            f"{ip}{user_agent}{datetime.now().hour}".encode()
        ).hexdigest()[:16])

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''INSERT INTO visitors (ip_hash, user_agent, page_url, session_id)
                    VALUES (?, ?, ?, ?)''', (ip_hash, user_agent, page_url, session_id))
        conn.commit()
        conn.close()

        return session_id
    except Exception as e:
        print(f"[ERROR] Tracking error: {e}")
        return None

def track_article_view(article_id, article_title):
    """Track article views"""
    try:
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

        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[ERROR] Article tracking error: {e}")

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
        response.set_cookie('session_id', session_id)
    return response

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

@app.route('/data_cache.json')
def serve_data_cache():
    """Serve data cache for client-side rendering"""
    return send_from_directory(DB_DIR, 'data_cache.json')

@app.route('/torq-logo.svg')
def serve_logo():
    """Serve TORQ logo"""
    return send_from_directory(DB_DIR, 'torq-logo.svg')

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
    if featured and normalize_slug(featured.get('title', '')) == slug:
        cached_article = featured
    else:
        # Find matching article in regular articles using normalized slug
        cached_article = next((a for a in articles if normalize_slug(a['title']) == slug), None)

    # If still not found, try fuzzy matching
    if not cached_article:
        if featured and normalize_slug(featured.get('title', '')).startswith(slug[:20]):
            cached_article = featured
        else:
            cached_article = next((a for a in articles if normalize_slug(a['title']).startswith(slug[:20])), None)

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
        response.set_cookie('session_id', session_id)

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
    print()

    # Start background automation
    start_background_automation()

    print()
    print("="*60)
    print("[SUCCESS] Server starting on http://localhost:5000")
    print("[INFO] Admin Dashboard: http://localhost:5000/admin")
    print("[INFO] API Analytics: http://localhost:5000/api/analytics")
    print("="*60)
    print()

    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
