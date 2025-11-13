#!/usr/bin/env python3
"""
Basic tests for TORQ Tech News
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_app_imports():
    """Test that main app imports successfully"""
    try:
        import app
        assert hasattr(app, 'app')
        assert hasattr(app, 'init_db')
        print("✓ App imports successfully")
    except ImportError as e:
        assert False, f"Failed to import app: {e}"


def test_aggregator_imports():
    """Test that multi_source_aggregator imports successfully"""
    try:
        import multi_source_aggregator
        assert hasattr(multi_source_aggregator, 'MultiSourceAggregator')
        print("✓ Aggregator imports successfully")
    except ImportError as e:
        assert False, f"Failed to import aggregator: {e}"


def test_subscription_routes_imports():
    """Test that subscription routes import successfully"""
    try:
        import subscription_routes
        assert hasattr(subscription_routes, 'register_subscription_routes')
        print("✓ Subscription routes import successfully")
    except ImportError as e:
        assert False, f"Failed to import subscription routes: {e}"


def test_database_initialization():
    """Test that database initializes correctly"""
    try:
        from app import init_db
        import tempfile
        import sqlite3

        # Use a temporary database for testing
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            test_db = tmp.name

        # Initialize DB
        import app as app_module
        original_db = app_module.DB_PATH
        app_module.DB_PATH = test_db

        init_db()

        # Check that tables were created
        conn = sqlite3.connect(test_db)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()

        # Restore original DB path
        app_module.DB_PATH = original_db

        # Clean up
        os.unlink(test_db)

        assert 'visitors' in tables
        assert 'articles' in tables
        assert 'user_sessions' in tables
        print("✓ Database initializes correctly with required tables")

    except Exception as e:
        assert False, f"Database initialization failed: {e}"


if __name__ == '__main__':
    test_app_imports()
    test_aggregator_imports()
    test_subscription_routes_imports()
    test_database_initialization()
    print("\n✅ All tests passed!")
