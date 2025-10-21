#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for analyze_data.py
Creates sample database with test data to verify the analyzer works correctly
"""

import sqlite3
import os
import sys
from datetime import datetime, timedelta
import random

def create_test_database(db_path="test_analytics.db"):
    """Create a test database with sample data"""
    
    # Remove existing test database
    if os.path.exists(db_path):
        os.remove(db_path)
    
    print(f"[*] Creating test database: {db_path}")
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Create tables (same as app.py)
    c.execute('''CREATE TABLE IF NOT EXISTS visitors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip_hash TEXT,
        user_agent TEXT,
        page_url TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        session_id TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS page_views (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        article_id TEXT,
        article_title TEXT,
        view_count INTEGER DEFAULT 1,
        last_viewed DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    
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
    
    c.execute('''CREATE TABLE IF NOT EXISTS user_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        event_type TEXT,
        element_id TEXT,
        value TEXT,
        page_url TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS referrers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        referrer_url TEXT,
        landing_page TEXT,
        count INTEGER DEFAULT 1,
        first_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
        last_seen DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS conversion_funnels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        funnel_step TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        metadata TEXT
    )''')
    
    # Generate sample data
    print("[*] Generating sample data...")
    
    devices = ['desktop', 'mobile', 'tablet']
    browsers = ['Chrome 120', 'Firefox 121', 'Safari 17', 'Edge 120']
    referrers = ['google.com', 'twitter.com', 'linkedin.com', 'direct', 'facebook.com']
    articles = [
        'AI Strategy: Building Competitive Advantage',
        'Leadership in the Age of Automation',
        'Sustainability Meets Innovation',
        'The Future of Digital Transformation',
        'Quantum Computing in Enterprise'
    ]
    
    # Generate 100 sessions over last 7 days
    for i in range(100):
        session_id = f"sess_{i:04d}"
        device = random.choice(devices)
        browser = random.choice(browsers)
        referrer = random.choice(referrers)
        
        # Random timestamp within last 7 days
        days_ago = random.randint(0, 6)
        hours_ago = random.randint(0, 23)
        timestamp = datetime.now() - timedelta(days=days_ago, hours=hours_ago)
        
        # Duration and pages
        duration = random.randint(30, 600)  # 30 sec to 10 min
        pages = random.randint(1, 5)
        bounce = 1.0 if pages == 1 else 0.0
        
        # Insert session
        c.execute('''INSERT INTO user_sessions 
                    (session_id, visitor_id, start_time, total_pages, duration_seconds, 
                     bounce_rate, device_type, browser, landing_page, referrer_url, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                 (session_id, f"user_{i%50}", timestamp, pages, duration, 
                  bounce, device, browser, '/', referrer, 0))
        
        # Insert homepage visit
        c.execute('''INSERT INTO visitors (ip_hash, user_agent, page_url, timestamp, session_id)
                    VALUES (?, ?, ?, ?, ?)''',
                 (f"hash_{i%50}", f"UserAgent {browser}", '/', timestamp, session_id))
        
        c.execute('''INSERT INTO conversion_funnels (session_id, funnel_step, timestamp, metadata)
                    VALUES (?, ?, ?, ?)''',
                 (session_id, 'homepage', timestamp, '{}'))
        
        # Some sessions view articles
        if pages > 1:
            article = random.choice(articles)
            article_timestamp = timestamp + timedelta(seconds=10)
            
            c.execute('''INSERT INTO visitors (ip_hash, user_agent, page_url, timestamp, session_id)
                        VALUES (?, ?, ?, ?, ?)''',
                     (f"hash_{i%50}", f"UserAgent {browser}", f'/article/{article[:20]}', 
                      article_timestamp, session_id))
            
            c.execute('''INSERT INTO conversion_funnels (session_id, funnel_step, timestamp, metadata)
                        VALUES (?, ?, ?, ?)''',
                     (session_id, 'article_view', article_timestamp, '{}'))
            
            # Track scroll events
            for depth in [25, 50, 75, 100]:
                if random.random() > 0.3:  # 70% chance
                    c.execute('''INSERT INTO user_events 
                                (session_id, event_type, element_id, value, page_url, timestamp)
                                VALUES (?, ?, ?, ?, ?, ?)''',
                             (session_id, 'scroll_depth', 'page', str(depth), 
                              f'/article/{article[:20]}', article_timestamp))
            
            # Full scroll means complete
            if random.random() > 0.5:  # 50% complete full scroll
                c.execute('''INSERT INTO conversion_funnels (session_id, funnel_step, timestamp, metadata)
                            VALUES (?, ?, ?, ?)''',
                         (session_id, 'scroll_100', article_timestamp, '{}'))
            
            # Some click external links
            if random.random() > 0.7:  # 30% click external
                c.execute('''INSERT INTO conversion_funnels (session_id, funnel_step, timestamp, metadata)
                            VALUES (?, ?, ?, ?)''',
                         (session_id, 'external_click', article_timestamp, '{}'))
    
    # Generate article views
    for article in articles:
        views = random.randint(10, 100)
        c.execute('''INSERT INTO page_views (article_id, article_title, view_count, last_viewed)
                    VALUES (?, ?, ?, ?)''',
                 (article[:20], article, views, datetime.now()))
    
    # Generate referrer stats
    for ref in referrers:
        count = random.randint(5, 30)
        c.execute('''INSERT INTO referrers (referrer_url, landing_page, count)
                    VALUES (?, ?, ?)''',
                 (ref, '/', count))
    
    conn.commit()
    conn.close()
    
    print(f"[SUCCESS] Test database created with sample data")
    print(f"  - 100 sessions")
    print(f"  - {len(articles)} articles with views")
    print(f"  - {len(referrers)} traffic sources")
    print()
    
    return db_path


if __name__ == '__main__':
    # Create test database
    db_path = create_test_database()
    
    # Run analyzer on test database
    print("[*] Running analyzer on test database...")
    print()
    
    from analyze_data import TORQAnalyzer
    
    analyzer = TORQAnalyzer(db_path=db_path)
    if analyzer.connect():
        analyzer.generate_report(days=7, detailed=True)
        analyzer.close()
        
        # Also test export
        print("\n[*] Testing JSON export...")
        analyzer2 = TORQAnalyzer(db_path=db_path)
        analyzer2.export_report("test_report.json", days=7)
        
        print(f"\n[SUCCESS] Analysis complete!")
        print(f"  - Console report displayed above")
        print(f"  - JSON report: test_report.json")
    else:
        print("[ERROR] Could not connect to test database")
        sys.exit(1)
