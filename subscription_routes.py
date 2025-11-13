"""Newsletter subscription routes for Flask application.

This module provides REST API endpoints for newsletter subscriptions
using Azure Table Storage with SQLite fallback.
"""

from __future__ import annotations

import json
import logging
import sqlite3
from pathlib import Path

from flask import jsonify, request

# Logging setup
logger = logging.getLogger(__name__)

# Database path
DB_PATH = Path(__file__).parent / "analytics.db"


def register_subscription_routes(app) -> None:
    """Register subscription routes to Flask app.

    Args:
        app: Flask application instance.

    Example:
        >>> from flask import Flask
        >>> app = Flask(__name__)
        >>> register_subscription_routes(app)
    """

    @app.route('/api/subscribe', methods=['POST'])
    def subscribe():
        """Newsletter subscription endpoint with Azure Table Storage and SQLite fallback.

        Accepts JSON payload with email address, validates format, checks for duplicates,
        and stores subscription in Azure Table Storage (primary) or SQLite (fallback).

        Request Body:
            {
                "email": "user@example.com"
            }

        Response (Success):
            {
                "success": true,
                "message": "Successfully subscribed!",
                "backend": "azure"
            }

        Response (Error):
            {
                "success": false,
                "error": "Email already subscribed"
            }

        Returns:
            JSON response with success status and message.
            HTTP 200: Successful subscription
            HTTP 400: Validation error (invalid email format)
            HTTP 409: Duplicate subscription (email already exists)
            HTTP 500: Server error
        """
        try:
            # Import subscribers storage module
            from subscribers_storage import (
                SubscribersStorage,
                ValidationError,
                DuplicateSubscriptionError,
                SubscriptionError
            )

            # Parse request data
            data = request.get_json()

            if not data:
                return jsonify({
                    'success': False,
                    'error': 'Request body must be JSON'
                }), 400

            email = data.get('email')

            if not email:
                return jsonify({
                    'success': False,
                    'error': 'Email address is required'
                }), 400

            # Get client IP for analytics (hashed for privacy)
            ip_address = request.remote_addr

            # Initialize storage and subscribe
            storage = SubscribersStorage()
            result = storage.subscribe(email, ip_address)

            # Track subscription event in analytics
            session_id = request.cookies.get('session_id')
            if session_id:
                try:
                    conn = sqlite3.connect(str(DB_PATH))
                    c = conn.cursor()
                    c.execute(
                        '''INSERT INTO conversion_funnels (session_id, funnel_step, metadata)
                        VALUES (?, ?, ?)''',
                        (session_id, 'newsletter_subscribe', json.dumps({
                            'email_domain': email.split('@')[1],
                            'backend': result.storage_backend
                        }))
                    )
                    conn.commit()
                    conn.close()
                except Exception as e:
                    logger.warning(f"Failed to track subscription event: {e}")

            # Return success response
            return jsonify({
                'success': True,
                'message': result.message,
                'backend': result.storage_backend
            }), 200

        except ValidationError as e:
            # Email validation failed
            logger.warning(f"Validation error: {e.message}, Context: {e.context}")
            return jsonify({
                'success': False,
                'error': e.message
            }), e.status_code

        except DuplicateSubscriptionError as e:
            # Email already subscribed
            logger.info(f"Duplicate subscription: {e.context}")
            return jsonify({
                'success': False,
                'error': e.message
            }), e.status_code

        except SubscriptionError as e:
            # Subscription operation failed
            logger.error(f"Subscription error: {e.message}, Context: {e.context}")
            return jsonify({
                'success': False,
                'error': 'Failed to process subscription. Please try again later.'
            }), e.status_code

        except Exception as e:
            # Unexpected error
            logger.critical(f"Unexpected error in subscribe endpoint: {e}", exc_info=True)
            return jsonify({
                'success': False,
                'error': 'An unexpected error occurred. Please try again later.'
            }), 500

    @app.route('/api/subscribers/count', methods=['GET'])
    def subscribers_count():
        """Get total subscriber count.

        Returns subscriber count from Azure Table Storage or SQLite fallback.

        Response:
            {
                "success": true,
                "count": 1234,
                "backend": "azure"
            }

        Returns:
            JSON response with subscriber count and backend information.
        """
        try:
            from subscribers_storage import SubscribersStorage

            storage = SubscribersStorage()
            stats = storage.get_subscriber_count()

            return jsonify({
                'success': stats['success'],
                'count': stats['count'],
                'backend': stats['backend']
            }), 200

        except Exception as e:
            logger.error(f"Failed to get subscriber count: {e}")
            return jsonify({
                'success': False,
                'error': 'Failed to retrieve subscriber count'
            }), 500

    logger.info("Newsletter subscription routes registered successfully")
