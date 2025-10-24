"""Script to add subscription endpoint to app.py"""

# Read the current app.py
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the line with "def health_check():"
insert_index = None
for i, line in enumerate(lines):
    if 'def health_check():' in line:
        insert_index = i
        break

if insert_index is None:
    print("ERROR: Could not find health_check function")
    exit(1)

# Subscription endpoint code to insert
subscription_code = '''
# ===== NEWSLETTER SUBSCRIPTION ENDPOINT =====

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
                conn = sqlite3.connect(DB_PATH)
                c = conn.cursor()
                c.execute(
                    \'\'\'INSERT INTO conversion_funnels (session_id, funnel_step, metadata)
                    VALUES (?, ?, ?)\'\'\',
                    (session_id, 'newsletter_subscribe', json.dumps({
                        'email_domain': email.split('@')[1],
                        'backend': result.storage_backend
                    }))
                )
                conn.commit()
                conn.close()
            except Exception as e:
                print(f"[WARNING] Failed to track subscription event: {e}")

        # Return success response
        return jsonify({
            'success': True,
            'message': result.message,
            'backend': result.storage_backend
        }), 200

    except ValidationError as e:
        # Email validation failed
        print(f"[VALIDATION] {e.message}: {e.context}")
        return jsonify({
            'success': False,
            'error': e.message
        }), e.status_code

    except DuplicateSubscriptionError as e:
        # Email already subscribed
        print(f"[DUPLICATE] {e.message}: {e.context}")
        return jsonify({
            'success': False,
            'error': e.message
        }), e.status_code

    except SubscriptionError as e:
        # Subscription operation failed
        print(f"[ERROR] Subscription error: {e.message}, Context: {e.context}")
        return jsonify({
            'success': False,
            'error': 'Failed to process subscription. Please try again later.'
        }), e.status_code

    except Exception as e:
        # Unexpected error
        print(f"[CRITICAL] Unexpected error in subscribe endpoint: {e}")
        import traceback
        traceback.print_exc()
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
        print(f"[ERROR] Failed to get subscriber count: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve subscriber count'
        }), 500

'''

# Insert the subscription code before health_check
lines.insert(insert_index, subscription_code)

# Write the updated content
with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("SUCCESS: Subscription endpoint added to app.py")
print(f"Inserted at line {insert_index}")
