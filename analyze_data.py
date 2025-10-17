#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TORQ Tech News - Analytics Analysis Tool

Comprehensive analytics analysis and reporting tool for TORQ Tech News.
Analyzes visitor behavior, content performance, conversion funnels, and more.
"""

import sys
import os
import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
import argparse

# Force UTF-8 encoding for Windows compatibility
if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'


class TORQAnalyzer:
    """Comprehensive analytics analyzer for TORQ Tech News"""

    def __init__(self, db_path: str = None, cache_path: str = None):
        """Initialize analyzer with database and cache paths"""
        if db_path is None:
            db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "analytics.db")
        if cache_path is None:
            cache_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_cache.json")

        self.db_path = db_path
        self.cache_path = cache_path
        self.conn = None

    def connect(self):
        """Connect to database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            return True
        except Exception as e:
            print(f"[ERROR] Failed to connect to database: {e}")
            return False

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

    def get_visitor_stats(self, days: int = 7) -> dict:
        """Get visitor statistics for the past N days"""
        if not self.conn:
            return {}

        c = self.conn.cursor()

        # Total unique visitors
        c.execute('''SELECT COUNT(DISTINCT session_id) FROM visitors
                    WHERE timestamp > datetime('now', '-{} days')'''.format(days))
        unique_visitors = c.fetchone()[0] or 0

        # Total page views
        c.execute('''SELECT COUNT(*) FROM visitors
                    WHERE timestamp > datetime('now', '-{} days')'''.format(days))
        total_views = c.fetchone()[0] or 0

        # Active sessions
        c.execute('SELECT COUNT(*) FROM user_sessions WHERE is_active = 1')
        active_sessions = c.fetchone()[0] or 0

        # Average session duration
        c.execute('''SELECT AVG(duration_seconds) FROM user_sessions
                    WHERE duration_seconds > 0 AND start_time > datetime('now', '-{} days')'''.format(days))
        avg_duration = c.fetchone()[0] or 0

        # Bounce rate
        c.execute('''SELECT AVG(bounce_rate) FROM user_sessions
                    WHERE start_time > datetime('now', '-{} days')'''.format(days))
        bounce_rate = c.fetchone()[0] or 0

        return {
            'unique_visitors': unique_visitors,
            'total_page_views': total_views,
            'active_sessions': active_sessions,
            'avg_session_duration_seconds': round(avg_duration, 2),
            'bounce_rate_percentage': round(bounce_rate * 100, 2),
            'period_days': days
        }

    def get_top_articles(self, limit: int = 10) -> list:
        """Get top viewed articles"""
        if not self.conn:
            return []

        c = self.conn.cursor()
        c.execute('''SELECT article_title, view_count, last_viewed
                    FROM page_views
                    ORDER BY view_count DESC LIMIT ?''', (limit,))

        articles = []
        for row in c.fetchall():
            articles.append({
                'title': row[0],
                'views': row[1],
                'last_viewed': row[2]
            })

        return articles

    def get_traffic_sources(self, limit: int = 10) -> list:
        """Get top traffic sources (referrers)"""
        if not self.conn:
            return []

        c = self.conn.cursor()
        c.execute('''SELECT referrer_url, landing_page, SUM(count) as total
                    FROM referrers
                    GROUP BY referrer_url
                    ORDER BY total DESC LIMIT ?''', (limit,))

        sources = []
        for row in c.fetchall():
            sources.append({
                'referrer': row[0],
                'landing_page': row[1],
                'visits': row[2]
            })

        return sources

    def get_device_breakdown(self, days: int = 7) -> dict:
        """Get device type breakdown"""
        if not self.conn:
            return {}

        c = self.conn.cursor()
        c.execute('''SELECT device_type, COUNT(*) as count
                    FROM user_sessions
                    WHERE start_time > datetime('now', '-{} days')
                    GROUP BY device_type'''.format(days))

        breakdown = {'desktop': 0, 'mobile': 0, 'tablet': 0, 'unknown': 0}
        total = 0

        for row in c.fetchall():
            device_type = row[0] or 'unknown'
            count = row[1]
            breakdown[device_type] = count
            total += count

        # Calculate percentages
        if total > 0:
            for device in breakdown:
                percentage = (breakdown[device] / total) * 100
                breakdown[device] = {
                    'count': breakdown[device],
                    'percentage': round(percentage, 2)
                }

        return breakdown

    def get_browser_breakdown(self, days: int = 7, limit: int = 10) -> list:
        """Get browser breakdown"""
        if not self.conn:
            return []

        c = self.conn.cursor()
        c.execute('''SELECT browser, COUNT(*) as count
                    FROM user_sessions
                    WHERE start_time > datetime('now', '-{} days')
                    GROUP BY browser
                    ORDER BY count DESC LIMIT ?'''.format(days), (limit,))

        browsers = []
        for row in c.fetchall():
            browsers.append({
                'browser': row[0],
                'sessions': row[1]
            })

        return browsers

    def get_conversion_funnel(self, days: int = 7) -> dict:
        """Analyze conversion funnel"""
        if not self.conn:
            return {}

        c = self.conn.cursor()
        c.execute('''SELECT funnel_step, COUNT(*) as count
                    FROM conversion_funnels
                    WHERE timestamp > datetime('now', '-{} days')
                    GROUP BY funnel_step
                    ORDER BY count DESC'''.format(days))

        funnel = {}
        for row in c.fetchall():
            funnel[row[0]] = row[1]

        # Calculate conversion rates
        homepage_visits = funnel.get('homepage', 0)
        if homepage_visits > 0:
            article_views = funnel.get('article_view', 0)
            scroll_100 = funnel.get('scroll_100', 0)
            external_clicks = funnel.get('external_click', 0)

            funnel_analysis = {
                'homepage_visits': homepage_visits,
                'article_views': article_views,
                'full_scrolls': scroll_100,
                'external_clicks': external_clicks,
                'homepage_to_article_rate': round((article_views / homepage_visits) * 100, 2) if homepage_visits > 0 else 0,
                'article_completion_rate': round((scroll_100 / article_views) * 100, 2) if article_views > 0 else 0,
                'external_click_rate': round((external_clicks / article_views) * 100, 2) if article_views > 0 else 0
            }
        else:
            funnel_analysis = {
                'homepage_visits': 0,
                'article_views': 0,
                'full_scrolls': 0,
                'external_clicks': 0,
                'homepage_to_article_rate': 0,
                'article_completion_rate': 0,
                'external_click_rate': 0
            }

        return funnel_analysis

    def get_hourly_activity(self, days: int = 7) -> list:
        """Get hourly activity pattern"""
        if not self.conn:
            return []

        c = self.conn.cursor()
        c.execute('''SELECT strftime('%H', timestamp) as hour, COUNT(*) as count
                    FROM visitors
                    WHERE timestamp > datetime('now', '-{} days')
                    GROUP BY hour
                    ORDER BY hour'''.format(days))

        activity = []
        for row in c.fetchall():
            activity.append({
                'hour': int(row[0]),
                'visits': row[1]
            })

        return activity

    def get_user_engagement(self, days: int = 7) -> dict:
        """Get user engagement metrics"""
        if not self.conn:
            return {}

        c = self.conn.cursor()

        # Average scroll depth
        c.execute('''SELECT AVG(CAST(value AS INTEGER)) as avg_depth
                    FROM user_events
                    WHERE event_type = 'scroll_depth'
                    AND timestamp > datetime('now', '-{} days')'''.format(days))
        avg_scroll = c.fetchone()[0] or 0

        # Average time on page
        c.execute('''SELECT AVG(CAST(value AS REAL)) as avg_time
                    FROM user_events
                    WHERE event_type = 'time_on_page'
                    AND timestamp > datetime('now', '-{} days')'''.format(days))
        avg_time = c.fetchone()[0] or 0

        # Total clicks (internal + external)
        c.execute('''SELECT COUNT(*) FROM user_events
                    WHERE event_type IN ('internal_link', 'outbound_link', 'button_click')
                    AND timestamp > datetime('now', '-{} days')'''.format(days))
        total_clicks = c.fetchone()[0] or 0

        return {
            'avg_scroll_depth_percent': round(avg_scroll, 2),
            'avg_time_on_page_seconds': round(avg_time, 2),
            'total_clicks': total_clicks
        }

    def get_content_stats(self) -> dict:
        """Get content statistics from data cache"""
        try:
            with open(self.cache_path, 'r', encoding='utf-8') as f:
                cache = json.load(f)

            articles = cache.get('articles', [])
            featured = cache.get('featured', {})
            sources = cache.get('sources_used', [])
            last_update = cache.get('timestamp', 'Unknown')

            # Count articles with full text
            full_text_count = sum(1 for a in articles if a.get('full_text'))

            return {
                'total_articles': len(articles),
                'articles_with_full_text': full_text_count,
                'featured_article': featured.get('title', 'N/A'),
                'sources_used': sources,
                'last_update': last_update,
                'categories': list(set(a.get('category', 'Unknown') for a in articles))
            }
        except Exception as e:
            print(f"[WARN] Could not read content cache: {e}")
            return {}

    def get_recent_activity(self, limit: int = 20) -> list:
        """Get recent visitor activity"""
        if not self.conn:
            return []

        c = self.conn.cursor()
        c.execute('''SELECT page_url, timestamp, session_id
                    FROM visitors
                    ORDER BY timestamp DESC LIMIT ?''', (limit,))

        activity = []
        for row in c.fetchall():
            activity.append({
                'page': row[0],
                'timestamp': row[1],
                'session': row[2][:8] + '...'  # Truncate for privacy
            })

        return activity

    def generate_report(self, days: int = 7, detailed: bool = True) -> dict:
        """Generate comprehensive analytics report"""
        print("="*70)
        print(f"TORQ Tech News - Analytics Report (Last {days} Days)")
        print("="*70)
        print()

        report = {
            'generated_at': datetime.now().isoformat(),
            'period_days': days
        }

        # Visitor Statistics
        print("[1] VISITOR STATISTICS")
        print("-" * 70)
        visitor_stats = self.get_visitor_stats(days)
        report['visitor_stats'] = visitor_stats

        print(f"  Unique Visitors:       {visitor_stats['unique_visitors']:,}")
        print(f"  Total Page Views:      {visitor_stats['total_page_views']:,}")
        print(f"  Active Sessions:       {visitor_stats['active_sessions']:,}")
        print(f"  Avg Session Duration:  {visitor_stats['avg_session_duration_seconds']:.1f} seconds")
        print(f"  Bounce Rate:           {visitor_stats['bounce_rate_percentage']:.2f}%")
        print()

        # Top Articles
        print("[2] TOP ARTICLES")
        print("-" * 70)
        top_articles = self.get_top_articles(10)
        report['top_articles'] = top_articles

        if top_articles:
            for i, article in enumerate(top_articles, 1):
                title = article['title'][:60] + '...' if len(article['title']) > 60 else article['title']
                print(f"  {i:2d}. {title:<63} {article['views']:>4} views")
        else:
            print("  No article data available yet.")
        print()

        # Traffic Sources
        print("[3] TRAFFIC SOURCES")
        print("-" * 70)
        traffic_sources = self.get_traffic_sources(10)
        report['traffic_sources'] = traffic_sources

        if traffic_sources:
            for i, source in enumerate(traffic_sources, 1):
                referrer = source['referrer'][:50] + '...' if len(source['referrer']) > 50 else source['referrer']
                print(f"  {i:2d}. {referrer:<53} {source['visits']:>4} visits")
        else:
            print("  No referrer data available yet.")
        print()

        # Device Breakdown
        print("[4] DEVICE BREAKDOWN")
        print("-" * 70)
        device_breakdown = self.get_device_breakdown(days)
        report['device_breakdown'] = device_breakdown

        for device, stats in device_breakdown.items():
            if isinstance(stats, dict):
                print(f"  {device.capitalize():<15} {stats['count']:>6} sessions ({stats['percentage']:>5.1f}%)")
        print()

        # Browser Breakdown
        print("[5] BROWSER BREAKDOWN")
        print("-" * 70)
        browser_breakdown = self.get_browser_breakdown(days, 10)
        report['browser_breakdown'] = browser_breakdown

        if browser_breakdown:
            for i, browser in enumerate(browser_breakdown, 1):
                browser_name = browser['browser'][:50] + '...' if len(browser['browser']) > 50 else browser['browser']
                print(f"  {i:2d}. {browser_name:<53} {browser['sessions']:>4} sessions")
        else:
            print("  No browser data available yet.")
        print()

        # Conversion Funnel
        print("[6] CONVERSION FUNNEL ANALYSIS")
        print("-" * 70)
        funnel = self.get_conversion_funnel(days)
        report['conversion_funnel'] = funnel

        print(f"  Homepage Visits:                {funnel['homepage_visits']:,}")
        print(f"  Article Views:                  {funnel['article_views']:,}")
        print(f"  Full Article Scrolls:           {funnel['full_scrolls']:,}")
        print(f"  External Link Clicks:           {funnel['external_clicks']:,}")
        print()
        print(f"  Homepage → Article Rate:        {funnel['homepage_to_article_rate']:.2f}%")
        print(f"  Article Completion Rate:        {funnel['article_completion_rate']:.2f}%")
        print(f"  External Click Rate:            {funnel['external_click_rate']:.2f}%")
        print()

        # User Engagement
        print("[7] USER ENGAGEMENT METRICS")
        print("-" * 70)
        engagement = self.get_user_engagement(days)
        report['user_engagement'] = engagement

        print(f"  Avg Scroll Depth:      {engagement['avg_scroll_depth_percent']:.1f}%")
        print(f"  Avg Time on Page:      {engagement['avg_time_on_page_seconds']:.1f} seconds")
        print(f"  Total Clicks:          {engagement['total_clicks']:,}")
        print()

        # Content Statistics
        print("[8] CONTENT STATISTICS")
        print("-" * 70)
        content_stats = self.get_content_stats()
        report['content_stats'] = content_stats

        if content_stats:
            print(f"  Total Articles:        {content_stats.get('total_articles', 0)}")
            print(f"  Articles w/ Full Text: {content_stats.get('articles_with_full_text', 0)}")
            print(f"  Featured Article:      {content_stats.get('featured_article', 'N/A')}")
            print(f"  Sources Used:          {', '.join(content_stats.get('sources_used', []))}")
            print(f"  Last Update:           {content_stats.get('last_update', 'Unknown')}")
            print(f"  Categories:            {', '.join(content_stats.get('categories', []))}")
        else:
            print("  No content data available.")
        print()

        if detailed:
            # Hourly Activity
            print("[9] HOURLY ACTIVITY PATTERN")
            print("-" * 70)
            hourly_activity = self.get_hourly_activity(days)
            report['hourly_activity'] = hourly_activity

            if hourly_activity:
                # Create simple bar chart
                max_visits = max(h['visits'] for h in hourly_activity) if hourly_activity else 1
                for activity in hourly_activity:
                    hour = activity['hour']
                    visits = activity['visits']
                    bar_length = int((visits / max_visits) * 40) if max_visits > 0 else 0
                    bar = '█' * bar_length
                    print(f"  {hour:02d}:00  {bar:<40} {visits:>4}")
            else:
                print("  No hourly activity data available yet.")
            print()

            # Recent Activity
            print("[10] RECENT ACTIVITY")
            print("-" * 70)
            recent = self.get_recent_activity(10)
            report['recent_activity'] = recent

            if recent:
                for activity in recent:
                    timestamp = activity['timestamp'][:19]  # Trim milliseconds
                    page = activity['page'][:30] + '...' if len(activity['page']) > 30 else activity['page']
                    print(f"  {timestamp}  {page:<33} [{activity['session']}]")
            else:
                print("  No recent activity available yet.")
            print()

        print("="*70)
        print(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
        print()

        return report

    def export_report(self, output_file: str, days: int = 7):
        """Export report to JSON file"""
        if not self.connect():
            print("[ERROR] Could not connect to database")
            return False

        try:
            report = self.generate_report(days, detailed=True)

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)

            print(f"[SUCCESS] Report exported to: {output_file}")
            return True

        except Exception as e:
            print(f"[ERROR] Failed to export report: {e}")
            return False
        finally:
            self.close()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='TORQ Tech News Analytics Analysis Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate report for last 7 days
  python analyze_data.py

  # Generate report for last 30 days
  python analyze_data.py --days 30

  # Export report to JSON
  python analyze_data.py --export report.json

  # Specify custom database path
  python analyze_data.py --db /path/to/analytics.db
        """
    )

    parser.add_argument('--days', type=int, default=7,
                       help='Number of days to analyze (default: 7)')
    parser.add_argument('--export', type=str, metavar='FILE',
                       help='Export report to JSON file')
    parser.add_argument('--db', type=str, metavar='PATH',
                       help='Path to analytics database')
    parser.add_argument('--cache', type=str, metavar='PATH',
                       help='Path to data cache file')
    parser.add_argument('--simple', action='store_true',
                       help='Generate simple report (no hourly breakdown)')

    args = parser.parse_args()

    # Create analyzer
    analyzer = TORQAnalyzer(db_path=args.db, cache_path=args.cache)

    # Check if database exists
    if not os.path.exists(analyzer.db_path):
        print(f"[ERROR] Database not found: {analyzer.db_path}")
        print("[INFO] Run the Flask app first to initialize the database:")
        print("  python app.py")
        return 1

    # Connect to database
    if not analyzer.connect():
        return 1

    try:
        if args.export:
            # Export mode
            analyzer.export_report(args.export, args.days)
        else:
            # Console report mode
            analyzer.generate_report(args.days, detailed=not args.simple)

        return 0

    except Exception as e:
        print(f"[ERROR] Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

    finally:
        analyzer.close()


if __name__ == '__main__':
    sys.exit(main())
